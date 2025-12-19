"""Memory map model."""

from dataclasses import dataclass
from typing import Literal, Self
from warnings import warn

from pydantic import BaseModel
from .serstor.abstract import ExtendedSerializable, NativeSerializable


class Address:
    """Address class."""

    bits: int

    def __init__(self, byte_offset: int, bit_offset: int) -> None:
        self.bits = byte_offset * 8 + bit_offset

    @property
    def byte_offset(self) -> int:
        """Byte offset."""
        return self.bits // 8

    @property
    def bit_offset(self) -> int:
        """Bit offset."""
        return self.bits % 8

    def serialize(self) -> NativeSerializable:
        """Serialize the address."""
        return repr(self)

    @classmethod
    def unserialize(cls, data: NativeSerializable) -> Self:
        """Unserialize the address."""

        if not isinstance(data, str):
            raise TypeError("Expected str.")

        byte_off, bit_off = data.split(":")
        return cls(int(byte_off, 16), int(bit_off))

    def __add__(self, other: "Address") -> "Address":
        """Add two addresses."""
        return Address(0, self.bits + other.bits)

    def __sub__(self, other: "Address") -> "Address":
        """Subtract two addresses."""
        return self + (-other)

    def __neg__(self) -> "Address":
        """Negate an address."""
        return Address(0, -self.bits)

    def __lt__(self, other: "Address") -> bool:
        """Compare two addresses."""
        return self.byte_offset < other.byte_offset or (
            self.byte_offset == other.byte_offset and self.bit_offset < other.bit_offset
        )

    def __eq__(self, other: object) -> bool:
        """Compare two addresses."""

        if other == 0:
            return self.bits == 0

        if not isinstance(other, Address):
            return NotImplemented

        return self.bits == other.bits

    def __repr__(self) -> str:
        """Return a string representation of the address."""
        return f"{self.byte_offset:08X}:{self.bit_offset}"


@dataclass
class AddressSpan:
    """Address span class ."""

    start: Address
    size: Address

    @property
    def end(self) -> Address:
        """Return the end address."""
        return self.start + self.size

    @end.setter
    def end(self, value: Address) -> None:
        """Set the end address."""
        self.size = value - self.start

    @property
    def last_bit(self) -> Address:
        """Return the last bit address."""
        return self.start + Address(0, self.size.bits - 1)

    def serialize(self) -> NativeSerializable:
        """Serialize the address span."""
        return {
            "start": self.start.serialize(),
            "size": self.size.serialize(),
        }

    @classmethod
    def unserialize(cls, data: NativeSerializable) -> Self:
        """Unserialize the address span."""

        if not isinstance(data, dict):
            raise TypeError("Expected dict")

        return cls(
            Address.unserialize(data["start"]),
            Address.unserialize(data["size"]),
        )

    def __irshift__(self, val: int) -> Self:
        """Shift the beginning of the address right, reducing size."""
        self.start += Address(0, val)
        self.size -= Address(0, val)
        return self

    def __and__(self, other: "AddressSpan") -> bool:
        """Check if two spans overlap."""
        return (
            self.start < other.start + other.size
            and other.start < self.start + self.size
        )

    def __ior__(self, other: "AddressSpan") -> Self:
        """Merge two spans."""
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)
        return self


@dataclass
class Value:
    """Register class ."""

    location: AddressSpan
    reset_value: int | Literal["CONFLICT"]
    reset_mask: int

    hits: int = 1

    @property
    def conflict(self) -> bool:
        """Check if this location was assigned conflicting values."""
        return self.reset_value == "CONFLICT"

    @conflict.setter
    def conflict(self, val: bool) -> None:
        if val:
            self.reset_value = "CONFLICT"
            return
        assert self.reset_value != "CONFLICT"

    def serialize(self) -> NativeSerializable:
        """Serialize the register."""
        serialized = {
            "location": self.location.serialize(),
            "reset_value": (
                self.reset_value
                if isinstance(self.reset_value, str)
                else hex(self.reset_value)
            ),
            "reset_mask": hex(self.reset_mask),
        }
        if self.hits != 1:
            serialized["hits"] = self.hits
        return serialized

    @classmethod
    def unserialize(cls, serialized: NativeSerializable) -> Self:
        """Unserialize the register."""

        if not isinstance(serialized, dict):
            raise TypeError("Expected dict")

        location = AddressSpan.unserialize(serialized["location"])

        str_reset_value = serialized["reset_value"]
        if not isinstance(str_reset_value, str):
            raise TypeError("Expected str")
        if str_reset_value == "CONFLICT":
            reset_value: Literal["CONFLICT"] | int = "CONFLICT"
        else:
            reset_value = int(str_reset_value, 16)

        str_reset_mask = serialized["reset_mask"]
        if not isinstance(str_reset_mask, str):
            raise TypeError("Expected str")
        reset_mask = int(str_reset_mask, 16)

        hits = serialized.get("hits", 1)
        if not isinstance(hits, int):
            raise TypeError("Expected str")

        return cls(location, reset_value, reset_mask, hits)

    def __irshift__(self, val: int) -> Self:
        """Move start address up, discarding leading bits."""
        self.location >>= val
        if self.reset_value != "CONFLICT":
            self.reset_value <<= val
        self.reset_mask <<= val
        return self


class MemoryMap(ExtendedSerializable):
    """Memory map class ."""

    read_values: list[Value]
    written_values: list[Value]

    def __init__(self) -> None:
        self.read_values = []
        self.written_values = []

    @property
    def conflicts(self) -> int:
        """Return the number of conflicting registers."""
        raise NotImplementedError()
        # return sum(v.hits for v in self.read_values if v.conflict)

    def serialize(self) -> NativeSerializable:
        """Serialize the memory map to a native Python object."""
        return {
            "read_values": [value.serialize() for value in self.read_values],
            "written_values": [value.serialize() for value in self.written_values],
        }

    @classmethod
    def unserialize(cls, data: NativeSerializable, hint: None = None) -> Self:
        """Unserialize a memory map from a native Python object."""

        new_map = cls()

        if not isinstance(data, dict):
            raise TypeError("Expected a dict of values")
        read = data["read_values"]
        written = data["written_values"]
        if not isinstance(read, list):
            raise TypeError("Expected a list of read values")
        if not isinstance(written, list):
            raise TypeError("Expected a list of written values")

        for value in read:
            new_map.read_values.append(Value.unserialize(value))
        for value in written:
            new_map.written_values.append(Value.unserialize(value))

        return new_map

    def add_read(self, other: Value) -> Self:
        """Add a readable register to the memory map."""

        for i, v in enumerate(self.read_values):
            if v.location & other.location:
                v.hits += 1
                if v.location == other.location:
                    if v.reset_value == other.reset_value:
                        return self
                warn(f"Conflicting registers at {v.location}.")
                v.location |= other.location
                v.conflict = True
                return self
            if v.location.start > other.location.start:
                self.read_values.insert(i, other)
                return self
        self.read_values.append(other)
        return self

    def add_written(self, other: Value) -> Self:
        """Add a writeable register to the memory map."""

        for i, v in enumerate(self.written_values):
            if v.location & other.location:
                v.hits += 1
                if v.location == other.location:
                    if v.reset_value == other.reset_value:
                        return self
                warn(f"Conflicting registers at {v.location}.")
                v.location |= other.location
                v.conflict = True
                return self
            if v.location.start > other.location.start:
                self.written_values.insert(i, other)
                return self
        self.written_values.append(other)
        return self


class Shadow(BaseModel):
    """Shadow of a memory map. Only keeps track of readable words."""

    name: str
    read: set[int]
    write: set[int]
