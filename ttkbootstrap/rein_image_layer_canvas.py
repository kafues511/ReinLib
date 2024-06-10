import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import math
import numpy as np
import numpy.typing as npt
from typing import Optional, Callable
from PIL import Image, ImageTk
from dataclasses import dataclass, field
from functools import partial

from reinlib.types.rein_float2 import Float2
from reinlib.types.rein_float_minmax import FloatMinMax
from reinlib.types.rein_float_bounding_box import FloatBoundingBox
from reinlib.types.rein_bounding_box import BoundingBox
from reinlib.types.rein_int2 import Int2
from reinlib.types.rein_size2d import Size2D
from reinlib.types.rein_blend_mode import BlendMode
from reinlib.utility.rein_image import alpha_composite
from reinlib.utility.rein_math import clamp


__all__ = [
    "LayerId",
    "ImageLayerCanvas",
]


# レイヤーID型
LayerId = int


class LayerProperties(ttk.Toplevel):
    """レイヤープロパティ
    """
    def __init__(
        self,
        position:tuple[int, int],
        layer_name:str,
        blend_mode:BlendMode,
        is_visible:bool,
        callback_apply_layer_properties:Optional[Callable[[str, BlendMode, bool], None]] = None,
    ) -> None:
        """コンストラクタ

        Args:
            position (tuple[int, int]): ポップ位置
            layer_name (str): レイヤー名
            blend_mode (BlendMode): ブレンドモード
            is_visible (bool): 可視性
            callback_apply_layer_properties (Optional[Callable[[str, BlendMode, bool], None]], optional): プロパティ適用時のコールバック. Defaults to None.
        """
        super().__init__(title="Layer Properties", position=position)

        self.layer_name_var = tk.StringVar(self, layer_name)
        self.blend_mode_var = tk.StringVar(self, blend_mode)
        self.is_visible_var = tk.BooleanVar(self, is_visible)

        self.tk_name_label = ttk.Label(self, text="Name")
        self.tk_name_label.grid(column=0, row=0, padx=5, pady=0, sticky=W)
        self.tk_name_entry = ttk.Entry(self, textvariable=self.layer_name_var)
        self.tk_name_entry.grid(column=0, columnspan=3, row=1, padx=5, pady=0, sticky=EW)

        self.tk_blend_mode_label = ttk.Label(self, text="BlendMode")
        self.tk_blend_mode_label.grid(column=0, row=4, padx=5, pady=(20, 0), sticky=W)

        self.tk_blend_mode_cmbbox = ttk.Combobox(self, state=READONLY, textvariable=self.blend_mode_var, values=BlendMode.values())
        self.tk_blend_mode_cmbbox.grid(column=1, columnspan=2, row=4, padx=5, pady=(20, 0), sticky=EW)

        self.tk_visible_ckbtn = ttk.Checkbutton(self, width=6, text="Visible", variable=self.is_visible_var)
        self.tk_visible_ckbtn.grid(column=0, columnspan=3, row=6, padx=5, pady=(15, 10), sticky=W)

        self.tk_ok_button = ttk.Button(self, width=8, text="OK", command=self.on_ok)
        self.tk_ok_button.grid(column=1, row=7, padx=5, pady=5, sticky=EW)

        self.tk_cancel_button = ttk.Button(self, width=8, bootstyle="outline", text="Cancel", command=self.on_cancel)
        self.tk_cancel_button.grid(column=2, row=7, padx=5, pady=5, sticky=EW)

        # register callbacks
        self.callback_apply_layer_properties = callback_apply_layer_properties

        # モーダルウィンドウ設定
        self.grab_set()
        self.focus_set()
        self.transient(self.master)

        self.resizable(width=False, height=False)                   # 最小化/最大化ボタンを無効化
        self.iconphoto(False, tk.PhotoImage(data=self.icondata()))  # アイコン設定

    @staticmethod
    def icondata() -> str:
        """アイコン画像をBase64で取得

        Returns:
            str: アイコン画像 (Base64)
        """
        return """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAALOSURBVDhPNVO5bhRBEH3TPT09987u+mAXI2xHJrFkI4TkACESC4gtAgISYhICAkTKHxDwTUgQIXHYkBgbH3t4PXvOxeuRWGk0PVVdVe+otbZevq/G4xQ3O2v48u0rPO2iAGDbCi+ePERlCaSzBaaLDFVVgQFmK8zmC1wMhxBx0kC300UYePC8AKXtQHk+Xh08ZhOblwFhWWiHPpSUEMKCFAJaO+gsLzPHjySJEfosVg5sz4Xj+kgCF7HvInIdaGVDSoGAZ0/bsHlWfAwS4TkM8vn04yck4SvHNNCMKQT1ZVk3GBOyOZu4QWF+eVlCOErW3ffvbSOqp2u4fPfHM4Q8N3wHia+xEvvQtoAp9YmkoB5GElEUJWzSkOR5sLcDTTSdZgO/LkZYaQRYayfotmJ0mzFaoYcmtXBtSTqa/NmAeFCSi6Rg14R5f3MNTd/D/vYGkUksJQHakUcRPd6yiMrBajOq35qaCaNsXlYYphMsRX499ag/onUZe1Nt5o14l8xnRYFrWnp02kc7DuGQurX7+kPVWWpySkjVNdFYyElufbnBCZL0JIvmWCzyeh/MLlxRn/OrFMPxBJZ49q6y6anQGj4d8LTCZquBR1u3QGD1Dhi1F1mO00FaL1TCnTk8OafALoThX7JrSTGnRQ6PsDbaMb7/HeL35QgzFl5N5lSdrvPe8we7tf+rSYScNZT+bQX6rBwNKAWfSEJ6nXOyccZlw6d31onObKGNk94VeukYMyIpq/8N6IBFa6TSaBHWnPtfcAqYVvTK5fdOp43YiHnN4izjdP5jDEXJ6QEXh+ohomh7t7vICdthcsr3DWoyoL2x69b854wZWgV1mec5rLtvPlYmaFbU53KYTfMoqpI2Ph+fYkKe61HATQwwms6Q5QUWnG4aZMyJlN3nDEwIC5aspwzI8bjXxzntGqRT/BmlODzr4YzWmc3tM6ZIS0uJf+TNJJPTh6T9AAAAAElFTkSuQmCC"""

    @property
    def layer_name(self) -> str:
        """レイヤー名を取得

        Returns:
            str: レイヤー名
        """
        return self.layer_name_var.get()

    @property
    def blend_mode(self) -> BlendMode:
        """ブレンドモードの取得

        Returns:
            BlendMode: ブレンドモード
        """
        return BlendMode.from_str(self.blend_mode_var.get())

    @property
    def is_visible(self) -> bool:
        """可視性を取得

        Returns:
            bool: 可視性
        """
        return self.is_visible_var.get()

    def on_ok(self) -> None:
        """okボタン
        """
        self.apply_property()
        self.close()

    def on_cancel(self) -> None:
        """cancelボタン
        """
        self.close()

    def apply_property(self) -> None:
        """設定したプロパティの適用
        """
        if self.callback_apply_layer_properties is not None:
            self.callback_apply_layer_properties(
                self.layer_name,
                self.blend_mode,
                self.is_visible,
            )

    def close(self) -> None:
        """終了処理
        """
        self.destroy()


