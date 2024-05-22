from typing import Optional, Self
from pathlib import Path
import yaml


__all__ = [
    "YMLLoader",
]


class YMLLoader:
    """YML読込機能クラス

    *.yml対応 | *.yaml非対応。
    """
    @classmethod
    def load_from_config(cls, config_path:str | Path) -> Optional[Self]:
        """設定ファイルの読込

        Args:
            config_path (str | Path): 設定ファイルパス

        Returns:
            Optional[Self]: 設定ファイルが無効な場合は None を返す。
        """
        if isinstance(config_path, str):
            config_path:Path = Path(config_path)
        elif not isinstance(config_path, Path):
            return None

        if not config_path.is_file() or config_path.suffix != ".yml":
            return None

        with open(config_path, mode="r", encoding="utf-8") as f:
            # NOTE: ファイルが空の場合は data(None) 状態になります。
            data = yaml.safe_load(f)

        return cls(**data)
