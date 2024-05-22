from dataclasses import dataclass
import random
from typing import Self

from reinlib.types.rein_int3 import Int3


__all__ = [
    "Range",
]


@dataclass
class Range(Int3):
    def __init__(self, start:int, stop:int, step:int = 1) -> None:
        super().__init__(start, stop, step)

    @property
    def start(self) -> int:
        return self.x

    @property
    def stop(self) -> int:
        return self.y

    @property
    def step(self) -> int:
        return self.z

    def is_valid(self) -> bool:
        """有効性を取得

        Returns:
            bool: 無効な場合は False を返します。
        """
        return self.start != (self.stop - 1)

    def __call__(self) -> int:
        """call random.randrange

        Returns:
            int: 指定された範囲 [start, stop, step] からランダムに値を選出
        """
        return random.randrange(*self) if self.is_valid() else self.start

    def with_start(self, start:int) -> Self:
        """startを置換

        Args:
            start (int): 開始値

        Returns:
            Self: Range
        """
        return Range(start, self.stop, self.step)
