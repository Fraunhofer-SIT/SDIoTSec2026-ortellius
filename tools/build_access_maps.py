"""Static analysis helper functions."""

from pathlib import Path
from shutil import move
import sys
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, cast
from typing_extensions import TypeIs
from urllib.request import urlretrieve
from zipfile import ZipFile

from pydantic import BaseModel, field_serializer, field_validator
import pyghidra


def is_set_of_ints(value: object) -> TypeIs[set[int]]:
    """Type narrowing function."""
    return isinstance(value, set) and all(
        isinstance(i, int) for i in cast(set[object], value)
    )


def is_list_of_strs(value: object) -> TypeIs[list[str]]:
    """Type narrowing function."""
    return isinstance(value, list) and all(
        isinstance(i, str) for i in cast(list[object], value)
    )


if TYPE_CHECKING:
    from ghidra.program.flatapi import FlatProgramAPI


GHIDRA_URL = (
    "https://github.com/NationalSecurityAgency/ghidra/releases/download/"
    "Ghidra_12.0_build/ghidra_12.0_PUBLIC_20251205.zip"
)


def install_ghidra(install_dir: Path) -> None:
    """Download and extract Ghidra."""

    if install_dir.is_dir():
        return
    install_dir.parent.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        ghidra_zip, _ = urlretrieve(GHIDRA_URL, tmpdir / "ghidra.zip")
        with ZipFile(ghidra_zip) as zf:
            zf.extractall(tmpdir)
        move(next(tmpdir.glob("ghidra_*")), install_dir)


class AnalysisResult(BaseModel):
    """Serializable result of an analysis."""

    read: set[int]
    write: set[int]

    @field_serializer("read", "write")
    def serialize_read(self, value: list[int]) -> list[str]:
        """serialize hexadecimally"""
        return [f"{addr:08x}" for addr in sorted(value)]

    @field_validator("read", "write", mode="before")
    @classmethod
    def validate_from_hex(cls, value: object) -> set[int]:
        """unserialize from hex"""

        if is_set_of_ints(value):
            return value

        if is_list_of_strs(value):
            return {int(v, 16) for v in value}

        raise ValueError("Unexpected type.")


def analyze_file(flatapi: "FlatProgramAPI", outfile: Path) -> None:
    """Analyze loaded file and write results to outfile."""

    program = flatapi.getCurrentProgram()
    memory = program.memory
    for block in memory.blocks:
        block.setRead(True)
        block.setWrite(False)
        block.setExecute(True)
    flatapi.analyzeAll(program)

    instruction = flatapi.firstInstruction
    reads: set[int] = set()
    writes: set[int] = set()
    while instruction is not None:
        for ref in instruction.referencesFrom:
            if ref.stackReference:
                continue
            if ref.referenceType.read:
                reads.add((int(ref.toAddress.offset) // 4) * 4)
            if ref.referenceType.write:
                writes.add((int(ref.toAddress.offset) // 4) * 4)
        instruction = instruction.next
    outfile.write_text(AnalysisResult(read=reads, write=writes).model_dump_json())


def analyze(
    source: Path, destination: Path, ghidra_dir: Path = Path("deps/ghidra")
) -> None:
    """Identify xrefs in firmware binaries."""

    destination.mkdir(exist_ok=True,parents=True)

    install_ghidra(ghidra_dir)
    pyghidra.start(install_dir=ghidra_dir)

    if source.is_dir():
        files = source.rglob("*")
    elif source.is_file():
        files = [source]
    else:
        raise ValueError(f"Source {source} is neither a file nor a directory.")

    for file in files:
        if not file.is_file():
            continue
        with TemporaryDirectory() as tmpdir, pyghidra.open_program(
            file, analyze=False, language="ARM:LE:32:Cortex", project_location=tmpdir
        ) as api:
            analyze_file(api, (destination / file.with_suffix(".json").name))

if __name__ == "__main__":
    analyze(Path(sys.argv[1]), Path(sys.argv[2]))
