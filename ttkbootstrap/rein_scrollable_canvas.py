import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import numpy as np
import numpy.typing as npt
from typing import Optional
from PIL import Image, ImageTk



__all__ = [
    "ScrollableCanvas",
]


class ScrollableCanvas(ttk.Canvas):
    """スクロール可能なキャンバス
    """
    def __init__(
        self,
        master:tk.Misc,
        *args,
        **kwargs,
    ) -> None:
        """コンストラクタ

        Args:
            master (tk.Misc): master
        """
        super().__init__(master, *args, *kwargs)

        # NOTE: ImageTk.PhotoImageは所有権が曖昧なので明示的にselfで所持します。
        self.iid:Optional[int] = None
        self.image:Optional[ImageTk.PhotoImage] = None

        self.xscrollbar = ttk.Scrollbar(master, orient=HORIZONTAL, command=self.xview)
        self.yscrollbar = ttk.Scrollbar(master, orient=VERTICAL,   command=self.yview)

        # キャンバス内の描画物をスクロールバーに連動させる
        self.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        # bind events
        self.bind("<MouseWheel>",       self.on_mouse_wheel)
        self.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)

    def grid(self, column:int = 0, row:int = 0) -> None:
        """grid layout

        内部で Scrollbar を保有しているため grid レイアウトする場合は columnspan, rowspan で調整してください。

        Args:
            column (int, optional): 列位置. Defaults to 0.
            row (int, optional): 行位置. Defaults to 0.
        """
        super().grid(column=column, row=row, sticky=NSEW)
        self.xscrollbar.grid(column=column,     row=row + 1, sticky=NSEW)
        self.yscrollbar.grid(column=column + 1, row=row,     sticky=NSEW)

    def on_mouse_wheel(self, event:tk.Event) -> None:
        """マウスホイール

        Args:
            event (tk.Event): イベントプロパティ
        """
        self.yview_scroll(-int(event.delta / abs(event.delta)), UNITS)

    def on_shift_mouse_wheel(self, event:tk.Event) -> None:
        """Shift押下＆マウスホイール

        Args:
            event (tk.Event): イベントプロパティ
        """
        self.xview_scroll(-int(event.delta / abs(event.delta)), UNITS)

    def set_pil_image(self, image:Image.Image) -> None:
        """PILで読み込んだ画像をセット

        Args:
            image (Image.Image): PILで読み込んだ画像
        """
        # to RGB
        if image.mode == "RGBA":
            image = image.convert("RGB")  # no need to copy
        elif image.mode == "L":
            image = image.convert("RGB")  # no need to copy

        # NOTE: この時点で self.image に突っ込むと直前の ImageTk.PhotoImage が消失して一瞬暗転する可能性ある。
        tmp_image = ImageTk.PhotoImage(image)

        # if:   画像を貼り付けるアイテムがない場合は新規作成
        # else: アイテムがある場合は新しい画像に切り替え
        if self.iid is None:
            self.iid = self.create_image(0, 0, anchor=NW, image=tmp_image)
        else:
            self.itemconfig(self.iid, image=tmp_image)

        # NOTE: アイテムにセットし終えてから直前の self.image を破棄する
        self.image = tmp_image

        # スクロール可能な範囲を画像サイズに合わせる
        self.configure(scrollregion=(0, 0, self.image.width(), self.image.height()))

    def set_cv2_image(self, image:npt.NDArray[np.uint8]) -> None:
        """OpenCVで読み込んだ画像をセット

        画像はGrayscaleないしBGR配置で渡されることを想定しています。

        Args:
            image (npt.NDArray[np.uint8]): OpenCVで読み込んだ画像
        """
        image = image.copy()

        if (shape_length:=len(image.shape)) == 2:
            c = 1
        elif shape_length == 3:
            _, _, c = image.shape
        else:
            return

        # delete alpha dim
        if c == 4:
            image = np.delete(image, 3, 2)
            _, _, c = image.shape

        # if:   BGR to RGB
        # elif: GRAY to RGB
        # else: not support format.
        if c == 3:
            image = image[:, :, ::-1]
        elif c == 1:
            image = np.repeat(image[:, :, np.newaxis], 3, 2)
        else:
            return

        # numpy to pil
        self.set_pil_image(Image.fromarray(image, "RGB"))

    def set_image(self, image:Optional[Image.Image | npt.NDArray[np.uint8]]) -> None:
        """画像をセット

        image に None をセットした場合は画像を削除します。

        Args:
            image (Optional[Image.Image  |  npt.NDArray[np.uint8]]): PILかOpenCVで読み込んだ画像
        """
        if isinstance(image, Image.Image):
            self.set_pil_image(image)
        elif isinstance(image, np.ndarray):
            self.set_cv2_image(image)
        elif image is None:
            self.remove_image()

    def remove_image(self) -> None:
        """画像を削除
        """
        if self.iid is None or self.image is None:  # no image
            return

        # remove items
        self.delete(self.iid)
        self.iid, self.image = None, None

        # reset scrollregion
        self.configure(scrollregion=(0, 0, 0, 0))

    def delete_image(self) -> None:
        """画像を削除
        """
        self.remove_image()