class LayersWindowItem(ttk.Frame):
    """LayersWindowに表示するアイテム
    """
    def __init__(
        self,
        master:tk.Misc,
        image:npt.NDArray[np.uint8],
        lid:LayerId,
        name:str = "Background",
        blend_mode:BlendMode = BlendMode.NORMAL,
        is_visible:bool = True,
        width:int = 14,
        is_start_selected:bool = False,
        depth:int = 0,
        callback_select_layer:Optional[Callable[[tk.Event, LayerId], None]] = None,
        callback_update_layer:Optional[Callable[[LayerId, int, BlendMode, bool], None]] = None,
    ) -> None:
        """コンストラクタ

        Args:
            master (tk.Misc): master
            image (npt.NDArray[np.uint8]): サムネイル画像
            lid (LayerId): レイヤーID
            name (str, optional): レイヤー名. Defaults to "Background".
            blend_mode (BlendMode, optional): ブレンドモード. Defaults to BlendMode.NORMAL.
            is_visible (bool, optional): 可視性. Defaults to True.
            width (int, optional): アイテムの横幅サイズ. Defaults to 14.
            is_start_selected (bool, optional): レイヤーを選択した状態で開始するか. Defaults to False.
            depth (int, optional): レイヤーの深さ. Defaults to 0.
            callback_select_layer (Optional[Callable[[tk.Event, LayerId], None]], optional): レイヤーを選択した際のコールバック. Defaults to None.
            callback_update_layer (Optional[Callable[[LayerId, int, BlendMode, bool], None]], optional): レイヤー設定を更新した際のコールバック. Defaults to None.
        """
        super().__init__(master, padding=1, bootstyle="info" if is_start_selected else None)

        # レイヤーID
        self.lid = lid

        # レイヤーの深さ
        self.depth = depth

        # 選択状態
        self.is_selected = is_start_selected

        # ブレンドモード
        self.blend_mode = blend_mode

        # サムネイル画像
        self.thumbnail_image = self.create_thumbnail_image(image)
        self.thumbnail_image_tk = ImageTk.PhotoImage(image=self.thumbnail_image)

        # サムネイル表示ラベル
        self.tk_thumbnail_label = ttk.Label(self, image=self.thumbnail_image_tk)
        self.tk_thumbnail_label.grid(column=0, row=0, sticky=NSEW)

        # レイヤー名
        self.layer_name_var = tk.StringVar(self, name)

        # レイヤー名表示ラベル
        self.tk_layer_name_label = ttk.Label(self, textvariable=self.layer_name_var, width=width)
        self.tk_layer_name_label.grid(column=1, row=0, sticky=NSEW)

        # 可視性
        self.is_visible_var = tk.BooleanVar(self, is_visible)

        # 可視性の切り替えボタン
        self.tk_visible_checkbutton = ttk.Checkbutton(self, padding=(2, 0, 0, 0), variable=self.is_visible_var, command=self.on_visible, bootstyle="light")
        self.tk_visible_checkbutton.grid(column=2, row=0, sticky=NSEW)

        # 各種コールバックの登録
        self.tk_thumbnail_label.bind("<ButtonPress-1>",    self.on_left_button_press)
        self.tk_layer_name_label.bind("<ButtonPress-1>",   self.on_left_button_press)
        self.tk_thumbnail_label.bind("<Double-Button-1>",  self.on_left_button_double)
        self.tk_layer_name_label.bind("<Double-Button-1>", self.on_left_button_double)

        self.callback_select_layer = callback_select_layer
        self.callback_update_layer = callback_update_layer

    @property
    def layer_name(self) -> str:
        """レイヤー名を取得

        Returns:
            str: レイヤー名
        """
        return self.layer_name_var.get()

    @layer_name.setter
    def layer_name(self, new_layer_name:str) -> None:
        """レイヤー名をセット

        Args:
            new_layer_name (str): レイヤー名
        """
        self.layer_name_var.set(new_layer_name)

    @property
    def is_selected(self) -> bool:
        """選択状態を取得

        Returns:
            bool: 選択状態
        """
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, is_new_selected:bool) -> None:
        """選択状態をセット

        Args:
            is_new_selected (bool): 選択状態
        """
        self.__is_selected = is_new_selected
        self.configure(bootstyle="info" if self.is_selected else "none")

    @property
    def is_visible(self) -> bool:
        """可視性の取得

        Returns:
            bool: 可視性
        """
        return self.is_visible_var.get()

    @is_visible.setter
    def is_visible(self, is_new_visible:bool) -> None:
        """可視性のセット

        Args:
            is_new_visible (bool): 可視性
        """
        self.is_visible_var.set(is_new_visible)

    def on_left_button_press(self, event:tk.Event) -> None:
        """マウス左ボタンをクリックした瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        if self.callback_select_layer is not None:
            self.callback_select_layer(event, self.lid)

    def on_left_button_double(self, event:tk.Event) -> None:
        """マウス左ボタンをダブルクリックした瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        layer_properties = LayerProperties(
            position=self.winfo_pointerxy(),
            layer_name=self.layer_name,
            blend_mode=self.blend_mode,
            is_visible=self.is_visible,
            callback_apply_layer_properties=self.set_layer_properties,
        )
        self.wait_window(layer_properties)

    def on_visible(self) -> None:
        """可視性の変更
        """
        self.callback_update_layer(self.lid, self.depth, self.blend_mode, self.is_visible)

    def set_layer_properties(
        self,
        layer_name:str,
        blend_mode:BlendMode,
        is_visible:bool,
    ) -> None:
        """レイヤー設定をセット

        Args:
            layer_name (str): レイヤー名
            blend_mode (BlendMode): ブレンドモード
            is_visible (bool): 可視性
        """
        # 見た目に関わるパラメータが変更されたか
        is_request_update = (self.blend_mode != blend_mode) or (self.is_visible != is_visible)

        self.layer_name = layer_name
        self.blend_mode = blend_mode
        self.is_visible = is_visible

        if is_request_update:
            self.callback_update_layer(
                self.lid,
                self.depth,
                self.blend_mode,
                self.is_visible,
            )

    def set_thumbnail_image(self, image:npt.NDArray[np.uint8]) -> None:
        """サムネイル画像をセット

        Args:
            image (npt.NDArray[np.uint8]): 画像
        """
        # サムネイル画像を作成
        thumbnail_image = self.create_thumbnail_image(image)
        thumbnail_image_tk = ImageTk.PhotoImage(image=thumbnail_image)

        # サムネイル表示ラベル
        self.tk_thumbnail_label.configure(image=thumbnail_image_tk)

        # change memroy
        self.thumbnail_image = thumbnail_image
        self.thumbnail_image_tk = thumbnail_image_tk

    def create_thumbnail_image(self, image:npt.NDArray[np.uint8]) -> Image.Image:
        """サムネイル画像の作成

        Args:
            image (npt.NDArray[np.uint8]): 画像

        Returns:
            Image.Image: サムネイル画像
        """
        if len(image.shape) == 2 or (c:=image.shape[2]) == 1:
            thumbnail_image = Image.fromarray(image, mode="L").convert("RGB")
        elif c == 4:
            thumbnail_image = Image.fromarray(image, mode="RGBA").convert("RGB")
        elif c == 3:
            thumbnail_image = Image.fromarray(image, mode="RGB")
        else:
            assert False, "not support."

        # 画像サイズの比率を維持してリサイズ
        src_size_w, src_size_h = (thumbnail_image.width, thumbnail_image.height)
        dst_size_w, dst_size_h = (50, 37)

        downscale_w = dst_size_w / src_size_w
        downscale_h = dst_size_h / src_size_h

        if downscale_w < downscale_h:
            new_w = int(src_size_w * downscale_w)
            new_h = int(src_size_h * downscale_w)
        elif downscale_w > downscale_h:
            new_w = int(src_size_w * downscale_h)
            new_h = int(src_size_h * downscale_h)
        else:
            new_w = int(src_size_w * downscale_w)
            new_h = int(src_size_h * downscale_h)

        thumbnail_image = thumbnail_image.resize((new_w, new_h), resample=Image.Resampling.BILINEAR)
        src_size_w, src_size_h = (thumbnail_image.width, thumbnail_image.height)

        canvas_image = Image.new("RGB", (dst_size_w, dst_size_h), (255, 255, 255))

        # 中央貼り付け
        paste_x = (dst_size_w - src_size_w)//2
        paste_y = (dst_size_h - src_size_h)//2

        canvas_image.paste(thumbnail_image, (paste_x, paste_y))

        return canvas_image


