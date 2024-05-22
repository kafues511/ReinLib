from enum import IntEnum, auto


__all__ = [
    "ColorMethod",
]


class ColorMethod(IntEnum):
    """色空間
    """
    # グレースケール
    GRAYSCALE = auto()
    # カラー
    COLOR = auto()
    # 透明度付き
    ALPHA = auto()
