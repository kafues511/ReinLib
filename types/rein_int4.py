from dataclasses import dataclass

from reinlib.types.rein_int4_abc import Int4Abstract


__all__ = [
    "Int4",
]


@dataclass
class Int4(Int4Abstract):
    def __init__(
        self,
        x:int,
        y:int,
        z:int,
        w:int,
    ) -> None:
        super().__init__(x, y, z, w)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "Int4":
        """_summary_

        Returns:
            Int4: _description_
        """
        return Int4(*args, **kwargs)

    @property
    def x(self) -> int:
        """x座標を取得

        Returns:
            int: X座標
        """
        return self._x

    @x.setter
    def x(self, new_value:int) -> None:
        """x座標をセット

        Args:
            new_value (int): x座標
        """
        self._x = new_value

    @property
    def y(self) -> int:
        """y座標を取得

        Returns:
            int: y座標
        """
        return self._y

    @y.setter
    def y(self, new_value:int) -> None:
        """y座標をセット

        Args:
            new_value (int): y座標
        """
        self._y = new_value

    @property
    def z(self) -> int:
        """z座標を取得

        Returns:
            int: z座標
        """
        return self._z

    @z.setter
    def z(self, new_value:int) -> None:
        """z座標をセット

        Args:
            new_value (int): z座標
        """
        self._z = new_value

    @property
    def w(self) -> int:
        """w座標を取得

        Returns:
            int: w座標
        """
        return self._w

    @w.setter
    def w(self, new_value:int) -> None:
        """w座標をセット

        Args:
            new_value (int): w座標
        """
        self._w = new_value
