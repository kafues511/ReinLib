from dataclasses import dataclass

from reinlib.types.rein_int4_abc import Int4Abstract


__all__ = [
    "BoundingBox",
]


@dataclass
class BoundingBox(Int4Abstract):
    def __init__(
        self,
        xmin:int,
        ymin:int,
        xmax:int,
        ymax:int,
    ) -> None:
        super().__init__(xmin, ymin, xmax, ymax)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "BoundingBox":
        """_summary_

        Returns:
            BoundingBox: _description_
        """
        return BoundingBox(*args, **kwargs)

    @property
    def xmin(self) -> int:
        """左上のx座標を取得

        Returns:
            int: 左上のX座標
        """
        return self._x

    @xmin.setter
    def xmin(self, new_value:int) -> None:
        """左上のx座標をセット

        Args:
            new_value (int): 左上のx座標
        """
        self._x = new_value

    @property
    def ymin(self) -> int:
        """左上のy座標を取得

        Returns:
            int: 左上のy座標
        """
        return self._y

    @ymin.setter
    def ymin(self, new_value:int) -> None:
        """左上のy座標をセット

        Args:
            new_value (int): 左上のy座標
        """
        self._y = new_value

    @property
    def xmax(self) -> int:
        """右下のx座標を取得

        Returns:
            int: 右下のx座標
        """
        return self._z

    @xmax.setter
    def xmax(self, new_value:int) -> None:
        """右下のx座標をセット

        Args:
            new_value (int): 右下のx座標
        """
        self._z = new_value

    @property
    def ymax(self) -> int:
        """右下のy座標を取得

        Returns:
            int: 右下のy座標
        """
        return self._w

    @ymax.setter
    def ymax(self, new_value:int) -> None:
        """右下のy座標をセット

        Args:
            new_value (int): 右下のy座標
        """
        self._w = new_value

    @property
    def width(self) -> int:
        """横幅を取得

        Returns:
            int: 横幅
        """
        return self.xmax - self.xmin

    @property
    def height(self) -> int:
        """縦幅を取得

        Returns:
            int: 縦幅
        """
        return self.ymax - self.ymin

    @property
    def w(self) -> int:
        """横幅を取得

        Returns:
            int: 横幅
        """
        return self.width

    @property
    def h(self) -> int:
        """縦幅を取得

        Returns:
            int: 縦幅
        """
        return self.height

    @property
    def wh(self) -> tuple[int, int]:
        """_summary_

        Returns:
            tuple[int, int]: _description_
        """
        return self.w, self.h

    @property
    def hw(self) -> tuple[int, int]:
        """_summary_

        Returns:
            tuple[int, int]: _description_
        """
        return self.h, self.w
