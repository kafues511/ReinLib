from typing import Optional, Self
from PIL import ImageFont
from dataclasses import dataclass, field

from reinlib.types.rein_color_method import ColorMethod
from reinlib.types.rein_int2 import Int2
from reinlib.types.rein_color import Color
from reinlib.types.rein_bounding_box import BoundingBox


__all__ = [
    "TextLayout",
]


@dataclass
class TextLayout:
    # フォント
    font:Optional[ImageFont.FreeTypeFont] = None

    # 文字色
    color:Color = field(default_factory=lambda: Color.white())

    # 縁取りの有効性
    is_outline:bool = False
    # 縁取りの色
    outline_color:Color = field(default_factory=lambda: Color.black())
    # 縁取りの太さ
    outline_weight:int = 1

    # 影の有効性
    is_shadow:bool = False
    # 影の色
    shadow_color:Color = field(default_factory=lambda: Color.black())
    # 影の太さ
    shadow_weight:int = 0
    # 影の位置
    # オフセットで指定します。
    shadow_offset:Int2 = field(default_factory=lambda: Int2.one())

    # 文字寄せ
    anchor:Optional[str] = None
    # 行間サイズ
    spacing:int = 0

    # 文字領域の中央値
    median_bbox:Optional[BoundingBox] = None

    @property
    def font_size(self) -> int:
        """フォントサイズを取得

        Returns:
            int: フォントサイズ
        """
        return self.font.size if self.font is not None else 0

    def is_valid(self) -> bool:
        """有効性の判定

        Returns:
            bool: 有効な場合はTrueを返します。
        """
        return self.font is not None

    def get_color(self, color_method:ColorMethod) -> int | tuple[int, int, int] | tuple[int, int, int, int]:
        """文字色を取得

        Args:
            color_method (ColorMethod): _description_

        Returns:
            int | tuple[int, int, int] | tuple[int, int, int, int]: 文字色
        """
        if color_method is ColorMethod.GRAYSCALE:
            return self.color.grayscale
        elif color_method is ColorMethod.COLOR:
            return self.color.rgb
        elif color_method is ColorMethod.ALPHA:
            return self.color.rgba
        else:
            assert False, "not support color method."

    def get_outline_color(self, color_method:ColorMethod) -> int | tuple[int, int, int] | tuple[int, int, int, int]:
        """縁取り色を取得

        Args:
            color_method (ColorMethod): _description_

        Returns:
            int | tuple[int, int, int] | tuple[int, int, int, int]: 縁取り色
        """
        if color_method is ColorMethod.GRAYSCALE:
            return self.outline_color.grayscale
        elif color_method is ColorMethod.COLOR:
            return self.outline_color.rgb
        elif color_method is ColorMethod.ALPHA:
            return self.outline_color.rgba
        else:
            assert False, "not support color method."

    def get_shadow_offset(self) -> Int2:
        """影のオフセットを取得

        文字描画位置に対してのオフセットです。

        Returns:
            Int2: 影のオフセット
        """
        return self.shadow_offset if self.is_shadow else Int2.zero()

    def get_shadow_color(self, color_method:ColorMethod) -> int | tuple[int, int, int] | tuple[int, int, int, int]:
        """影色を取得

        Args:
            color_method (ColorMethod): _description_

        Returns:
            int | tuple[int, int, int] | tuple[int, int, int, int]: 影色
        """
        if color_method is ColorMethod.GRAYSCALE:
            return self.shadow_color.grayscale
        elif color_method is ColorMethod.COLOR:
            return self.shadow_color.rgb
        elif color_method is ColorMethod.ALPHA:
            return self.shadow_color.rgba
        else:
            assert False, "not support color method."

    def get_outline_weight(self) -> int:
        """縁取りの太さを取得

        Returns:
            int: 縁取りが無効な場合は0を返します。
        """
        return self.outline_weight if self.is_outline else 0

    def get_shadow_weight(self) -> int:
        """影の太さを取得

        Returns:
            int: 影が無効な場合は0を返します。
        """
        return self.shadow_weight if self.is_shadow else 0

    def get_max_weight(self) -> int:
        """最大の太さを取得

        Returns:
            int: 縁取り、影の太い方
        """
        return max(self.get_outline_weight(), self.get_shadow_weight())

    def get_outline_alpha(self) -> int:
        """縁取りの透明度を取得

        Returns:
            int: 透明度
        """
        return self.outline_color.alpha if self.is_outline else 255

    def get_shadow_alpha(self) -> int:
        """影の透明度を取得

        Returns:
            int: 透明度
        """
        return self.shadow_color.alpha if self.is_shadow else 255