class LayersWindow(ttk.Frame):
    """各レイヤーの制御ウィンドウ
    """
    # マウスボタン待機中
    BUTTON_NONE = 0x0
    # マウス左ボタン押下中
    BUTTON_LEFT_PRESS  = 0x1
    # マウス中央ボタン押下中
    BUTTON_CENTER_PRESS  = 0x2
    # マウス右ボタン押下中
    BUTTON_RIGHT_PRESS = 0x4

    def __init__(
        self,
        master:tk.Misc,
        callback_move_layers:Optional[Callable[[Int2], None]] = None,
        callback_update_layer:Optional[Callable[[LayerId, int, BlendMode, bool], None]] = None,
    ) -> None:
        super().__init__(master, padding=1, bootstyle="secondary")

        self.tk_label = ttk.Label(self, text="Layers", padding=(4, 4, 0, 4))
        self.tk_label.grid(column=0, row=0, sticky=NSEW)

        # 表示するレイヤーリスト
        self.layers:list[LayersWindowItem] = []

        # カーソル位置
        self.cursor_xy = Int2.zero()

        # マウスボタンの入力状態
        self.button_flags = self.BUTTON_NONE

        # 各種コールバックの登録
        self.tk_label.bind("<ButtonPress-1>",   self.on_left_button_press)
        self.tk_label.bind("<ButtonRelease-1>", self.on_left_button_release)
        self.tk_label.bind("<Motion>",          self.on_mouse_motion)

        self.callback_move_layers = callback_move_layers
        self.callback_update_layer = callback_update_layer

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def on_left_button_press(self, event:tk.Event) -> None:
        """マウス左ボタンをクリックした瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        # 複数アクションは現状禁止
        if self.button_flags != self.BUTTON_NONE:
            return

        self.cursor_xy = Int2(event.x_root, event.y_root)

        # マウス左ボタン押下中を立てる
        self.button_flags |= self.BUTTON_LEFT_PRESS

    def on_left_button_release(self, event:tk.Event) -> None:
        """マウス左ボタンを離した瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        # マウス左ボタン押下中の削除
        self.button_flags &= ~self.BUTTON_LEFT_PRESS

    def on_mouse_motion(self, event:tk.Event) -> None:
        """マウスカーソル移動

        Args:
            event (tk.Event): イベントプロパティ
        """
        if self.button_flags == self.BUTTON_NONE:
            return

        new_cursor_xy = Int2(event.x_root, event.y_root)

        if self.callback_move_layers is not None:
            # velocityを引数にLayersWindowの移動を伝えます。
            self.callback_move_layers(new_cursor_xy - self.cursor_xy)

        self.cursor_xy = new_cursor_xy

    def on_select_layer(self, event:tk.Event, lid:LayerId) -> None:
        """レイヤー選択の更新

        Args:
            event (tk.Event): イベントプロパティ
            lid (LayerId): 選択したレイヤーID
        """
        for layer in self.layers:
            layer.is_selected = (layer.lid == lid)

    def get_selecting_layer_id(self) -> Optional[LayerId]:
        """選択中のレイヤーIDを取得

        Returns:
            Optional[LayerId]: レイヤーが未選択の場合はNoneを返します。
        """
        for layer in self.layers:
            if layer.is_selected:
                return layer.lid
        return None

    def create_layer_name(self) -> str:
        """レイヤー名の作成

        Returns:
            str: レイヤー名
        """
        return "Background" if len(self.layers) == 0 else f"Layer {len(self.layers) + 1}"

    def add_layer(
        self,
        image:npt.NDArray[np.uint8],
        layer_name:Optional[str],
        layer_id:int,
        depth:int,
        blend_mode:BlendMode,
    ) -> None:
        """レイヤーの追加

        Args:
            image (npt.NDArray[np.uint8]): サムネイル画像
            layer_name (Optional[str]): レイヤー名
            layer_id (int): レイヤーID
            depth (int): レイヤーの深さ
            blend_mode (BlendMode): ブレンドモード
        """
        if layer_name is None:
            layer_name = self.create_layer_name()

        # 新規追加レイヤーを選択させるため、既存の選択状態を全解除
        for layer in self.layers:
            layer.is_selected = False

        self.layers.append(
            LayersWindowItem(
                self,
                image=image,
                lid=layer_id,
                name=layer_name,
                blend_mode=blend_mode,
                depth=depth,
                is_start_selected=True,
                callback_select_layer=self.on_select_layer,
                callback_update_layer=self.callback_update_layer,
            )
        )

        for layer in self.layers:
            layer.grid(column=0, row=len(self.layers) - layer.depth)

    def set_layer_name(self, lid:LayerId, layer_name:str) -> None:
        """レイヤー名をセット

        Args:
            lid (LayerId): レイヤーID
            layer_name (str): レイヤー名
        """
        for layer in self.layers:
            if layer.lid == lid:
                layer.layer_name = layer_name
                break

    def set_is_visible(self, lid:LayerId, is_visible:bool) -> None:
        """可視性をセット

        Args:
            lid (LayerId): レイヤーID
            is_visible (bool): 可視性
        """
        for layer in self.layers:
            if layer.lid == lid:
                layer.is_visible = is_visible
                break

    def set_thumbnail_image(self, lid:LayerId, image:npt.NDArray[np.uint8]) -> None:
        """サムネイル画像をセット

        Args:
            lid (LayerId): レイヤーID
            image (npt.NDArray[np.uint8]): 画像
        """
        for layer in self.layers:
            if layer.lid == lid:
                layer.set_thumbnail_image(image)
                break


