from typing import Iterator, Self
from dataclasses import dataclass
from abc import ABC, abstractmethod


__all__ = [
    "Int3Abstract",
]


@dataclass
class Int3Abstract(ABC):
    _x:int = 0
    _y:int = 0
    _z:int = 0

    def __post_init__(self) -> None:
        assert isinstance(self._x, int), f"{self}.x only supports int type, the input type was {self._x}."
        assert isinstance(self._y, int), f"{self}.y only supports int type, the input type was {self._y}."
        assert isinstance(self._z, int), f"{self}.z only supports int type, the input type was {self._z}."

    @classmethod
    @abstractmethod
    def static_class(cls, *args, **kwargs) -> "Int3Abstract":
        """_summary_

        Returns:
            Int3Abstract: _description_
        """
        return Int3Abstract(*args, **kwargs)

    def __iter__(self) -> Iterator[int]:
        return iter((self._x, self._y, self._z))

    def __add__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x + rhs, self._y + rhs, self._z + rhs)
        elif isinstance(rhs, Int3Abstract):
            return self.static_class(self._x + rhs._x, self._y + rhs._y, self._z + rhs._z)
        else:
            raise NotImplementedError()

    def __sub__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x - rhs, self._y - rhs, self._z - rhs)
        elif isinstance(rhs, Int3Abstract):
            return self.static_class(self._x - rhs._x, self._y - rhs._y, self._z - rhs._z)
        else:
            raise NotImplementedError()

    def __mul__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x * rhs, self._y * rhs, self._z * rhs)
        elif isinstance(rhs, Int3Abstract):
            return self.static_class(self._x * rhs._x, self._y * rhs._y, self._z * rhs._z)
        else:
            raise NotImplementedError()

    def __truediv__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x / rhs, self._y / rhs, self._z / rhs)
        elif isinstance(rhs, Int3Abstract):
            return self.static_class(self._x / rhs._x, self._y / rhs._y, self._z / rhs._z)
        else:
            raise NotImplementedError()

    @classmethod
    def from_str(cls, value:str, sep:str) -> Self:
        """数値を3つ含む文字列から作成

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
        return cls(0, 0, 0)
