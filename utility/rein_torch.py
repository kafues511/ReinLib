from pathlib import Path

import torch


__all__ = [
    "get_accelerator",
    "find_minimum_loss_checkpoint",
]


def get_accelerator() -> str:
    """acceleratorを取得

    "cpu", "gpu" のどちらかを想定しています。

    Returns:
        str: accelerator
    """
    return "gpu" if torch.cuda.is_available() else "cpu"


def find_minimum_loss_checkpoint(checkpoint_directory:str) -> str:
    """最小損失のチェックポイントを探す

    Args:
        checkpoint_directory (str): チェックポイントが保存されているディレクトリ

    Returns:
        str: 最小損失のチェックポイントのパス
    """
    minimum_loss:float = None
    minimum_ckpt:str = None

    for checkpoint_path in Path(checkpoint_directory).glob("*.ckpt"):
        start = checkpoint_path.name.find("loss=")
        end = checkpoint_path.name.find(".ckpt")
        if start == -1 or end == -1:
            continue

        loss = float(checkpoint_path.name[start + len("loss="):end])

        if minimum_loss is None or loss < minimum_loss:
            minimum_loss = loss
            minimum_ckpt = str(checkpoint_path)

    return minimum_ckpt
