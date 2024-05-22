import os
from pathlib import Path
from typing import Any

from reinlib.utility.rein_yml import YMLLoader
from reinlib.types.rein_stage_type import StageType


__all__ = [
    "GenerateConfigBase",
]


class GenerateConfigBase(YMLLoader):
    """生成設定のベースクラス
    """
    def __init__(
        self,
        max_workers:int,
        is_debug_enabled:bool,
        is_tqdm_enabled:bool,
        output_directory:str,
        *args,
        **kwargs,
    ) -> None:
        """コンストラクタ

        Args:
            max_workers (int): 最大ワーカー数
            is_debug_enabled (bool): デバッグの有効性
            is_tqdm_enabled (bool): 進捗表示にtqdmを使用するか
            output_directory (str): 出力先のディレクトリ
        """
        # 最大ワーカー数
        # デバッグモードの場合はシングルワーカーを強制
        self.max_workers = 1 if is_debug_enabled else (max_workers if max_workers != -1 else (1 if (value:=os.cpu_count()) is None else value))

        # デバッグモードの有効性
        self.is_debug_enabled = is_debug_enabled

        # 進捗表示にtqdmを使用するか
        # デバッグモードの場合は print(..) と相性が悪いため未使用を強制
        self.is_tqdm_enabled = not is_debug_enabled and is_tqdm_enabled

        # str to Path
        output_directory:Path = Path(output_directory)

        # 出力先ディレクトリのナンバリング
        self.output_version = [
            int(dir.stem.split("_")[1])
            for dir in output_directory.glob("*")
            if dir.name.startswith("version_")
        ]
        self.output_version = max(self.output_version) + 1 if len(self.output_version) > 0 else 0

        # 出力先ディレクトリにナンバリングを適用
        self.output_directory = output_directory / f"version_{self.output_version}"

    def create_dataset_parameters(self, stage_type:StageType) -> list[tuple[Any, ...]]:
        """データセットのパラメータを作成

        Args:
            stage_type (StageType): ステージの種類

        Returns:
            list[tuple[Any, ...]]: データセットのパラメータ
        """
        try:
            return getattr(self, f"create_{stage_type}_dataset_parameters")()
        except Exception as _:
            assert False, f"not support '{stage_type}' stage_type."

    def create_stage_directory(self, stage_type:StageType, is_force_mkdir:bool = False) -> Path:
        """ステージの種類に応じた出力先を作成

        デバッグモードの場合は出力先ディレクトリを自動的に作成しません。

        Args:
            stage_type (StageType): ステージの種類
            is_force_mkdir (bool, optional): デバッグモードに関わらずディレクトリを作成するか. Defaults to False.

        Returns:
            Path: 出力先
        """
        stage_directory = self.output_directory / f"{stage_type}"
        if not self.is_debug_enabled or is_force_mkdir:
            stage_directory.mkdir(parents=True, exist_ok=True)
        return stage_directory
