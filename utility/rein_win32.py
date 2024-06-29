import time
import win32gui
import win32com
import win32com.client
import ctypes
import ctypes.wintypes
from functools import partial
from dataclasses import dataclass
from typing import Optional, Callable
import warnings


__all__ = [
    "WindowInfo",
    "get_window_info_list",
    "foreground_window",
    "extended_frame_bounds",
    "get_window_rect",
    "get_window_bbox",
]


# GW_OWNER: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindow
GW_OWNER = 4

# DWMWA_EXTENDED_FRAME_BOUNDS: https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
DWMWA_EXTENDED_FRAME_BOUNDS = 9


@dataclass
class WindowInfo:
    """ウィンドウ情報
    """
    # ウィンドウハンドル
    hwnd:int = -1

    # ウィンドウの入力操作（マウス、キーボード）の有効性
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-iswindowenabled
    enabled:int = -1

    # ウィンドウの可視性
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-iswindowvisible
    visible:int = -1

    # ウィンドウのオーナーウィンドウのハンドル
    owner:int = -1

    # ウィンドウタイトル名
    title:str = ""

    # ウィンドウが属するクラスの名前
    class_name:str = ""

    @property
    def is_enabled(self) -> bool:
        """ウィンドウの入力操作（マウス、キーボード）の有効性を取得

        Returns:
            bool: 入力操作が有効な場合はTrueを返します。
        """
        return self.enabled == 1

    @property
    def is_visible(self) -> bool:
        """ウィンドウの可視性を取得

        Returns:
            bool: 可視性が有効な場合はTrueを返します。
        """
        return self.visible == 1

    @property
    def is_owner(self) -> bool:
        """オーナーウィンドウか判定

        非オーバーウィンドウは Paint.net を例にすると Tools, Colors, History, Layers, ... を指します。

        Returns:
            bool: オーバーウィンドウの場合はTrueを返します。
        """
        return self.owner == 0

    def __init__(self, hwnd:int) -> None:
        self.hwnd = hwnd
        self.enabled = win32gui.IsWindowEnabled(hwnd)
        self.visible = win32gui.IsWindowVisible(hwnd)
        self.title = win32gui.GetWindowText(hwnd)
        self.owner = win32gui.GetWindow(hwnd, GW_OWNER)
        self.class_name = win32gui.GetClassName(hwnd)

    def is_valid(self) -> bool:
        """有効性を判定

        Returns:
            bool: 有効な場合はTrueを返します。
        """
        return self.hwnd != -1


def enum_window_callback(
    hwnd:int,
    lparam:int,
    callback_window_info_add_conditions:Optional[Callable[[WindowInfo], bool]],
    out_window_info_list:list[WindowInfo],
) -> None:
    """EnumWindowsProc

    https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclassname

    Args:
        hwnd (int): A handle to the window and, indirectly, the class to which the window belongs.
        lparam (int): zero only.
        callback_window_info_add_conditions_info (Optional[Callable[[WindowInfo], bool]]): ウィンドウ情報を追加する条件を指定
        out_window_info_list (list[WindowInfo]): ウィンドウ情報の格納先
    """
    if (window_info:=WindowInfo(hwnd)).is_valid():
        if callback_window_info_add_conditions is None or callback_window_info_add_conditions(window_info):
            out_window_info_list.append(window_info)


def get_window_info_list(
    callback_window_info_add_conditions:Optional[Callable[[WindowInfo], bool]] = None,
) -> list[WindowInfo]:
    """ウィンドウ情報リストを取得

    Args:
        callback_window_info_add_conditions (Optional[Callable[[WindowInfo], bool]], optional): ウィンドウ情報を追加する条件を指定. Defaults to None.

    Returns:
        list[WindowInfo]: ウィンドウ情報リスト
    """
    window_info_list:list[WindowInfo] = []
    # EnumWindows     : https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows
    # EnumWindowsProc : https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms633498(v=vs.85)
    win32gui.EnumWindows(partial(enum_window_callback, callback_window_info_add_conditions=callback_window_info_add_conditions, out_window_info_list=window_info_list), 0)
    return window_info_list


def foreground_window(
    hwnd:int,
    wait_time:float = 0.01666666,
    after_dispatch:Optional[str] = None,
) -> None:
    """ウィンドウを最前面に移動

    Args:
        hwnd (int): ウィンドウハンドル
        wait_time (float, optional): 最前面に移動後の待機時間 (単位: sec). Defaults to 0.01666666.
    """
    # NOTE: fix pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')
    win32com.client.Dispatch("WScript.Shell").SendKeys("%")

    win32gui.SetForegroundWindow(hwnd)
    if wait_time > 0.0:
        time.sleep(wait_time)

    # NOTE: SetForegroundWindowの対象がtkinterの場合Menuが初期選択されるので解除する
    if after_dispatch is not None:
        win32com.client.Dispatch("WScript.Shell").SendKeys(after_dispatch)


def extended_frame_bounds(hwnd:int) -> tuple[int, int, int, int]:
    """ウィンドウ領域を取得

    不正なウィンドウハンドルの場合はウィンドウ領域はゼロです。

    Args:
        hwnd (int): 対象のウィンドウハンドル

    Returns:
        tuple[int, int, int, int]: xmin, ymin, xmax, ymaxを返す
    """
    rect = ctypes.wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(
        ctypes.wintypes.HWND(hwnd),
        ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect),
        ctypes.sizeof(rect),
    )
    return rect.left, rect.top, rect.right, rect.bottom


def get_window_bbox(hwnd:int) -> tuple[int, int, int, int]:
    """ウィンドウ領域を取得

    不正なウィンドウハンドルの場合はウィンドウ領域はゼロです。

    Args:
        hwnd (int): 対象のウィンドウハンドル

    Returns:
        tuple[int, int, int, int]: xmin, ymin, xmax, ymaxを返す
    """
    warnings.warn(
        "get_window_bbox(..) has been deprecated use extended_frame_bounds(..) instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return extended_frame_bounds(hwnd)


def get_window_rect(hwnd) -> tuple[int, int, int, int]:
    """ウィンドウ領域を取得

    不正なウィンドウハンドルの場合はウィンドウ領域はゼロです。

    Args:
        hwnd (int): 対象のウィンドウハンドル

    Returns:
        tuple[int, int, int, int]: xmin, ymin, xmax, ymaxを返す
    """
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(
        hwnd,
        ctypes.byref(rect),
    )
    return rect.left, rect.top, rect.right, rect.bottom
