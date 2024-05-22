from dataclasses import dataclass

from reinlib.types.rein_float2_abc import Float2Abstract


__all__ = [
    "Float2",
]


@dataclass
class Float2(Float2Abstract):
    def __init__(
        self,
        x:float,
        y:float,
    ) -> None:
        super().__init__(x, y)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "Float2":
        """_summary_

        Returns:
            Float2: _description_
        """
        return Float2(*args, **kwargs)

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

    @classmethod
    def from_int(cls, x:int, y:int) -> "Float2":
        """int2からfloat2を作成

        暗黙的な変換を許容していないため明示的な呼び出しです。

        Args:
            x (int): _description_
            y (int): _description_

        Returns:
            Float2: _description_
        """
        return cls(float(x), float(y))
