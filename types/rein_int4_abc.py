from typing import Iterator, Self
from dataclasses import dataclass
from abc import ABC, abstractmethod


__all__ = [
    "Int4Abstract",
]


@dataclass
class Int4Abstract(ABC):
    _x:int = 0
    _y:int = 0
    _z:int = 0
    _w:int = 0

    def __post_init__(self) -> None:
        assert isinstance(self._x, int), f"{self}.x only supports int type, the input type was {self._x}."
        assert isinstance(self._y, int), f"{self}.y only supports int type, the input type was {self._y}."
        assert isinstance(self._z, int), f"{self}.z only supports int type, the input type was {self._z}."
        assert isinstance(self._w, int), f"{self}.w only supports int type, the input type was {self._w}."

    @classmethod
    @abstractmethod
    def static_class(cls, *args, **kwargs) -> "Int4Abstract":
        """_summary_

        Returns:
            Int4Abstract: _description_
        """
        return Int4Abstract(*args, **kwargs)

    def __iter__(self) -> Iterator[int]:
        return iter((self._x, self._y, self._z, self._w))

    def __add__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x + rhs, self._y + rhs, self._z + rhs, self._w + rhs)
        elif isinstance(rhs, Int4Abstract):
            return self.static_class(self._x + rhs._x, self._y + rhs._y, self._z + rhs._z, self._w + rhs._w)
        else:
            raise NotImplementedError()

    def __sub__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x - rhs, self._y - rhs, self._z - rhs, self._w - rhs)
        elif isinstance(rhs, Int4Abstract):
            return self.static_class(self._x - rhs._x, self._y - rhs._y, self._z - rhs._z, self._w - rhs._w)
        else:
            raise NotImplementedError()

    def __mul__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x * rhs, self._y * rhs, self._z * rhs, self._w * rhs)
        elif isinstance(rhs, Int4Abstract):
            return self.static_class(self._x * rhs._x, self._y * rhs._y, self._z * rhs._z, self._w * rhs._w)
        else:
            raise NotImplementedError()

    def __div__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x / rhs, self._y / rhs, self._z / rhs, self._w / rhs)
        elif isinstance(rhs, Int4Abstract):
            return self.static_class(self._x / rhs._x, self._y / rhs._y, self._z / rhs._z, self._w / rhs._w)
        else:
            raise NotImplementedError()

    @classmethod
    def from_str(cls, value:str, sep:str) -> Self:
        """数値を4つ含む文字列から作成

        Args:
            value (str): 文字列
            sep (str): 区切り文字

        Returns:
            Self: _description_
        """
        assert isinstance(sep, str), f"'sep' only supports str type, the input type was '{type(sep)}'."
        assert len(sep) > 0, "'sep' must be at least 1 character long."
        return cls(*[int(val) for val in value.split(sep)])

    @classmethod
    def zero(cls) -> Self:
        return cls(0, 0, 0, 0)
