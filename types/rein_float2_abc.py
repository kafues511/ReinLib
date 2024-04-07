from typing import Iterator, Self
from dataclasses import dataclass
from abc import ABC, abstractmethod


__all__ = [
    "Float2Abstract",
]


@dataclass
class Float2Abstract(ABC):
    _x:float = 0.0
    _y:float = 0.0

    def __post_init__(self) -> None:
        assert isinstance(self._x, float), f"{self}.x only supports float type, the input type was {self._x}."
        assert isinstance(self._y, float), f"{self}.y only supports float type, the input type was {self._y}."

    @classmethod
    @abstractmethod
    def static_class(cls, *args, **kwargs) -> "Float2Abstract":
        """_summary_

        Returns:
            Float2Abstract: _description_
        """
        return Float2Abstract(*args, **kwargs)

    def __iter__(self) -> Iterator[float]:
        return iter((self._x, self._y))

    def __add__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            return self.static_class(self._x + rhs, self._y + rhs)
        elif isinstance(rhs, Float2Abstract):
            return self.static_class(self._x + rhs._x, self._y + rhs._y)
        else:
            raise NotImplementedError()

    def __sub__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            return self.static_class(self._x - rhs, self._y - rhs)
        elif isinstance(rhs, Float2Abstract):
            return self.static_class(self._x - rhs._x, self._y - rhs._y)
        else:
            raise NotImplementedError()

    def __mul__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            return self.static_class(self._x * rhs, self._y * rhs)
        elif isinstance(rhs, Float2Abstract):
            return self.static_class(self._x * rhs._x, self._y * rhs._y)
        else:
            raise NotImplementedError()

    def __div__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            return self.static_class(self._x / rhs, self._y / rhs)
        elif isinstance(rhs, Float2Abstract):
            return self.static_class(self._x / rhs._x, self._y / rhs._y)
        else:
            raise NotImplementedError()

    def __iadd__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            self._x += rhs
            self._y += rhs
        elif isinstance(rhs, Float2Abstract):
            self._x += rhs._x
            self._y += rhs._y
        else:
            raise NotImplementedError()
        return self

    def __isub__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            self._x -= rhs
            self._y -= rhs
        elif isinstance(rhs, Float2Abstract):
            self._x -= rhs._x
            self._y -= rhs._y
        else:
            raise NotImplementedError()
        return self

    def __imul__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            self._x *= rhs
            self._y *= rhs
        elif isinstance(rhs, Float2Abstract):
            self._x *= rhs._x
            self._y *= rhs._y
        else:
            raise NotImplementedError()
        return self

    @classmethod
    def zero(cls) -> Self:
        return cls(0.0, 0.0)
