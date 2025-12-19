"""Types needed for storage."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol, Self, cast, runtime_checkable

from pydantic import BaseModel

if TYPE_CHECKING:
    # exec environment can be Python 3.12
    from typing import TypeIs  # introduced in Python 3.13

type NativeSerializable = (
    dict[str, NativeSerializable]
    | list[NativeSerializable]
    | str
    | int
    | float
    | bool
    | None
)


def is_native_serializable(obj: object) -> "TypeIs[NativeSerializable]":
    """Check if an object is natively serializable."""
    if isinstance(obj, dict):
        return all(
            isinstance(k, str) and is_native_serializable(v)
            for k, v in cast(dict[object, object], obj).items()
        )
    if isinstance(obj, list):
        return all(is_native_serializable(v) for v in cast(list[object], obj))
    return isinstance(obj, str | int | float | bool | None)


@runtime_checkable
class ExtendedSerializable(Protocol):
    """A protocol for serializable objects."""

    @abstractmethod
    def serialize(self) -> NativeSerializable:
        """Serialize the object to a dictionary."""

    @classmethod
    @abstractmethod
    def unserialize(cls, data: NativeSerializable, hint: Any = None) -> Self:
        """Unserialize the object from a dictionary. Optional hint can be provided."""


type Serializable = NativeSerializable | ExtendedSerializable | BaseModel
