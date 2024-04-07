from enum import IntEnum, auto


__all__ = [
    "AlphaBlendMode",
]


class AlphaBlendMode(IntEnum):
    """透明度のブレンドモード
    """
    # (src.rgb * src.a) + (dst.rgb * (1.0 - src.a))
    STRAIGHT = auto()
    # src.rgb + (dst.rgb * (1.0 - src.a))
    PREMULTIPLIED = auto()
