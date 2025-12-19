"""Storage class for arbitrary serializable objects."""

import json
import sqlite3
import tarfile
from collections.abc import Iterator, MutableMapping
from contextlib import AbstractContextManager
from io import BytesIO
from logging import info
from pathlib import Path
from types import TracebackType

from pydantic import BaseModel

from .abstract import (
    ExtendedSerializable,
    NativeSerializable,
    Serializable,
    is_native_serializable,
)


class Storage(MutableMapping[str, Serializable], AbstractContextManager["Storage"]):
    """Storage class for arbitrary serializable objects."""

    prefix: Path

    ramcache: dict[str, str | None]
    _conn: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self, prefix: Path):
        if prefix.name.endswith(".tar.gz"):
            # pathlib does not see ".tar" as part of the suffix
            prefix = prefix.with_suffix("")
            # now it does
        self.prefix = prefix

        import_tar_afterwards = False

        if not self.prefix.with_suffix(".cache").exists():
            info("No cache file found, creating new one.")
            if self.prefix.with_suffix(".tar.gz").exists():
                info("Found tar.gz file. Will import after creation.")
                import_tar_afterwards = True

        self._conn = sqlite3.connect(
            str(self.prefix.with_suffix(".cache")), autocommit=False
        )
        self._conn.rollback()
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS storage (handle TEXT PRIMARY KEY, data BLOB)"
        )
        self._conn.commit()

        self.ramcache = {
            handle: None
            for handle, in self._cursor.execute("SELECT handle FROM storage").fetchall()
        }

        if import_tar_afterwards:
            self.import_tar()

    def getraw(self, handle: str) -> str:
        """Get stored serialized object."""
        if (val := self.ramcache[handle]) is not None:
            return val
        result = self._cursor.execute(
            "SELECT data FROM storage WHERE handle = ?", (handle,)
        ).fetchone()
        assert isinstance(result[0], str)
        self.ramcache[handle] = result[0]
        return result[0]

    def get_and_unserialize[T: ExtendedSerializable | BaseModel](
        self, handle: str, typ: type[T]
    ) -> T:
        """Get and unserialize stored object."""
        raw = self.getraw(handle)
        if issubclass(typ, ExtendedSerializable):
            data = json.loads(raw)
            assert is_native_serializable(data)
            return typ.unserialize(data)
        return typ.model_validate_json(raw)

    def export_tar(self) -> None:
        """Write the cached storage into a compressed tarball."""
        with tarfile.open(self.prefix.with_suffix(".tar.gz"), "w:gz") as tar:
            for handle in self:
                data = BytesIO(self.getraw(handle).encode())
                tinfo = tarfile.TarInfo(handle)
                tinfo.size = len(data.getvalue())
                tar.addfile(tinfo, data)

    def import_tar(self) -> None:
        """Read the cached storage from a compressed tarball."""
        with tarfile.open(self.prefix.with_suffix(".tar.gz"), "r:gz") as tar:
            for member in tar:
                handle = member.name
                file = tar.extractfile(member)
                assert file is not None
                self[handle] = json.loads(file.read().decode())

    def __getitem__(self, handle: str) -> NativeSerializable:
        item = json.loads(self.getraw(handle))
        assert is_native_serializable(item)
        return item

    def __setitem__(self, handle: str, result: Serializable) -> None:
        if isinstance(result, ExtendedSerializable):
            serialized = json.dumps(result.serialize())
        elif isinstance(result, BaseModel):
            serialized = result.model_dump_json()
        else:
            serialized = json.dumps(result)

        if handle in self:
            self._cursor.execute(
                "UPDATE storage SET data = ? WHERE handle = ?", (handle, serialized)
            )
        else:
            self._cursor.execute(
                "INSERT INTO storage (handle, data) VALUES (?, ?)", (handle, serialized)
            )
        self._conn.commit()
        self.ramcache[handle] = serialized

    def __delitem__(self, key: str) -> None:
        if key not in self:
            raise KeyError(key)
        self._cursor.execute("DELETE FROM storage WHERE handle = ?", (key,))
        self._conn.commit()
        del self.ramcache[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.ramcache)

    def __contains__(self, handle: object) -> bool:
        if not isinstance(handle, str):
            return False
        return handle in self.ramcache

    def __len__(self) -> int:
        return len(self.ramcache)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._conn.close()
