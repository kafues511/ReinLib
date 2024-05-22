from dataclasses import dataclass

from reinlib.types.rein_int3_abc import Int3Abstract


__all__ = [
    "Int3",
]


@dataclass
class Int3(Int3Abstract):
    def __init__(
        self,
        x:int,
        y:int,
        z:int,
    ) -> None:
        super().__init__(x, y, z)

    @classmethod
    def static_class(cls, *args, **kwargs) -> "Int3":
        """_summary_

        Returns:
            Int3: _description_
        """
        return Int3(*args, **kwargs)

    @property
    def x(self) -> int:
        """x座標を取得

        Returns:
            int: x座標
        """
        return self._x

    @x.setter
    def x(self, new_value:int) -> None:
        """x座標をセット

        Returns:
            int: x座標
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

        Returns:
            int: y座標
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

        Returns:
            int: z座標
        """
        self._z = new_value
