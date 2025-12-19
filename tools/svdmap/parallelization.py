"""Parallelization utilities."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from time import sleep
from typing import Self, TypedDict
from warnings import WarningMessage, catch_warnings, warn

import psutil
from pydantic import BaseModel
from .serstor.abstract import (
    ExtendedSerializable,
    NativeSerializable,
    Serializable,
    is_native_serializable,
)


@dataclass
class Result[T: Serializable](ExtendedSerializable):
    """Parallelization-friendly result container."""

    class Serialized(TypedDict):
        """
        Serializable version of Result. Keep updated with serialize().
        """

        args: list[str]
        kwargs: dict[str, str]
        returned: str
        error: str | None
        warnings: list[str]

    args: Sequence[object]
    kwargs: Mapping[str, object]
    returned: T | None
    error: Exception | None
    warnings: list[WarningMessage]

    @property
    def success(self) -> bool:
        """Return True if the function did not crash."""
        return self.error is None

    @staticmethod
    def contained[**P, _T: Serializable](
        func: Callable[P, _T],
    ) -> Callable[P, Result[_T]]:
        """Decorate a function to return a Result."""

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[_T]:
            with catch_warnings(record=True) as w:
                try:
                    returned = func(*args, **kwargs)
                    return Result(args, kwargs, returned, None, w)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    return Result(args, kwargs, None, e, w)

        return wrapper

    def _serialize(self) -> Serialized:
        """Return a serializable version of the result."""
        if isinstance(self.returned, ExtendedSerializable):
            returned = json.dumps(self.returned.serialize())
        elif isinstance(self.returned, BaseModel):
            returned = self.returned.model_dump_json()
        else:
            returned = json.dumps(self.returned)

        return {
            "args": [str(a) for a in self.args],
            "kwargs": {k: str(v) for k, v in self.kwargs.items()},
            "returned": returned,
            "error": str(self.error) if self.error is not None else None,
            "warnings": [str(w) for w in self.warnings],
        }

    def serialize(self) -> NativeSerializable:
        """Return a serializable version of the result."""

        serialized = self._serialize()
        assert is_native_serializable(serialized)
        return serialized  # pyright: ignore

    @classmethod
    def unserialize(cls, data: NativeSerializable, hint: type[T] | None = None) -> Self:
        """
        Unserialize a result from a serialized version. Drops typing nuance.
        @param hint: Type hint for the returned value.
        """

        if hint is None:
            raise ValueError("Type hint required for unserialization.")

        if not isinstance(data, dict):
            raise TypeError("Expected dict")

        args = data["args"]
        if not isinstance(args, list):
            raise TypeError("Expected list")

        kwargs = data["kwargs"]
        if not isinstance(kwargs, dict):
            raise TypeError("Expected dict")

        returned_str = data["returned"]
        if not isinstance(returned_str, str):
            raise TypeError("Expected str")

        returned: "T|None"
        loaded_json = json.loads(returned_str)
        if loaded_json is None:
            returned = None
        elif issubclass(hint, ExtendedSerializable):
            returned = hint.unserialize(loaded_json)
        elif issubclass(hint, BaseModel):
            returned = hint.model_validate(loaded_json)
        else:
            returned = loaded_json

        match data["error"]:
            case None:
                error = None
            case "None":
                warn("Incorrectly serialized error message. Use newer tarball.")
                error = None
            case _:
                error = Exception(data["error"])

        raw_warnings = data["warnings"]
        if not isinstance(raw_warnings, list):
            raise TypeError("Expected list")
        warnings: list[WarningMessage] = []
        for warning in raw_warnings:
            if not isinstance(warning, str):
                raise TypeError("Expected str")
            warnings.append(WarningMessage(warning, Warning, "", 0))

        return cls(args, kwargs, returned, error, warnings)


def die() -> None:
    """Kill all children and die."""

    process = psutil.Process()

    if not process.children():
        return

    while children := process.children(recursive=True):
        sleep(0.1)
        killcount = 0
        sleepkillcount = 0
        reapcount = 0
        vanishedcount = 0
        for child in children:
            try:
                match child.status():
                    case psutil.STATUS_RUNNING:
                        child.kill()
                        child.wait()
                        killcount += 1
                    case psutil.STATUS_SLEEPING:
                        child.kill()
                        child.wait()
                        sleepkillcount += 1
                    case psutil.STATUS_ZOMBIE:
                        child.wait()
                        reapcount += 1
                    case _:
                        raise RuntimeError(
                            f"Child process {
                                child.pid} has unexpected status {
                                child.status()!r}."
                        )
            except psutil.NoSuchProcess:
                vanishedcount += 1
        if killcount:
            print(f"Killed {killcount} running children.")
        if sleepkillcount:
            print(f"Killed {sleepkillcount} sleeping children.")
        if reapcount:
            print(f"Reaped {reapcount} zombie children.")
        if vanishedcount:
            print(f"{vanishedcount} children vanished.")
            print("All children dead. Suicide time.")
            process.kill()
