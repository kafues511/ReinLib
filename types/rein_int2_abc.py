from typing import Iterator, Self
from dataclasses import dataclass
from abc import ABC, abstractmethod


__all__ = [
    "Int2Abstract",
]


@dataclass
class Int2Abstract(ABC):
    _x:int = 0
    _y:int = 0

    def __post_init__(self) -> None:
        assert isinstance(self._x, int), f"{self}.x only supports int type, the input type was {self._x}."
        assert isinstance(self._y, int), f"{self}.y only supports int type, the input type was {self._y}."

    @classmethod
    @abstractmethod
    def static_class(cls, *args, **kwargs) -> "Int2Abstract":
        """_summary_

        Returns:
            Int2Abstract: _description_
        """
        return Int2Abstract(*args, **kwargs)

    def __iter__(self) -> Iterator[int]:
        return iter((self._x, self._y))

    def __add__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x + rhs, self._y + rhs)
        elif isinstance(rhs, Int2Abstract):
            return self.static_class(self._x + rhs._x, self._y + rhs._y)
        else:
            raise NotImplementedError()

    def __sub__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x - rhs, self._y - rhs)
        elif isinstance(rhs, Int2Abstract):
            return self.static_class(self._x - rhs._x, self._y - rhs._y)
        else:
            raise NotImplementedError()

    def __mul__(self, rhs:int | float | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x * rhs, self._y * rhs)
        elif isinstance(rhs, float):
            return self.static_class(int(self._x * rhs), int(self._y * rhs))
        elif isinstance(rhs, Int2Abstract):
            return self.static_class(self._x * rhs._x, self._y * rhs._y)
        else:
            raise NotImplementedError()

    def __truediv__(self, rhs:int | float | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x / rhs, self._y / rhs)
        elif isinstance(rhs, float):
            return self.static_class(float(self._x / rhs), float(self._y / rhs))
        elif isinstance(rhs, Int2Abstract):
            return self.static_class(self._x / rhs._x, self._y / rhs._y)
        else:
            raise NotImplementedError()

    def __floordiv__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            return self.static_class(self._x // rhs, self._y // rhs)
        elif isinstance(rhs, Int2Abstract):
            return self.static_class(self._x // rhs._x, self._y // rhs._y)
        else:
            raise NotImplementedError()

    def __iadd__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            self._x += rhs
            self._y += rhs
        elif isinstance(rhs, Int2Abstract):
            self._x += rhs._x
            self._y += rhs._y
        else:
            raise NotImplementedError()
        return self

    def __isub__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            self._x -= rhs
            self._y -= rhs
        elif isinstance(rhs, Int2Abstract):
            self._x -= rhs._x
            self._y -= rhs._y
        else:
            raise NotImplementedError()
        return self

    def __imul__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            self._x *= rhs
            self._y *= rhs
        elif isinstance(rhs, Int2Abstract):
            self._x *= rhs._x
            self._y *= rhs._y
        else:
            raise NotImplementedError()
        return self

    def __ifloordiv__(self, rhs:int | Self) -> Self:
        if isinstance(rhs, int):
            self._x //= rhs
            self._y //= rhs
        elif isinstance(rhs, Int2Abstract):
            self._x //= rhs._x
            self._y //= rhs._y
        else:
            raise NotImplementedError()
        return self

    def __pos__(self) -> Self:
        return self.static_class(+self._x, +self._y)

    def __neg__(self) -> Self:
        return self.static_class(-self._x, -self._y)

    def is_zero(self) -> bool:
        """ゼロ値判定

        Returns:
            bool: 全要素がゼロ値の場合は True を返す
        """
        return self._x == 0 and self._y == 0

    @classmethod
    def max(cls, lhs:Self, rhs:Self) -> Self:
        return cls(max(lhs._x, rhs._x), max(lhs._y, rhs._y))

    @classmethod
    def min(cls, lhs:Self, rhs:Self) -> Self:
        return cls(min(lhs._x, rhs._x), min(lhs._y, rhs._y))

    @classmethod
    def zero(cls) -> Self:
        return cls(0, 0)

    @classmethod
    def one(cls) -> Self:
        return cls(1, 1)

    @classmethod
    def fill(cls, value:int) -> Self:
        return cls(value, value)
