from dataclasses import dataclass

from reinlib.types.rein_int2_abc import Int2Abstract


__all__ = [
    "Size2D",
]


@dataclass
class Size2D(Int2Abstract):
    def __init__(
        self,
        width:int,
        height:int,
    ) -> None:
        super().__init__(width, height)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "Size2D":
        """_summary_

        Returns:
            Size2D: _description_
        """
        return Size2D(*args, **kwargs)

    @property
    def width(self) -> int:
        return self._x

    @width.setter
    def width(self, new_value:int) -> None:
        self._x = new_value

    @property
    def height(self) -> int:
        return self._y

    @height.setter
    def height(self, new_value:int) -> None:
        self._y = new_value

    @property
    def w(self) -> int:
        return self.width

    @w.setter
    def w(self, new_value:int) -> None:
        self.width = new_value

    @property
    def h(self) -> int:
        return self.height

    @h.setter
    def h(self, new_value:int) -> None:
        self.height = new_value

    @property
    def wh(self) -> tuple[int, int]:
        return self.w, self.h

    @wh.setter
    def wh(self, new_value:tuple[int, int]) -> None:
        self.width, self.height = new_value

    @property
    def hw(self) -> tuple[int, int]:
        return self.height, self.width

    @hw.setter
    def hw(self, new_value:tuple[int, int]) -> None:
        self.height, self.width = new_value
