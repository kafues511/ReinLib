import os
import subprocess
from typing import Optional
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor, Future
from tqdm import tqdm


__all__ = [
    "try_readlink",
    "get_sort_hash",
    "get_paths_in_directory",
    "get_paths_in_directories",
    "directory_to_purepath",
    "path_to_purepath",
    "fast_remove",
]


def try_readlink(path:str) -> Optional[str]:
    """シンボリックリンクの参照元を取得

    Args:
        path (str): シンボリックリンクが設定されているパス

    Returns:
        str: シンボリックリンクの参照元、取得に失敗した場合は None を返します。
    """
    if os.path.islink(path) and os.path.isfile(symlink_path:=os.readlink(path)):
        return symlink_path
    else:
        return None


def get_sort_hash() -> Optional[str]:
    """省略ハッシュを取得

    Returns:
        Optional[str]: 省略ハッシュ、取得に失敗した場合は None を返します。
    """
    try:
        command = "git rev-parse --short HEAD"
        sort_hash = subprocess.check_output(command.split()).strip().decode("utf-8")
        return sort_hash
    except Exception as e:
        return None


def get_paths_in_directory(
    directory:str,
    suffixes:tuple[str, ...],
) -> list[Path]:
    """ディレクトリ内のパスを取得

    Args:
        directory (str): ディレクトリ
        suffixes (tuple[str, ...]): 対象の拡張子リスト (ピリオドを含む)

    Returns:
        list[Path]: 拡張子が含まれるパスリスト
    """
    return [
        path
        for path in Path(directory).glob("*")
        if path.suffix in suffixes
    ]


def get_paths_in_directories(
    directories:tuple[str, ...] | list[str],
    suffixes:tuple[str, ...],
) -> list[Path]:
    """ディレクトリ内のパスを取得

    Args:
        directories (tuple[str, ...] | list[str]): ディレクトリリスト
        suffixes (tuple[str, ...]): 対象の拡張子リスト (ピリオドを含む)

    Returns:
        list[Path]: 拡張子が含まれるパスリスト
    """
    return [
        path
        for directory in directories
        for path in Path(directory).glob("*")
        if path.suffix in suffixes
    ]


def directory_to_purepath(
    directory:str | Path,
    is_dir:bool = True,
) -> Optional[Path]:
    """_summary_

    Args:
        directory (str | Path): _description_
        is_dir (bool, optional): _description_. Defaults to True.

    Returns:
        Optional[Path]: _description_
    """
    if isinstance(directory, str):
        directory:Path = Path(directory)
    elif not isinstance(directory, Path):
        return None

    if is_dir and not directory.is_dir():
        return None

    return directory


def path_to_purepath(
    path:str | Path,
    is_file:bool = True,
) -> Optional[Path]:
    """_summary_

    Args:
        path (str | Path): _description_
        is_file (bool, optional): _description_. Defaults to True.

    Returns:
        Optional[Path]: _description_
    """
    if isinstance(path, str):
        path:Path = Path(path)
    elif not isinstance(path, Path):
        return None

    if is_file and not path.is_file():
        return None

    return path


def fast_remove(
    remove_directory:str | Path,
    pattern_list:list[str] = ["**/*.pkl", "**/*.png", "**/*.jpg"],
    max_workers:Optional[int] = None,
) -> None:
    """_summary_

    Args:
        remove_directory (str | Path): _description_
        pattern_list (list[str], optional): _description_. Defaults to ["**/*.pkl", "**/*.png", "**/*.jpg"].
        max_workers (Optional[int], optional): _description_. Defaults to None.
    """
    if isinstance(remove_directory, str):
        remove_directory:Path = Path(remove_directory)
    elif not isinstance(remove_directory, Path):
        return

    if not remove_directory.is_dir():
        return

    with ThreadPoolExecutor(max_workers) as executor:
        futures:list[Future[None]] = []

        for pattern in pattern_list:
            futures += [
                executor.submit(
                    os.remove,
                    str(path),
                )
                for path in Path(remove_directory).glob(pattern)
            ]

        with tqdm(futures, desc=str(remove_directory)) as pbar:
            for future in pbar:
                future.result()

        futures.clear()

    # ファイルの削除が完了したらディレクトリごと削除
    shutil.rmtree(str(remove_directory))
