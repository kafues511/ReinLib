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

    @property
    def wslice(self) -> slice:
        """xmin ~ xmaxのsliceを取得

        Returns:
            slice: xmin ~ xmaxのslice
        """
        return slice(self.xmin, self.xmax, 1)

    @property
    def hslice(self) -> slice:
        """ymin ~ ymaxのsliceを取得

        Returns:
            slice: ymin ~ ymaxのslice
        """
        return slice(self.ymin, self.ymax, 1)

    @property
    def whslice(self) -> tuple[slice, slice]:
        """xmin ~ xmax, ymin ~ ymaxのsliceを取得

        Returns:
            tuple[slice, slice]: xmin ~ xmax, ymin ~ ymaxのslice
        """
        return self.wslice, self.hslice

    @property
    def hwslice(self) -> tuple[slice, slice]:
        """ymin ~ ymax, xmin ~ xmaxのsliceを取得

        Returns:
            tuple[slice, slice]: ymin ~ ymax, xmin ~ xmaxのslice
        """
        return self.hslice, self.wslice

    @property
    def center(self) -> tuple[int, int]:
        """中心座標を取得

        Returns:
            tuple[int, int]: 中心座標
        """
        return self.xmin + self.width//2, self.ymin + self.height//2

    @property
    def xymin(self) -> tuple[int, int]:
        """xminとyminを取得

        Returns:
            tuple[int, int]: xminとymin
        """
        return self._x, self._y

    @property
    def xymax(self) -> tuple[int, int]:
        """xmaxとymaxを取得

        Returns:
            tuple[int, int]: xmaxとymax
        """
        return self._z, self._w

    def collision(self, rhs:"BoundingBox") -> bool:
        return self.xmin <= rhs.xmax and rhs.xmin <= self.xmax and self.ymin <= rhs.ymax and rhs.ymin <= self.ymax

    def collisions(self, rhs:list["BoundingBox"]) -> bool:
        for bbox in rhs:
            if self.collision(bbox):
                return True
        return False

    @property
    def area(self) -> int:
        """バウンディングボックスの面積を取得

        Returns:
            int: バウンディングボックスの面積
        """
        return self.width * self.height

    @classmethod
    def test(cls, bboxes:list["BoundingBox"]) -> "BoundingBox":
        if len(bboxes) == 0:
            return cls.zero()

        bbox = cls(*bboxes[0])

        for xmin, ymin, xmax, ymax in bboxes[1:]:
            bbox.xmin = min(bbox.xmin, xmin)
            bbox.ymin = min(bbox.ymin, ymin)
            bbox.xmax = max(bbox.xmax, xmax)
            bbox.ymax = max(bbox.ymax, ymax)

        return bbox
