import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from enum import Enum
from typing import Optional, Union, Callable
from PIL import Image, ImageTk


__all__ = [
    "ImageButton",
]


class ButtonState(Enum):
    """ボタンのステート
    """
    NORMAL  = 0x0
    HOVER   = 0x1
    ACTIVE  = 0x2
    DISABLE = 0x4


class ImageButton(ttk.Label):
    """画像ボタン
    """
    def __init__(
        self,
        master:tk.Misc,
        normal:Union[str, Image.Image],
        hover:Union[str, Image.Image],
        active:Union[str, Image.Image],
        disabled:Union[str, Image.Image],
        is_disabled:bool = False,
        command:Optional[Callable[[], None]] = None,
    ) -> None:
        """コンストラクタ

        Args:
            master (tk.Misc): master
            normal (Union[str, Image.Image]): 通常時の画像
            hover (Union[str, Image.Image]): カーソルを合わせた時の画像
            active (Union[str, Image.Image]): クリックした時の画像
            disabled (Union[str, Image.Image]): 無効時の画像
            is_disabled (bool, optional): ボタンの無効状態 (初期値). Defaults to False.
            command (Optional[Callable[[], None]], optional): カーソルを合わせた状態でクリックを離した時のコールバック. Defaults to None.
        """
        self.normal_image = self.create_photo_image(normal)
        self.hover_image = self.create_photo_image(hover)
        self.active_image = self.create_photo_image(active)
        self.disabled_image = self.create_photo_image(disabled)

        super().__init__(master, image=self.disabled_image if is_disabled else self.normal_image, borderwidth=0, padding=0)

        self.bind("<ButtonPress-1>",   self.on_left_button_press)
        self.bind("<ButtonRelease-1>", self.on_left_button_release)
        self.bind("<Enter>",           self.on_enter)
        self.bind("<Leave>",           self.on_leave)

        self.command = command

        # ボタンの状態
        self.set_state(ButtonState.DISABLE if is_disabled else ButtonState.NORMAL)

    @property
    def is_hover(self) -> bool:
        """ボタンにマウスカーソルが置かれているか取得

        Returns:
            bool: ボタンにマウスカーソルが置かれている場合はTrueを返します。
        """
        return self.is_set_state(ButtonState.HOVER)

    @property
    def is_active(self) -> bool:
        """ボタンがクリックされているか取得

        ボタンにマウスカーソルが置かれているかは考慮しません。

        Returns:
            bool: ボタンがクリックされている場合はTrueを返します。
        """
        return self.is_set_state(ButtonState.ACTIVE)

    @property
    def is_disable(self) -> bool:
        """ボタンが無効状態か取得

        Returns:
            bool: 無効状態の場合はTrueを返します。
        """
        return self.is_set_state(ButtonState.DISABLE)

    @is_disable.setter
    def is_disable(self, value:bool) -> None:
        """ボタンの無効状態をセット

        Args:
            value (bool): 無効状態にする場合はTrueを指定します。
        """
        if value:
            # 無効状態は既存状態を全てクリアするため上書き
            self.set_state(ButtonState.DISABLE)
            self.configure(image=self.disabled_image)
        else:
            self.remove_state(ButtonState.DISABLE)
            self.configure(image=self.normal_image)

    def add_state(self, state:ButtonState) -> None:
        """ステートを追加

        Args:
            state (ButtonState): ステート
        """
        assert isinstance(state, ButtonState), "not support type."
        self.button_state |= state.value

    def set_state(self, state:ButtonState) -> None:
        """ステートをセット

        Args:
            state (ButtonState): ステート
        """
        assert isinstance(state, ButtonState), "not support type."
        self.button_state = state.value

    def remove_state(self, state:ButtonState) -> None:
        """ステートを削除

        Args:
            state (ButtonState): ステート
        """
        assert isinstance(state, ButtonState), "not support type."
        self.button_state &= ~state.value

    def is_set_state(self, state:ButtonState) -> bool:
        """ステートがセットされているか

        Args:
            state (ButtonState): ステート

        Returns:
            bool: セットされている場合はTrueを返します。
        """
        assert isinstance(state, ButtonState), "not support type."
        return self.button_state & state.value

    def on_left_button_press(self, event:tk.Event) -> None:
        """左クリックが押された瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        if self.is_disable:
            return

        self.add_state(ButtonState.ACTIVE)
        self.configure(image=self.active_image)

    def on_left_button_release(self, event:tk.Event) -> None:
        """左クリックが離された瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        if self.is_disable:
            return

        is_call_command = self.is_active and self.is_hover

        self.remove_state(ButtonState.ACTIVE)
        self.configure(image=self.hover_image if self.is_hover else self.normal_image)

        if is_call_command:
            self.safe_command()

    def on_enter(self, event:tk.Event) -> None:
        """ボタンにマウスカーソルが置かれた、合わせた

        Args:
            event (tk.Event): イベントプロパティ
        """
        if self.is_disable:
            return

        self.add_state(ButtonState.HOVER)
        self.configure(image=self.active_image if self.is_active else self.hover_image)

    def on_leave(self, event:tk.Event) -> None:
        """ボタンからマウスカーソルが離れた

        Args:
            event (tk.Event): イベントプロパティ
        """
        if self.is_disable:
            return

        self.remove_state(ButtonState.HOVER)
        self.configure(image=self.hover_image if self.is_active else self.normal_image)

    def safe_command(self) -> None:
        """例外全無視コールバック実行
        """
        if self.command is None:
            return

        try:
            self.command()
        except Exception as e:
            pass

    @staticmethod
    def create_photo_image(path_or_data:Union[str, Image.Image]) -> ImageTk.PhotoImage:
        """PhotoImageの作成

        画像読込や不正なImageの場合は、32x32ピクセルのパープルで塗りつぶした画像を作成します。

        Args:
            path_or_data (Union[str, Image.Image]): 画像パスかImage

        Returns:
            ImageTk.PhotoImage: PhotoImage
        """
        try:
            if isinstance(path_or_data, str):
                return ImageTk.PhotoImage(Image.open(path_or_data))
            elif isinstance(path_or_data, Image.Image):
                return ImageTk.PhotoImage(path_or_data)
        except Exception as e:
            return ImageTk.PhotoImage(Image.new("RGB", (32, 32), (255, 0, 255)))
