"""Build a memory map from an SVD file."""

from pathlib import Path

from .serstor import Storage

from .model import MemoryMap, Shadow
from .parallelization import Result


def check_storage(prefix: Path) -> None:
    """Check the storage for errors."""

    errors = 0
    total = 0

    storage = Storage(prefix)
    for svd in storage:
        result = Result[MemoryMap].unserialize(storage[svd], MemoryMap)
        total += 1
        if result.error is not None:
            errors += 1
            continue

    print(f"Initial parser found {errors} errors in {total} files.")
    print("Storage has been read successfully.")


def make_shadows(prefix: Path, output_prefix: Path, output_dir: Path | None) -> None:
    """Create shadow files for all memory maps in storage."""

    storage = Storage(prefix)
    output_storage = Storage(output_prefix)
    for svd in storage:
        result = Result[MemoryMap].unserialize(storage[svd], MemoryMap)
        if result.error is not None:
            continue
        memory_map = result.returned
        assert memory_map is not None
        shadow = Shadow(read=set(), write=set(), name=svd)
        for value in memory_map.read_values:
            first_word = value.location.start.byte_offset & ~0x3
            last_word = value.location.last_bit.byte_offset & ~0x3

            for addr in range(first_word, last_word + 1, 4):
                shadow.read.add(addr)
        for value in memory_map.written_values:
            first_word = value.location.start.byte_offset & ~0x3
            last_word = value.location.last_bit.byte_offset & ~0x3
            for addr in range(first_word, last_word + 1, 4):
                shadow.write.add(addr)
        output_storage[svd] = shadow
    output_storage.export_tar()

    if output_dir is None:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    for svd in output_storage:
        entry = output_storage.getraw(svd)
        destination = (output_dir / svd).with_suffix(".json")
        if not destination.resolve().is_relative_to(output_dir.resolve()):
            raise ValueError("Output directory traversal detected.")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(entry)
