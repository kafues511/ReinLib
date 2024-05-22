from abc import ABC, abstractmethod
import shutil

from reinlib.utility.rein_generate_config import GenerateConfigBase


__all__ = [
    "DatasetGeneratorAbstract",
]


class DatasetGeneratorAbstract(ABC):
    """データセット生成の抽象クラス
    """
    def __init__(
        self,
        config_path:str,
        *args,
        **kwargs,
    ) -> None:
        """コンストラクタ

        Args:
            config_path (str): 生成設定のファイルパス
        """
        if (config:=self.generate_config_cls.load_from_config(config_path)) is None:
            assert False, "fail load config."

        self.config = config
        self.config_path = config_path

    @property
    @abstractmethod
    def config(self) -> GenerateConfigBase:
        """生成設定を取得

        Returns:
            GenerateConfigBase: 生成設定
        """
        raise NotImplementedError()

    @config.setter
    @abstractmethod
    def config(self, new_config:GenerateConfigBase) -> None:
        """生成設定をセット

        Args:
            new_config (GenerateConfigBase): 生成設定
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def generate_config_cls(self) -> GenerateConfigBase:
        """生成設定クラス

        Returns:
            GenerateConfigBase: 生成設定クラス
        """
        raise NotImplementedError()

    def generate(self) -> None:
        """データセットの生成
        """
        # 再現性のために設定ファイルを出力先にコピー
        self.config_copy_to_output_directory()

        # データセットの生成
        self.generate_impl()

    def generate_impl(self) -> None:
        """データセットの生成（実装）
        """
        raise NotImplementedError()

    def config_copy_to_output_directory(self) -> None:
        """設定ファイルを出力先にコピー
        """
        if not self.config.is_debug_enabled:
            self.config.output_directory.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.config_path, str(self.config.output_directory / "config.yml"))
