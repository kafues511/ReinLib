from dataclasses import dataclass

from reinlib.types.rein_int3_abc import Int3Abstract


__all__ = [
    "HSV",
]


@dataclass
class HSV(Int3Abstract):
    """HSV/HSB色空間
    """
    def __init__(
        self,
        hue:int,
        saturation:int,
        value:int,
    ) -> None:
        """コンストラクタ

        Args:
            hue (int): 色相
            saturation (int): 彩度
            value (int): 明度
        """
        super().__init__(hue, saturation, value)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "HSV":
        """_summary_

        Returns:
            HSV: _description_
        """
        return HSV(*args, **kwargs)

    @property
    def hue(self) -> int:
        """色相を取得

        Returns:
            int: 色相
        """
        return self._x

    @hue.setter
    def hue(self, new_value:int) -> None:
        """色相をセット

        Args:
            new_value (int): 色相
        """
        self._x = new_value

    @property
    def saturation(self) -> int:
        """彩度を取得

        Returns:
            int: 彩度
        """
        return self._y

    @saturation.setter
    def saturation(self, new_value:int) -> None:
        """彩度をセット

        Args:
            new_value (int): 彩度
        """
        self._y = new_value

    @property
    def chroma(self) -> int:
        """彩度を取得

        Returns:
            int: 彩度
        """
        return self._y

    @chroma.setter
    def chroma(self, new_value:int) -> None:
        """彩度をセット

        Args:
            new_value (int): 彩度
        """
        self._y = new_value

    @property
    def value(self) -> int:
        """明度を取得

        Returns:
            int: 明度
        """
        return self._z

    @value.setter
    def value(self, new_value:int) -> None:
        """明度をセット

        Args:
            new_value (int): 明度
        """
        self._z = new_value

    @property
    def brightness(self) -> int:
        """明度を取得

        Returns:
            int: 明度
        """
        return self._z

    @brightness.setter
    def brightness(self, new_value:int) -> None:
        """明度をセット

        Args:
            new_value (int): 明度
        """
        self._z = new_value

    @property
    def h(self) -> int:
        """色相を取得

        Returns:
            int: 色相
        """
        return self.hue

    @h.setter
    def h(self, new_value:int) -> None:
        """色相をセット

        Args:
            new_value (int): 色相
        """
        self.hue = new_value

    @property
    def s(self) -> int:
        """彩度を取得

        Returns:
            int: 彩度
        """
        return self.saturation

    @s.setter
    def s(self, new_value:int) -> None:
        """彩度をセット

        Args:
            new_value (int): 彩度
        """
        self.saturation = new_value

    @property
    def c(self) -> int:
        """彩度を取得

        Returns:
            int: 彩度
        """
        return self.chroma

    @c.setter
    def c(self, new_value:int) -> None:
        """彩度をセット

        Args:
            new_value (int): 彩度
        """
        self.chroma = new_value

    @property
    def v(self) -> int:
        """明度を取得

        Returns:
            int: 明度
        """
        return self.value

    @v.setter
    def v(self, new_value:int) -> None:
        """明度をセット

        Args:
            new_value (int): 明度
        """
        self.value = new_value

    @property
    def b(self) -> int:
        """明度を取得

        Returns:
            int: 明度
        """
        return self.brightness

    @b.setter
    def b(self, new_value:int) -> None:
        """明度をセット

        Args:
            new_value (int): 明度
        """
        self.brightness = new_value
