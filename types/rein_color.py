from dataclasses import dataclass
from typing import Self

from reinlib.types.rein_int4_abc import Int4Abstract
from reinlib.types.rein_hsv import HSV
from reinlib.utility.rein_math import clamp


__all__ = [
    "Color",
]


@dataclass
class Color(Int4Abstract):
    def __init__(
        self,
        red:int,
        green:int,
        blue:int,
        alpha:int,
    ) -> None:
        """コンストラクタ

        Args:
            red (int): 赤成分
            green (int): 緑成分
            blue (int): 青成分
            alpha (int): 透明度
        """
        super().__init__(red, green, blue, alpha)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "Color":
        """_summary_

        Returns:
            Color: _description_
        """
        return Color(*args, **kwargs)

    @property
    def red(self) -> int:
        """赤成分を取得

        Returns:
            int: 赤成分
        """
        return self._x

    @red.setter
    def red(self, new_value:int) -> None:
        """赤成分をセット

        Args:
            new_value (int): 赤成分
        """
        self._x = new_value

    @property
    def green(self) -> int:
        """緑成分を取得

        Returns:
            int: 緑成分
        """
        return self._y

    @green.setter
    def green(self, new_value:int) -> None:
        """緑成分をセット

        Args:
            new_value (int): 緑成分
        """
        self._y = new_value

    @property
    def blue(self) -> int:
        """青成分を取得

        Returns:
            int: 青成分
        """
        return self._z

    @blue.setter
    def blue(self, new_value:int) -> None:
        """青成分をセット

        Args:
            new_value (int): 青成分
        """
        self._z = new_value

    @property
    def alpha(self) -> int:
        """透明度を取得

        Returns:
            int: 透明度
        """
        return self._w

    @alpha.setter
    def alpha(self, new_value:int) -> None:
        """透明度をセット

        Args:
            new_value (int): 透明度
        """
        self._w = new_value

    @property
    def r(self) -> int:
        """赤成分を取得

        Returns:
            int: 赤成分
        """
        return self.red

    @r.setter
    def r(self, new_value:int) -> None:
        """赤成分をセット

        Args:
            new_value (int): 赤成分
        """
        self.red = new_value

    @property
    def g(self) -> int:
        """緑成分を取得

        Returns:
            int: 緑成分
        """
        return self.green

    @g.setter
    def g(self, new_value:int) -> None:
        """緑成分をセット

        Args:
            new_value (int): 緑成分
        """
        self.green = new_value

    @property
    def b(self) -> int:
        """青成分を取得

        Returns:
            int: 青成分
        """
        return self.blue

    @b.setter
    def b(self, new_value:int) -> None:
        """青成分をセット

        Args:
            new_value (int): 青成分
        """
        self.blue = new_value

    @property
    def a(self) -> int:
        """透明度を取得

        Returns:
            int: 透明度
        """
        return self.alpha

    @a.setter
    def a(self, new_value:int) -> None:
        """透明度をセット

        Args:
            new_value (int): 透明度
        """
        self.alpha = new_value

    @property
    def grayscale(self) -> int:
        """グレースケールを取得

        内部的にはRチャンネルを指します。

        Returns:
            int: グレースケール
        """
        return self.red

    @grayscale.setter
    def grayscale(self, new_value:int) -> None:
        """グレースケールをセット

        内部的にはRチャンネルを指します。

        Args:
            new_value (int): グレースケール
        """
        self.red = new_value

    @property
    def rgb(self) -> tuple[int, int, int]:
        """RGB配置で取得

        Returns:
            tuple[int, int, int]: RGB
        """
        return self.red, self.green, self.blue

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """RGBA配置で取得

        Returns:
            tuple[int, int, int, int]: RGBA
        """
        return self.red, self.green, self.blue, self.alpha

    @property
    def bgr(self) -> tuple[int, int, int]:
        """BGR配置で取得

        Returns:
            tuple[int, int, int]: BGR配置
        """
        return self.b, self.g, self.r

    @property
    def bgra(self) -> tuple[int, int, int, int]:
        """BGRA配置で取得

        Returns:
            tuple[int, int, int, int]: BGRA配置
        """
        return self.b, self.g, self.r, self.a

    @classmethod
    def white(cls) -> Self:
        return cls(255, 255, 255, 255)

    @classmethod
    def black(cls) -> Self:
        return cls(0, 0, 0, 255)

    @classmethod
    def from_hsv(cls, hsv:HSV) -> Self:
        """HSVからColor

        Args:
            hsv (HSV): HSV色空間

        Returns:
            Self: Color
        """
        h, s, v = hsv

        h = clamp(h, 0, 360)
        s = s * 0.01
        v = v * 0.01

        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if 60 <= h < 120:
            r, g, b = x, c, 0.0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        elif 300 <= h < 360:
            r, g, b = c, 0, x
        else:
            r, g, b = c, x, 0.0

        return cls(int((r + m) * 255), int((g + m) * 255), int((b + m) * 255), 255)
