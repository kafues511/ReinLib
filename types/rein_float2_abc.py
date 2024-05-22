import math
from typing import Iterator, Self
from dataclasses import dataclass
from abc import ABC, abstractmethod

from reinlib.utility.rein_math import pow2


__all__ = [
    "Float2Abstract",
]


@dataclass
class Float2Abstract(ABC):
    _x:float = 0.0
    _y:float = 0.0

    def __post_init__(self) -> None:
        assert isinstance(self._x, float), f"Float2Abstract._x only supports float type, the input type was {self._x}."
        assert isinstance(self._y, float), f"Float2Abstract._y only supports float type, the input type was {self._y}."

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

    def __truediv__(self, rhs:float | Self) -> Self:
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

    def __itruediv__(self, rhs:float | Self) -> Self:
        if isinstance(rhs, float):
            self._x /= rhs
            self._y /= rhs
        elif isinstance(rhs, Float2Abstract):
            self._x /= rhs._x
            self._y /= rhs._y
        else:
            raise NotImplementedError()
        return self

    def distance(self, rhs:Self) -> float:
        """2点間のユークリッド距離を計算

        Args:
            rhs (Self): _description_

        Returns:
            float: ユークリッド距離
        """
        return math.sqrt(pow2(self._x - rhs._x) + pow2(self._y - rhs._y))

    @staticmethod
    def dot(lhs:"Float2Abstract", rhs:"Float2Abstract") -> float:
        """内積解

        Args:
            lhs (Float2Abstract): 左辺
            rhs (Float2Abstract): 右辺

        Returns:
            float: 内積解
        """
        return lhs._x * rhs._x + lhs._y * rhs._y

    def magnitude(self) -> float:
        """ベクトルの大きさ（ノルム）を計算

        Args:
            lhs (Float2Abstract): _description_

        Returns:
            float: ベクトルの大きさ（ノルム）
        """
        return math.sqrt(self._x * self._x + self._y * self._y)

    @staticmethod
    def nearest(a:"Float2Abstract", b:"Float2Abstract", p:"Float2Abstract") -> float:
        """辺ABと点Pの最短距離を計算

        Args:
            a (Float2Abstract): 点A (辺AB)
            b (Float2Abstract): 点B (辺AB)
            p (Float2Abstract): 点P

        Returns:
            float: 辺ABと点Pの最短距離
        """
        ap = p - a
        ab = b - a
        ba = a - b
        bp = p - b

        if Float2Abstract.dot(ap, ab) < 0.0:
            return ap.magnitude()
        elif Float2Abstract.dot(bp, ba) < 0.0:
            return (p - b).magnitude()
        else:
            ai_norm = Float2Abstract.dot(ap, ab) / max(1.0e-6, ab.magnitude())
            neighbor_point = a + ab / max(1.0e-6, ab.magnitude()) * ai_norm
            return (p - neighbor_point).magnitude()

    @classmethod
    def zero(cls) -> Self:
        return cls(0.0, 0.0)
