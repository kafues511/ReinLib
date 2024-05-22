from typing import Union, Iterator, Self, Optional, ClassVar, TypeVar
from dataclasses import dataclass

from reinlib.types.rein_float4_abc import Float4Abstract


__all__ = [
    "Float4",
]


@dataclass
class Float4(Float4Abstract):
    def __init__(
        self,
        x:float,
        y:float,
        z:float,
        w:float,
    ) -> None:
        super().__init__(x, y, z, w)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "Float4":
        """_summary_

        Returns:
            Float4: _description_
        """
        return Float4(*args, **kwargs)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, new_value:float) -> None:
        self._x = new_value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, new_value:float) -> None:
        self._y = new_value

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, new_value:float) -> None:
        self._z = new_value

    @property
    def w(self) -> float:
        return self._w

    @w.setter
    def w(self, new_value:float) -> None:
        self._w = new_value
