from dataclasses import dataclass

from reinlib.types.rein_float2_abc import Float2Abstract


__all__ = [
    "FloatMinMax",
]


@dataclass
class FloatMinMax(Float2Abstract):
    def __init__(
        self,
        minimum:float,
        maximum:float,
    ) -> None:
        super().__init__(minimum, maximum)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "FloatMinMax":
        """_summary_

        Returns:
            FloatMinMax: _description_
        """
        return FloatMinMax(*args, **kwargs)

    @property
    def minimum(self) -> float:
        """最小値を取得

        Returns:
            float: 最小値
        """
        return self._x

    @minimum.setter
    def minimum(self, new_value:float) -> None:
        """最小値をセット

        Args:
            new_value (float): 最小値
        """
        self._x = new_value

    @property
    def maximum(self) -> float:
        """最大値を取得

        Returns:
            float: 最大値
        """
        return self._y

    @maximum.setter
    def maximum(self, new_value:float) -> None:
        """最大値をセット

        Args:
            new_value (float): 最大値
        """
        self._y = new_value
