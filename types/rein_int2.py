from dataclasses import dataclass

from reinlib.types.rein_int2_abc import Int2Abstract


__all__ = [
    "Int2",
]


@dataclass
class Int2(Int2Abstract):
    def __init__(
        self,
        x:int,
        y:int,
    ) -> None:
        super().__init__(x, y)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "Int2":
        """_summary_

        Returns:
            Int2: _description_
        """
        return Int2(*args, **kwargs)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, new_value:int) -> None:
        self._x = new_value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, new_value:int) -> None:
        self._y = new_value

    @property
    def xy(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def yx(self) -> tuple[int, int]:
        return self.y, self.x
