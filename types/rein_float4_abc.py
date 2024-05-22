from typing import Iterator, Self
from dataclasses import dataclass
from abc import ABC, abstractmethod


__all__ = [
    "Float4Abstract",
]


@dataclass
class Float4Abstract(ABC):
    _x:float = 0.0
    _y:float = 0.0
    _z:float = 0.0
    _w:float = 0.0

    def __post_init__(self) -> None:
        assert isinstance(self._x, float), f"Float4Abstract._x only supports float type, the input type was {self._x}."
        assert isinstance(self._y, float), f"Float4Abstract._y only supports float type, the input type was {self._y}."
        assert isinstance(self._z, float), f"Float4Abstract._z only supports float type, the input type was {self._z}."
        assert isinstance(self._w, float), f"Float4Abstract._w only supports float type, the input type was {self._w}."

    @classmethod
    @abstractmethod
    def static_class(cls, *args, **kwargs) -> "Float4Abstract":
        """_summary_

        Returns:
            Float4Abstract: _description_
        """
        return Float4Abstract(*args, **kwargs)

    def __iter__(self) -> Iterator[float]:
        return iter((self._x, self._y, self._z, self._w))

    def __add__(self, rhs:float | int | Self) -> Self:
        if isinstance(rhs, (float, int)):
            return self.static_class(self._x + rhs, self._y + rhs, self._z + rhs, self._w + rhs)
        elif isinstance(rhs, Float4Abstract):
            return self.static_class(self._x + rhs._x, self._y + rhs._y, self._z + rhs._z, self._w + rhs._w)
        else:
            raise NotImplementedError()

    def __sub__(self, rhs:float | int | Self) -> Self:
        if isinstance(rhs, (float, int)):
            return self.static_class(self._x - rhs, self._y - rhs, self._z - rhs, self._w - rhs)
        elif isinstance(rhs, Float4Abstract):
            return self.static_class(self._x - rhs._x, self._y - rhs._y, self._z - rhs._z, self._w - rhs._w)
        else:
            raise NotImplementedError()

    def __mul__(self, rhs:float | int | Self) -> Self:
        if isinstance(rhs, (float, int)):
            return self.static_class(self._x * rhs, self._y * rhs, self._z * rhs, self._w * rhs)
        elif isinstance(rhs, Float4Abstract):
            return self.static_class(self._x * rhs._x, self._y * rhs._y, self._z * rhs._z, self._w * rhs._w)
        else:
            raise NotImplementedError()

    def __truediv__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            return self.static_class(self._x / rhs, self._y / rhs, self._z / rhs, self._w / rhs)
        elif isinstance(rhs, Float4Abstract):
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
        return cls(*[float(val) for val in value.split(sep)])

    @classmethod
    def from_int(cls, x:int, y:int, z:int, w:int) -> Self:
        """_summary_

        Args:
            x (int): _description_
            y (int): _description_
            z (int): _description_
            w (int): _description_

        Returns:
            Self: _description_
        """
        return cls(float(x), float(y), float(z), float(w))

    @classmethod
    def zero(cls) -> Self:
        """_summary_

        Returns:
            Self: _description_
        """
        return cls(0.0, 0.0, 0.0, 0.0)