@dataclass
class LayerInfo:
    # レイヤーID
    lid:LayerId = -1
    # 元画像 (スケール適用前)
    image:Optional[npt.NDArray[np.uint8]] = None
    # RGB (スケール適用後)
    color:Optional[npt.NDArray[np.uint8]] = None
    # Alpha (スケール適用後)
    alpha:Optional[npt.NDArray[np.uint8]] = None
    # レイヤー深度
    depth:int = 0
    # ブレンドモード
    blend_mode:BlendMode = BlendMode.NORMAL
    # 可視性
    is_visible:bool = True
    # レイヤーの位置固定化
    is_fixed_position:bool = False
    # 最後に適用したスケール
    scale:float = 1.0
    # 位置 (スケール適用前)
    position:Int2 = field(default_factory=lambda: Int2.zero())
    # サイズ (スケール適用前)
    size:Size2D = field(default_factory=lambda: Size2D.zero())

    def __post_init__(self) -> None:
        if self.image is not None:
            h, w, c = self.image.shape

            if c == 3:
                pass
            elif c == 4:
                pass

            self.size.wh = (w, h)

            # 初期スケールを適用
            self.apply_scale(self.scale)

    @property
    def position2(self) -> Int2:
        """スケール適用後の位置を取得

        Returns:
            Int2: スケール適用後の位置
        """
        return Int2(math.ceil(self.position.x * self.scale), math.ceil(self.position.y * self.scale))

    @property
    def size2(self) -> Size2D:
        """スケール適用後のサイズを取得

        Returns:
            Size2D: スケール適用後のサイズ
        """
        return Size2D(math.ceil(self.size.w * self.scale), math.ceil(self.size.h * self.scale))

    @property
    def xmax(self) -> int:
        """スケール適用前の右下のx座標を取得

        Returns:
            int: 右下のx座標
        """
        return self.position.x + self.size.w

    @property
    def ymax(self) -> int:
        """スケール適用前の右下のy座標を取得

        Returns:
            int: 右下のy座標
        """
        return self.position.y + self.size.h

    @property
    def xmax2(self) -> int:
        """スケール適用後の右下のx座標を取得

        Returns:
            int: 右下のx座標
        """
        return self.position2.x + self.size2.w

    @property
    def ymax2(self) -> int:
        """スケール適用後の右下のy座標を取得

        Returns:
            int: 右下のy座標
        """
        return self.position2.y + self.size2.h

    def update_image(self, image:npt.NDArray[np.uint8]) -> None:
        """レイヤーの画像更新

        Args:
            image (npt.NDArray[np.uint8]): 画像
        """
        self.image = image

        h, w, _ = self.image.shape

        self.size.wh = (w, h)

        # 最終スケールを適用
        self.apply_scale(self.scale)

    def apply_scale(self, scale:float) -> None:
        """スケール変更の適用

        Args:
            scale (float): スケール値
        """
        self.scale = scale

        if self.scale == 1.0:
            image = self.image
        elif self.scale > 1.0:
            image = Image.fromarray(self.image, mode="RGBA")
            image = image.resize(self.size2.wh, resample=Image.Resampling.NEAREST)
            image = np.array(image)
        else:
            image = Image.fromarray(self.image, mode="RGBA")
            image = image.resize(self.size2.wh, resample=Image.Resampling.BILINEAR)
            image = np.array(image)

        self.color, self.alpha = np.dsplit(image, (3, ))


