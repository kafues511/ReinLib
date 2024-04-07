from enum import IntEnum, auto


__all__ = [
    "BlendMode",
]


class BlendMode(IntEnum):
    """ブレンドモード
    """
    # 標準・通常
    NORMAL = auto()
    # 差の絶対値
    DIFFERENCE = auto()

    @staticmethod
    def from_str(blend_mode:str) -> "BlendMode":
        for value in BlendMode:
            if str(value) == blend_mode:
                return value
        assert False, "not support."

    @staticmethod
    def values() -> tuple[str, ...]:
        return tuple([str(val) for val in BlendMode])

    def __str__(self) -> str:
        if self is BlendMode.NORMAL:
            return "Normal"
        elif self is BlendMode.DIFFERENCE:
            return "Difference"
        else:
            assert False, "not support."
