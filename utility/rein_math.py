from typing import TypeVar


__all__ = [
    "clamp",
    "saturate",
    "lerp",
]


FloatOrInt = TypeVar("FloatOrInt", float, int)


def clamp(value:FloatOrInt, minimum:FloatOrInt, maximum:FloatOrInt) -> FloatOrInt:
    """指定した値を、指定した最小値と最大値の範囲にクランプします。

    Args:
        value (FloatOrInt): クランプする値
        minimum (FloatOrInt): 指定された最小範囲
        maximum (FloatOrInt): 指定した最大範囲

    Returns:
        FloatOrInt: クランプされた値
    """
    return max(min(value, maximum), minimum)


def saturate(value:FloatOrInt) -> FloatOrInt:
    """0-1クランプ

    Args:
        value (FloatOrInt): クランプする値

    Returns:
        float: クランプされた値
    """
    if isinstance(value, int):
        return clamp(value, 0, 1)
    elif isinstance(value, float):
        return clamp(value, 0.0, 1.0)
    else:
        assert False, "not support type."


def lerp(a:FloatOrInt, b:FloatOrInt, t:float) -> FloatOrInt:
    """線形補間

    Args:
        a (FloatOrInt): 開始値
        b (FloatOrInt): 終了値
        t (float): 補間値

    Returns:
        FloatOrInt: 補間された値
    """
    return (1.0 - t) * a + t * b
