from dataclasses import dataclass

from reinlib.types.rein_float4_abc import Float4Abstract


__all__ = [
    "FloatBoundingBox",
]


@dataclass
class FloatBoundingBox(Float4Abstract):
    def __init__(
        self,
        xmin:float,
        ymin:float,
        xmax:float,
        ymax:float,
    ) -> None:
        super().__init__(xmin, ymin, xmax, ymax)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "FloatBoundingBox":
        """_summary_

        Returns:
            FloatBoundingBox: _description_
        """
        return FloatBoundingBox(*args, **kwargs)

    @property
    def xmin(self) -> float:
        """左上のx座標を取得

        Returns:
            float: 左上のX座標
        """
        return self._x

    @xmin.setter
    def xmin(self, new_value:float) -> None:
        """左上のx座標をセット

        Args:
            new_value (float): 左上のx座標
        """
        self._x = new_value

    @property
    def ymin(self) -> float:
        """左上のy座標を取得

        Returns:
            float: 左上のy座標
        """
        return self._y

    @ymin.setter
    def ymin(self, new_value:float) -> None:
        """左上のy座標をセット

        Args:
            new_value (float): 左上のy座標
        """
        self._y = new_value

    @property
    def xmax(self) -> float:
        """右下のx座標を取得

        Returns:
            float: 右下のx座標
        """
        return self._z

    @xmax.setter
    def xmax(self, new_value:float) -> None:
        """右下のx座標をセット

        Args:
            new_value (float): 右下のx座標
        """
        self._z = new_value

    @property
    def ymax(self) -> float:
        """右下のy座標を取得

        Returns:
            float: 右下のy座標
        """
        return self._w

    @ymax.setter
    def ymax(self, new_value:float) -> None:
        """右下のy座標をセット

        Args:
            new_value (float): 右下のy座標
        """
        self._w = new_value

    @property
    def width(self) -> float:
        """横幅を取得

        Returns:
            float: 横幅
        """
        return self.xmax - self.xmin

    @property
    def height(self) -> float:
        """縦幅を取得

        Returns:
            float: 縦幅
        """
        return self.ymax - self.ymin

    @property
    def w(self) -> float:
        """横幅を取得

        Returns:
            float: 横幅
        """
        return self.width

    @property
    def h(self) -> float:
        """縦幅を取得

        Returns:
            float: 縦幅
        """
        return self.height
