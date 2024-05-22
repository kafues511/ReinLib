from enum import IntEnum, auto


__all__ = [
    "StageType",
]


class StageType(IntEnum):
    """ステージの種類
    """
    TRAIN = auto()
    VALID = auto()
    TEST = auto()

    def __str__(self) -> str:
        if self is StageType.TRAIN:
            return "train"
        elif self is StageType.VALID:
            return "valid"
        elif self is StageType.TEST:
            return "test"
        else:
            assert False, "not support."

    def __int__(self) -> int:
        if self is StageType.TRAIN:
            return StageType.TRAIN.value
        elif self is StageType.VALID:
            return StageType.VALID.value
        elif self is StageType.TEST:
            return StageType.TEST.value
        else:
            assert False, "not support."