class ImageLayerCanvas:
    """レイヤー機能付きの画像表示キャンバス
    """
    # マウスボタン待機中
    BUTTON_NONE = 0x0
    # マウス左ボタン押下中
    BUTTON_LEFT_PRESS  = 0x1
    # マウス中央ボタン押下中
    BUTTON_CENTER_PRESS  = 0x2
    # マウス右ボタン押下中
    BUTTON_RIGHT_PRESS = 0x4

    def __init__(
        self,
        master:tk.Misc,
    ) -> None:
        # メインキャンバス
        self.tk_canvas = ttk.Canvas(master)

        # スクロールバー
        self.tk_yview = ttk.Scrollbar(master, orient=VERTICAL,   command=self.on_yview)
        self.tk_xview = ttk.Scrollbar(master, orient=HORIZONTAL, command=self.on_xview)
        self.tk_canvas.configure(xscrollcommand=self.tk_xview.set, yscrollcommand=self.tk_yview.set)

        # 背景
        self.bg_iid = self.tk_canvas.create_rectangle(-1920.0, -1920.0, 1920.0, 1920.0, fill="#CFCFCF", width=0)

        # カーソル位置
        self.cursor_xy = Int2.zero()

        # マウスボタンの入力状態
        self.button_flags = self.BUTTON_NONE

        # SceneColor
        self.scene_color:Optional[ImageTk.PhotoImage] = None
        self.scene_color_iid = self.tk_canvas.create_image(0, 0, anchor=NW)

        # レイヤーリスト
        self.layers:list[LayerInfo] = []

        # 空いているレイヤーID
        self.empty_lids:list[LayerId] = []

        # スケール細分度
        self.global_scales = [
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            12.0,
            13.0,
            15.0,
            16.0,
            18.0,
            20.0,
            23.0,
            26.0,
            29.0,
            32.0,
            36.0,
            40.0,
            45.0,
            51.0,
            57.0,
            64.0,
            71.0,
            80.0,
            89.0,
            100.0,
            112.0,
            125.0,
            140.0,
            157.0,
            176.0,
            200.0,
            # NOTE: リサイズコストが高いので封印
            #224.0,
            #251.0,
            #281.0,
            #300.0,
            #336.0,
            #376.0,
            #421.0,
            #472.0,
            #529.0,
            #600.0,
            #700.0,
            #800.0,
            #900.0,
            #1000.0,
            #1100.0,
            #1200.0,
            #1300.0,
            #1500.0,
            #1700.0,
            #1900.0,
            #2100.0,
            #2400.0,
            #2700.0,
            #3000.0,
            #3400.0,
            #3800.0,
            #4300.0,
            #4800.0,
            #5400.0,
            #6000.0,
            #6700.0,
            #7500.0,
            #8400.0,
            #9400.0,
            #10000.0,
        ]

        # 現在のスケール
        self.global_scale_var = ttk.StringVar(master, value="100%")
        self.global_scale_index = self.global_scales.index(100.0)

        # 現在のスケール表示ラベル
        self.tk_global_scale_label = ttk.Label(master, textvariable=self.global_scale_var)

        # レイヤー制御ウィンドウ
        self.tk_layers_window = LayersWindow(master, self.on_layers, self.on_update_layer)
        self.layers_window_lid = self.tk_canvas.create_window(100.0, 100.0, window=self.tk_layers_window, width=168)

        # 各種コールバックの設定
        self.tk_canvas.bind("<MouseWheel>",         self.on_mouse_wheel)
        self.tk_canvas.bind("<Shift-MouseWheel>",   self.on_shift_mouse_wheel)
        self.tk_canvas.bind("<Control-MouseWheel>", self.on_control_mouse_wheel)
        self.tk_canvas.bind("<Motion>",             self.on_mouse_motion)

        self.tk_canvas.bind("<ButtonPress-1>",   self.on_left_button_press)
        self.tk_canvas.bind("<ButtonRelease-1>", self.on_left_button_release)
        self.tk_canvas.bind("<ButtonPress-2>",   self.on_center_button_press)
        self.tk_canvas.bind("<ButtonRelease-2>", self.on_center_button_release)

        self.tk_canvas.bind("<Configure>", self.on_configure)

        self.tk_canvas.bind("<KeyPress-Up>",    partial(self.on_key_press_arrow, Int2( 0, -1)))
        self.tk_canvas.bind("<KeyPress-Down>",  partial(self.on_key_press_arrow, Int2( 0,  1)))
        self.tk_canvas.bind("<KeyPress-Left>",  partial(self.on_key_press_arrow, Int2(-1,  0)))
        self.tk_canvas.bind("<KeyPress-Right>", partial(self.on_key_press_arrow, Int2( 1,  0)))

        self.tk_canvas.bind("<Enter>", self.on_enter)
        self.tk_canvas.bind("<Leave>", self.on_leave)

    def grid(
        self,
        column:int = 0,
        row:int = 0,
    ) -> None:
        self.tk_canvas.grid(column=column, row=row, sticky=NSEW)
        self.tk_xview.grid(column=column, row=row+1, sticky=EW)
        self.tk_yview.grid(column=column+1, row=row, sticky=NS)
        self.tk_global_scale_label.grid(column=column, row=row+2, columnspan=2,sticky=E)

    @property
    def global_scale(self) -> float:
        return self.global_scales[self.global_scale_index] / 100.0

    @property
    def scrollregion(self) -> FloatBoundingBox:
        """スクロール領域・範囲を取得

        Returns:
            FloatBoundingBox: スクロール領域・範囲
        """
        max_width  = max([layer.size2.w for layer in self.layers] + [0])
        max_height = max([layer.size2.h for layer in self.layers] + [0])
        scrollregion = self.create_scrollregion(max_width, max_height)
        return FloatBoundingBox(*scrollregion)

    @property
    def xview(self) -> FloatMinMax:
        """_summary_

        Returns:
            FloatMinMax: _description_
        """
        return FloatMinMax(*self.tk_canvas.xview())

    @property
    def yview(self) -> FloatMinMax:
        """_summary_

        Returns:
            FloatMinMax: _description_
        """
        return FloatMinMax(*self.tk_canvas.yview())

    @property
    def canvas_width(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self.tk_canvas.winfo_width()

    @property
    def canvas_height(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self.tk_canvas.winfo_height()

    def on_xview(self, *args) -> None:
        """水平・横スクロールバーのSCROLLとMOVETO
        """
        # 現在の位置をピクセル単位で取得
        pos = self.xview.minimum * self.scrollregion.width

        # スクロール移動の適用
        self.tk_canvas.xview(*args)

        # 移動後の位置をピクセル単位で取得
        new_pos = self.xview.minimum * self.scrollregion.width

        # レイヤーウィンドウの位置を固定化するために移動量で相殺
        self.tk_canvas.move(self.layers_window_lid, new_pos - pos, 0)

    def on_yview(self, *args) -> None:
        """垂直・縦スクロールバーのSCROLLとMOVETO
        """
        # 現在の位置をピクセル単位で取得
        pos = self.yview.minimum * self.scrollregion.height

        # スクロール移動の適用
        self.tk_canvas.yview(*args)

        # 移動後の位置をピクセル単位で取得
        new_pos = self.yview.minimum * self.scrollregion.height

        # レイヤーウィンドウの位置を固定化するために移動量で相殺
        self.tk_canvas.move(self.layers_window_lid, 0, new_pos - pos)

    def on_mouse_wheel(self, event:tk.Event) -> None:
        """マウスホイール

        Args:
            event (tk.Event): イベントプロパティ
        """
        scrollregion = self.scrollregion

        yview = self.yview.minimum

        # キャンバスの位置をホイール方向に合わせて上下移動
        self.tk_canvas.yview_scroll(-int(event.delta / abs(event.delta)), UNITS)

        new_yview = self.yview.minimum

        yview_pixel = yview * scrollregion.height
        new_yview_pixel = new_yview * scrollregion.height
        ydiff_pixel = new_yview_pixel - yview_pixel

        self.tk_canvas.move(self.layers_window_lid, 0, ydiff_pixel)

    def on_shift_mouse_wheel(self, event:tk.Event) -> None:
        """Shift押下＆マウスホイール

        Args:
            event (tk.Event): イベントプロパティ
        """
        scrollregion = self.scrollregion

        xview = self.xview.minimum

        # キャンバスの位置をホイール方向に合わせて左右移動
        self.tk_canvas.xview_scroll(-int(event.delta / abs(event.delta)), UNITS)

        new_xview = self.xview.minimum

        xview_pixel = xview * scrollregion.width
        new_xview_pixel = new_xview * scrollregion.width
        xdiff_pixel = new_xview_pixel - xview_pixel

        self.tk_canvas.move(self.layers_window_lid, xdiff_pixel, 0)

    def on_control_mouse_wheel(self, event:tk.Event) -> None:
        """Ctrl押下＆マウスホイール

        Args:
            event (tk.Event): イベントプロパティ
        """

        # スケール前の情報を取得
        prev_scrollregion = self.scrollregion
        prev_xview = self.xview
        prev_yview = self.yview
        prev_xpos = prev_xview * prev_scrollregion.width
        prev_ypos = prev_yview * prev_scrollregion.height

        # スケール値を更新
        self.global_scale_index += (1 if event.delta > 0 else -1)
        self.global_scale_index = clamp(self.global_scale_index, 0, len(self.global_scales) - 1)
        self.global_scale_var.set(f"{int(self.global_scales[self.global_scale_index])}%")

        # 全レイヤーにスケール適用
        if (global_scale:=self.global_scale):  # NOTE: C++のスコープ寿命とは違うけど書き方が好きだから
            for layer in self.layers:
                layer.apply_scale(global_scale)

        # 画像更新
        self.update_scene_color()

        # スケール後の情報を取得
        new_scrollregion = self.scrollregion
        new_xview = self.xview
        new_yview = self.yview
        new_xpos = new_xview * new_scrollregion.width
        new_ypos = new_yview * new_scrollregion.height

        # LayersWindowの移動量
        velocity = Float2.zero()

        if   ((eps:=prev_scrollregion.width - prev_xpos.maximum) != 0.0 or prev_xview.maximum == 1.0) and (new_xview.maximum == 1.0):
            # スケール前後で発生したスクロール範囲(xmax | 右端)の差分の打ち消し + 誤差(主にマウス中央ボタン移動)の打ち消し
            velocity.x = (new_scrollregion.xmax - prev_scrollregion.xmax) + eps
        elif ((eps:=new_xpos.maximum        - prev_xpos.maximum) != 0.0 or prev_xview.minimum == 0.0) and (new_xview.minimum == 0.0):
            # スケール前後で発生したスクロール範囲(xmin | 左端)の差分の打ち消し + 誤差(主にマウス中央ボタン移動)の打ち消し
            velocity.x = (new_scrollregion.xmin - prev_scrollregion.xmin) + eps

        if   ((eps:=prev_scrollregion.height - prev_ypos.maximum) != 0.0 or prev_yview.maximum == 1.0) and (new_yview.maximum == 1.0):
            # スケール前後で発生したスクロール範囲(ymax | 下端)の差分の打ち消し + 誤差(主にマウス中央ボタン移動)の打ち消し
            velocity.y = (new_scrollregion.ymax - prev_scrollregion.ymax) + eps
        elif ((eps:=new_ypos.maximum         - prev_ypos.maximum) != 0.0 or prev_yview.minimum == 0.0) and (new_yview.minimum == 0.0):
            # スケール前後で発生したスクロール範囲(ymin | 上端)の差分の打ち消し + 誤差(主にマウス中央ボタン移動)の打ち消し
            velocity.y = (new_scrollregion.ymin - prev_scrollregion.ymin) + eps

        # LayersWindowの位置を固定化するための相殺移動
        self.tk_canvas.move(self.layers_window_lid, *velocity)

    def on_mouse_motion(self, event:tk.Event) -> None:
        """マウスカーソル移動

        Args:
            event (tk.Event): イベントプロパティ
        """
        if self.button_flags == self.BUTTON_NONE:
            return

        if len(self.layers) == 0:
            return

        new_cursor_xy = Int2(event.x_root, event.y_root)

        scale = 100.0 / self.global_scales[self.global_scale_index]

        velocity = (new_cursor_xy - self.cursor_xy)

        if velocity.x == 0 and velocity.y == 0:
            return

        if self.button_flags & self.BUTTON_CENTER_PRESS:
            scrollregion = self.scrollregion

            xview_upper, xview_lower = self.tk_canvas.xview()
            yview_upper, yview_lower = self.tk_canvas.yview()

            new_xview_upper = xview_upper - velocity.x / scrollregion.width
            new_yview_upper = yview_upper - velocity.y / scrollregion.height
            new_xview_lower = xview_lower - velocity.x / scrollregion.width
            new_yview_lower = yview_lower - velocity.y / scrollregion.height

            if new_xview_lower < 1.0 and new_yview_upper > 0.0 and new_yview_lower < 1.0 and new_xview_upper > 0.0:
                self.tk_canvas.xview_moveto(new_xview_upper)
                self.tk_canvas.yview_moveto(new_yview_upper)

                xview_pixel = xview_upper * scrollregion.width
                yview_pixel = yview_upper * scrollregion.height

                new_xview_pixel = new_xview_upper * scrollregion.width
                new_yview_pixel = new_yview_upper * scrollregion.height

                xdiff_pixel = new_xview_pixel - xview_pixel
                ydiff_pixel = new_yview_pixel - yview_pixel

                self.tk_canvas.move(self.layers_window_lid, xdiff_pixel, ydiff_pixel)
        elif (layer:=self.get_selecting_layer()) is not None:
            if not layer.is_fixed_position:
                layer.position += velocity * scale  # レイヤー位置はスケールを考慮します。
                self.update_scene_color()

        self.cursor_xy = new_cursor_xy

    def on_left_button_press(self, event:tk.Event) -> None:
        """マウス左ボタンをクリックした瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        # 複数アクションは現状禁止
        if self.button_flags != self.BUTTON_NONE:
            return

        self.cursor_xy = Int2(event.x_root, event.y_root)

        # マウス左ボタン押下中を立てる
        self.button_flags |= self.BUTTON_LEFT_PRESS

    def on_left_button_release(self, event:tk.Event) -> None:
        """マウス左ボタンを離した瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        # マウス左ボタン押下中の削除
        self.button_flags &= ~self.BUTTON_LEFT_PRESS

    def on_center_button_press(self, event:tk.Event) -> None:
        """マウス中央ボタンをクリックした瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        # 複数アクションは現状禁止
        if self.button_flags != self.BUTTON_NONE:
            return

        self.cursor_xy = Int2(event.x_root, event.y_root)

        # マウス中央ボタン押下中を立てる
        self.button_flags |= self.BUTTON_CENTER_PRESS

    def on_center_button_release(self, event:tk.Event) -> None:
        """マウス中央ボタンを離した瞬間

        Args:
            event (tk.Event): イベントプロパティ
        """
        # マウス中央ボタン押下中の削除
        self.button_flags &= ~self.BUTTON_CENTER_PRESS

    def on_configure(self, event:tk.Event) -> None:
        """ウィンドウサイズの変更

        Args:
            event (tk.Event): イベントプロパティ
        """
        scrollregion = self.scrollregion

        # 背景サイズとスクロール範囲を更新
        self.tk_canvas.coords(self.bg_iid, *scrollregion)
        self.tk_canvas.configure(scrollregion=tuple(scrollregion))

        velocity = Float2.zero()

        # レイヤーウィンドウのBoundingBoxを取得
        bbox = BoundingBox(*self.tk_canvas.bbox(self.layers_window_lid))

        # LayersWindowの移動量
        # レイヤーウィンドウのBoundingBoxを取得
        bbox = BoundingBox(*self.tk_canvas.bbox(self.layers_window_lid))

        xview = self.xview * self.scrollregion.width + scrollregion.xmin
        yview = self.yview * self.scrollregion.height + scrollregion.ymin

        # if   : 右制限
        # elif : 左制限
        if bbox.xmax > xview.maximum:
            velocity.x = xview.maximum - bbox.xmax
        elif bbox.xmin < xview.minimum:
            velocity.x = xview.minimum - bbox.xmin

        # if   : 上制限
        # elif : 下制限
        if bbox.ymin < yview.minimum:
            velocity.y = yview.minimum - bbox.ymin
        elif bbox.ymax > yview.maximum:
            velocity.y = yview.maximum - bbox.ymax

        # レイヤーウィンドウを画面外に出ないように移動
        self.tk_canvas.move(self.layers_window_lid, velocity.x, velocity.y)

    def on_key_press_arrow(self, velocity:Int2, event:tk.Event) -> None:
        """矢印の押下

        Args:
            velocity (Int2): 押下した方向
            event (tk.Event): イベントプロパティ
        """
        if (layer:=self.get_selecting_layer()) is not None:
            if not layer.is_fixed_position:
                layer.position += velocity
                self.update_scene_color()

    def on_enter(self, event:tk.Event) -> None:
        """マウスカーソルがウィンドウ内に進入

        Args:
            event (tk.Event): イベントプロパティ
        """
        self.tk_canvas.focus_set()

    def on_leave(self, event:tk.Event) -> None:
        """マウスカーソルがウィンドウ外に退出

        Args:
            event (tk.Event): イベントプロパティ
        """
        pass

    def on_layers(self, velocity:Int2) -> None:
        """レイヤーウィンドウを移動させた際のイベント

        Args:
            velocity (Int2): 移動量
        """
        scrollregion = self.scrollregion

        # レイヤーウィンドウのBoundingBoxを取得
        bbox = BoundingBox(*self.tk_canvas.bbox(self.layers_window_lid))

        xview = self.xview * self.scrollregion.width + scrollregion.xmin
        yview = self.yview * self.scrollregion.height + scrollregion.ymin

        # if   : 右制限
        # elif : 左制限
        if bbox.xmax + velocity.x > xview.maximum:
            velocity.x = 0
        elif bbox.xmin + velocity.x < xview.minimum:
            velocity.x = 0

        # if   : 上制限
        # elif : 下制限
        if bbox.ymin + velocity.y < yview.minimum:
            velocity.y = 0
        elif bbox.ymax + velocity.y > yview.maximum:
            velocity.y = 0

        # レイヤーウィンドウを画面外に出ないように移動
        self.tk_canvas.move(self.layers_window_lid, velocity.x, velocity.y)

    def on_update_layer(self, lid:LayerId, depth:int, blend_mode:BlendMode, is_visible:bool) -> None:
        """レイヤー設定の更新

        Args:
            lid (LayerId): レイヤーID
            depth (int): レイヤーの深さ
            blend_mode (BlendMode): ブレンドモード
            is_visible (bool): 可視性
        """
        for layer in self.layers:
            if layer.lid == lid:
                layer.depth = depth
                layer.blend_mode = blend_mode
                layer.is_visible = is_visible
                self.update_scene_color()
                break

    def create_lid(self) -> LayerId:
        """レイヤーIDの作成

        Returns:
            LayerId: レイヤーID
        """
        # 空きレイヤーIDがある場合はそれを使用.
        # 空きがない場合は現在のレイヤー数から.
        return self.empty_lids.pop() if len(self.empty_lids) > 0 else LayerId(len(self.layers) if len(self.layers) > 0 else 0)

    def create_depth(self) -> int:
        return max([layer.depth for layer in self.layers]) + 1 if len(self.layers) > 0 else 0

    def find_layer(self, lid:LayerId) -> Optional[LayerInfo]:
        """レイヤーIDのレイヤーを探します

        Args:
            lid (LayerId): レイヤーID

        Returns:
            Optional[LayerInfo]: 見つからない場合はNoneを返します。
        """
        for layer in self.layers:
            if layer.lid == lid:
                return layer
        return None

    def get_selecting_layer(self) -> Optional[LayerInfo]:
        """選択中のレイヤーを取得

        Returns:
            Optional[LayerInfo]: レイヤーが未選択の場合はNoneを返します。
        """
        if (select_lid:=self.tk_layers_window.get_selecting_layer_id()) is not None:
            for layer in self.layers:
                if layer.lid == select_lid:
                    return layer
        # 選択中のレイヤーがない or レイヤーIDが見つからない
        return None

    def add_new_layer_with_image(
        self,
        image:npt.NDArray[np.uint8],
    ) -> LayerId:
        """画像から新規レイヤーの作成

        Args:
            image (npt.NDArray[np.uint8]): 画像 (RGBA)

        Returns:
            LayerId: レイヤーID、レイヤー操作で使用します。
        """
        layer = LayerInfo(
            lid=self.create_lid(),
            image=image,
            depth=self.create_depth(),
            blend_mode=BlendMode.NORMAL,
        )
        self.tk_layers_window.add_layer(layer.image, layer_name=None, layer_id=layer.lid, depth=layer.depth, blend_mode=layer.blend_mode)
        self.layers.append(layer)
        return layer.lid

    def update_layer_image(self, lid:LayerId, image:npt.NDArray[np.uint8], is_update_scene_color:bool = True) -> None:
        """レイヤーの画像を更新

        Args:
            lid (LayerId): レイヤーID
            image (npt.NDArray[np.uint8]): 画像 (RGBA)
            is_update_scene_color (bool, optional): SceneColorを更新するか. Defaults to True.
        """
        # レイヤーを探します
        if (layer:=self.find_layer(lid)) is None:
            return

        # 画像更新
        layer.update_image(image)

        # サムネ画像の更新
        self.tk_layers_window.set_thumbnail_image(lid, image)

        # 描画更新
        if is_update_scene_color:
            self.update_scene_color()

    def update_layer_info(
        self,
        lid:LayerId,
        layer_name:Optional[str] = None,
        is_fixed_position:Optional[bool] = None,
        is_visible:Optional[bool] = None,
    ) -> None:
        """レイヤーの設定を更新

        Args:
            lid (LayerId): レイヤーID
            layer_name (Optional[str], optional): レイヤー名. Defaults to None.
            is_fixed_position (Optional[bool], optional): レイヤーの位置を固定化するか. Defaults to None.
            is_visible (Optional[bool], optional): レイヤーの可視性. Defaults to None.
        """
        # レイヤーを探します
        if (layer:=self.find_layer(lid)) is None:
            return

        # レイヤー設定の更新
        if layer_name is not None:
            self.tk_layers_window.set_layer_name(lid, layer_name)
        if is_fixed_position is not None:
            layer.is_fixed_position = is_fixed_position
        if is_visible is not None:
            layer.is_visible = is_visible
            self.tk_layers_window.set_is_visible(lid, is_visible)

    def create_scrollregion(self, width:int, height:int) -> tuple[float, float, float, float]:
        """画像のハーフサイズまでスクロール可能な範囲を作成します。

        画像のハーフサイズがキャンバスのハーフサイズに満たない場合は、キャンバスの中央

        画像のハーフサイズまでスクロール可能
        ただしキャンバスのハーフサイズを超過する場合は、キャンバスのハーフサイズまでしかスクロールできません。

        Args:
            width (int): 画像の横幅
            height (int): 画像の縦幅

        Returns:
            tuple[int, int, int, int]: 範囲 (w, n, e, s)
        """
        image_full_size_width = width
        image_full_size_height = height

        # NOTE: 小数点を許容するとLayerWindowの相対移動に誤差発生するので禁止です.
        image_half_size_width = math.ceil(image_full_size_width * 0.5)
        image_half_size_height = math.ceil(image_full_size_height * 0.5)

        canvas_full_size_width = self.canvas_width
        canvas_full_size_height = self.canvas_height

        canvas_half_size_width = math.ceil(canvas_full_size_width * 0.5)
        canvas_half_size_height = math.ceil(canvas_full_size_height * 0.5)

        diff_size_width = canvas_full_size_width - image_full_size_width
        diff_size_height = canvas_full_size_height - image_full_size_height

        w = min(-image_half_size_width - diff_size_width, -canvas_half_size_width)
        n = min(-image_half_size_height - diff_size_height, -canvas_half_size_height)

        e = image_full_size_width + max(image_half_size_width + diff_size_width, canvas_half_size_width)
        s = image_full_size_height + max(image_half_size_height + diff_size_height, canvas_half_size_height)

        return float(w), float(n), float(e), float(s)

    def update_scene_color(self):
        """レイヤー情報を元にSceneColorを更新
        """
        max_width  = max([layer.size2.w for layer in self.layers] + [0])
        max_height = max([layer.size2.h for layer in self.layers] + [0])

        scene_color = np.full((max_height, max_width, 3), (255, 255, 255), np.uint8)

        for layer in sorted(self.layers, key=lambda layer:layer.depth):
            if not layer.is_visible:  # 可視性が無効なレイヤーはスキップ
                continue

            # 始点が画面外の場合、座標の符号は負.
            # 絶対値を取ることで画面外部分を切り取る.
            src_xmin = abs(layer.position2.x) if layer.position2.x < 0 else 0
            src_ymin = abs(layer.position2.y) if layer.position2.y < 0 else 0

            src_xmax = layer.size2.w - max(0, layer.xmax2 - max_width)
            src_ymax = layer.size2.h - max(0, layer.ymax2 - max_height)

            dst_xmin = max(0, layer.position2.x)
            dst_ymin = max(0, layer.position2.y)

            dst_xmax = min(max_width,  layer.xmax2)
            dst_ymax = min(max_height, layer.ymax2)

            src_width  = src_xmax - src_xmin
            src_height = src_ymax - src_ymin

            dst_width  = dst_xmax - dst_xmin
            dst_height = dst_ymax - dst_ymin

            if layer.depth == 1:
                pass

            if src_width < 0 or dst_width < 0 or src_height < 0 or dst_height < 0:
                continue

            if layer.blend_mode is BlendMode.DIFFERENCE:
                base  = scene_color[dst_ymin:dst_ymax, dst_xmin:dst_xmax].astype(np.float64)
                blend = layer.color[src_ymin:src_ymax, src_xmin:src_xmax].astype(np.float64)
                alpha = layer.alpha[src_ymin:src_ymax, src_xmin:src_xmax] / 255.0
                result = np.clip(np.abs(base - blend * alpha), 0.0, 255.0).astype(np.uint8)
                scene_color[dst_ymin:dst_ymax, dst_xmin:dst_xmax] = result
            elif layer.blend_mode is BlendMode.NORMAL:
                scene_color[dst_ymin:dst_ymax, dst_xmin:dst_xmax] = alpha_composite(
                    layer.color[src_ymin:src_ymax, src_xmin:src_xmax],
                    scene_color[dst_ymin:dst_ymax, dst_xmin:dst_xmax],
                    layer.alpha[src_ymin:src_ymax, src_xmin:src_xmax] / 255.0,
                )
            else:
                assert False, f"{layer.blend_mode} is an unsupported blend mode."

        new_scrollregion = self.create_scrollregion(max_width, max_height)

        # 背景を更新
        self.tk_canvas.coords(self.bg_iid, *new_scrollregion)

        # Image to PhotoImage
        scene_color = Image.fromarray(scene_color, mode="RGB")
        scene_color = ImageTk.PhotoImage(scene_color)

        # 画像を更新
        # NOTE: 先にscene_colorを上書きするとImageTkが一瞬消失して暗転の原因になります.
        # NOTE: itemconfigより先にscene_colorをセットするとscene_color_iidにセットしたImageTkが一瞬消失して暗転の原因になります。
        self.tk_canvas.itemconfig(self.scene_color_iid, image=scene_color)
        self.scene_color = scene_color

        # スクロール範囲を更新
        self.tk_canvas.configure(scrollregion=new_scrollregion)
