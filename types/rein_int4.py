from typing import Union, Iterator, Self
from dataclasses import dataclass


__all__ = [
    "Int4",
]


@dataclass
class Int4:
    x:int = 0
    y:int = 0
    z:int = 0
    w:int = 0

    @property
    def xyzw(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.z, self.w

    @property
    def xy(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def zw(self) -> tuple[int, int]:
        return self.z, self.w

    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y, self.z, self.w))

    def __add__(self, rhs:Union[int, float, tuple[int, int, int, int], list[int], Self]) -> Self:
        if isinstance(rhs, (tuple, list)):
            assert len(rhs) == 4, "not match lenght"
            return Int4(self.x + rhs[0], self.y + rhs[1], self.z + rhs[2], self.w + rhs[3])
        elif isinstance(rhs, int):
            return Int4(self.x + rhs, self.y + rhs, self.z + rhs, self.w + rhs)
        elif isinstance(rhs, float):
            return Int4(int(self.x + rhs), int(self.y + rhs), int(self.z + rhs), int(self.w + rhs))
        elif isinstance(rhs, Int4):
            return Int4(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z, self.w + rhs.w)
        else:
            assert False, "not support types"

    def __sub__(self, rhs:Union[int, float, tuple[int, int, int, int], list[int], Self]) -> Self:
        if isinstance(rhs, (tuple, list)):
            assert len(rhs) == 4, "not match lenght"
            return Int4(self.x - rhs[0], self.y - rhs[1], self.z - rhs[2], self.w - rhs[3])
        elif isinstance(rhs, int):
            return Int4(self.x - rhs, self.y - rhs, self.z - rhs, self.w - rhs)
        elif isinstance(rhs, float):
            return Int4(int(self.x - rhs), int(self.y - rhs), int(self.z - rhs), int(self.w - rhs))
        elif isinstance(rhs, Int4):
            return Int4(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z, self.w - rhs.w)
        else:
            assert False, "not support types"

    def __mul__(self, rhs:Union[int, float, tuple[int, int, int, int], list[int], Self]) -> Self:
        if isinstance(rhs, (tuple, list)):
            assert len(rhs) == 4, "not match lenght"
            return Int4(self.x * rhs[0], self.y * rhs[1], self.z * rhs[2], self.w * rhs[3])
        elif isinstance(rhs, int):
            return Int4(self.x * rhs, self.y * rhs, self.z * rhs, self.w * rhs)
        elif isinstance(rhs, float):
            return Int4(int(self.x * rhs), int(self.y * rhs), int(self.z * rhs), int(self.w * rhs))
        elif isinstance(rhs, Int4):
            return Int4(self.x * rhs.x, self.y * rhs.y, self.z * rhs.z, self.w * rhs.w)
        else:
            assert False, "not support types"

    def __floordiv__(self, rhs:Union[int, float, tuple[int, int], list[int], Self]) -> Self:
        if isinstance(rhs, (tuple, list)):
            assert len(rhs) == 4, "not match lenght"
            return Int4(self.x//rhs[0], self.y//rhs[1])
        elif isinstance(rhs, int):
            return Int4(self.x//rhs, self.y//rhs, self.z//rhs, self.w//rhs)
        elif isinstance(rhs, float):
            return Int4(self.x//int(rhs), self.y//int(rhs), self.z//int(rhs), self.w//int(rhs))
        elif isinstance(rhs, Int4):
            return Int4(self.x//rhs.x, self.y//rhs.y, self.z//rhs.z, self.w//rhs.w)
        else:
            assert False, "not support types"

    def __iadd__(self, rhs:Union[int, float, tuple[int, int, int, int], list[int], Self]) -> Self:
        if isinstance(rhs, (tuple, list)):
            assert len(rhs) == 4, "not match lenght"
            self.x += rhs[0]
            self.y += rhs[1]
            self.z += rhs[2]
            self.w += rhs[3]
        elif isinstance(rhs, int):
            self.x += rhs
            self.y += rhs
            self.z += rhs
            self.w += rhs
        elif isinstance(rhs, float):
            self.x += int(rhs)
            self.y += int(rhs)
            self.z += int(rhs)
            self.w += int(rhs)
        elif isinstance(rhs, Int4):
            self.x += rhs.x
            self.y += rhs.y
            self.z += rhs.z
            self.w += rhs.w
        else:
            assert False, "not support types"
        return self

    def __isub__(self, rhs:Union[int, float, tuple[int, int, int, int], list[int], Self]) -> Self:
        if isinstance(rhs, (tuple, list)):
            assert len(rhs) == 4, "not match lenght"
            self.x -= rhs[0]
            self.y -= rhs[1]
            self.z -= rhs[2]
            self.w -= rhs[3]
        elif isinstance(rhs, int):
            self.x -= rhs
            self.y -= rhs
            self.z -= rhs
            self.w -= rhs
        elif isinstance(rhs, float):
            self.x -= int(rhs)
            self.y -= int(rhs)
            self.z -= int(rhs)
            self.w -= int(rhs)
        elif isinstance(rhs, Int4):
            self.x -= rhs.x
            self.y -= rhs.y
            self.z -= rhs.z
            self.w -= rhs.w
        else:
            assert False, "not support types"
        return self

    def __ifloordiv__(self, rhs:Union[int, float, tuple[int, int, int, int], list[int], Self]) -> Self:
        if isinstance(rhs, (tuple, list)):
            assert len(rhs) == 4, "not match lenght"
            self.x //= rhs[0]
            self.y //= rhs[1]
            self.z //= rhs[2]
            self.w //= rhs[3]
        elif isinstance(rhs, int):
            self.x //= rhs
            self.y //= rhs
            self.z //= rhs
            self.w //= rhs
        elif isinstance(rhs, float):
            self.x //= int(rhs)
            self.y //= int(rhs)
            self.z //= int(rhs)
            self.w //= int(rhs)
        elif isinstance(rhs, Int4):
            self.x //= rhs.x
            self.y //= rhs.y
            self.z //= rhs.z
            self.w //= rhs.w
        else:
            assert False, "not support types"
        return self
