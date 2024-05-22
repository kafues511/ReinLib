import numpy as np
import numpy.typing as npt
from typing import Optional
from PIL import ImageFont, ImageDraw
from collections.abc import Generator

from reinlib.types.rein_color_method import ColorMethod
from reinlib.types.rein_color import Color
from reinlib.types.rein_int2 import Int2
from reinlib.types.rein_bounding_box import BoundingBox
from reinlib.types.rein_text_layout import TextLayout


__all__ = [
    "calc_median_bbox",
    "calc_character_bbox",
    "calc_character_bboxes",
    "draw_simple_text",
    "draw_text_layout",
    "apply_font_decoration",
    "find_smallest_bounding_rectangle",
]


def calc_median_bbox(
    characters:str | list[str] | tuple[str, ...] | Generator[str, None, None],
    font:ImageFont.FreeTypeFont,
    anchor:str = "ls",
) -> BoundingBox:
    """文字領域の中央値を取得

    Args:
        characters (str | list[str] | tuple[str, ...] | Generator[str, None, None]): 中央値算出に使用する文字列
        font (ImageFont.FreeTypeFont): フォント
        anchor (str, optional): 文字寄せ. Defaults to "ls".

    Returns:
        BoundingBox: 文字領域の中央値
    """
    return BoundingBox(*np.median([
        font.getbbox(character, anchor=anchor)
        for character in characters
    ], axis=0).astype(np.int64).tolist())


def calc_character_bbox(
    text_pos:Int2,
    character:str,
    font:ImageFont.FreeTypeFont,
    anchor:str,
    median_bbox:BoundingBox,
) -> BoundingBox:
    """文字領域の中央値を考慮した文字領域を計算

    Args:
        text_pos (Int2): 文字描画位置
        character (str): 文字
        font (ImageFont.FreeTypeFont): フォント
        anchor (str): 文字寄せ
        median_bbox (BoundingBox): 文字領域の中央値

    Returns:
        BoundingBox: 文字領域
    """
    char_bbox = BoundingBox(*font.getbbox(character, anchor=anchor))

    xmin = text_pos.x + char_bbox.xmin
    ymin = text_pos.y + min(median_bbox.ymin, char_bbox.ymin)
    xmax = text_pos.x + char_bbox.xmax
    ymax = text_pos.y + max(median_bbox.ymax, char_bbox.ymax)

    return BoundingBox(xmin, ymin, xmax, ymax)


def calc_character_bboxes(
    text_pos:Int2,
    text:str,
    font:ImageFont.FreeTypeFont,
    anchor:str,
    median_bbox:BoundingBox,
    out_bboxes:list[BoundingBox],
) -> None:
    """文字列から文字単位の文字領域を計算

    Args:
        text_pos (Int2): 文字描画位置
        text (str): 文字列
        font (ImageFont.FreeTypeFont): フォント
        anchor (str): 文字寄せ
        median_bbox (BoundingBox): 文字領域の中央値
        out_bboxes (list[BoundingBox]): 文字領域の格納先
    """
    char_pos = Int2(*text_pos)

    for char in text:
        char_bbox = BoundingBox(*font.getbbox(char, anchor=anchor))

        if char != "　":
            xmin = char_pos.x + char_bbox.xmin
            ymin = char_pos.y + min(median_bbox.ymin, char_bbox.ymin)
            xmax = char_pos.x + char_bbox.xmax
            ymax = char_pos.y + max(median_bbox.ymax, char_bbox.ymax)

            out_bboxes.append(BoundingBox(xmin, ymin, xmax, ymax))

        char_pos.x += char_bbox.width


def draw_simple_text(
    drawer:ImageDraw.ImageDraw,
    text_pos:Int2,
    text:str,
    font:ImageFont.FreeTypeFont,
    fill:int | Color = 255,
    anchor:Optional[str] = None,
    spacing:int = 0,
) -> None:
    """シンプルなテキスト描画

    Args:
        drawer (ImageDraw.ImageDraw): ImageDraw
        text_pos (Int2): 描画位置
        text (str): テキスト
        font (ImageFont.FreeTypeFont): フォント
        fill (int, optional): 文字色 (グレースケール). Defaults to 255.
        anchor (Optional[str], optional): 文字寄せ. Defaults to None.
        spacing (int, optional): 行間. Defaults to 0.
    """
    drawer.text(text_pos.xy, text, fill, font, anchor, spacing)


def draw_text_layout(
    drawer:ImageDraw.ImageDraw,
    text_pos:Int2,
    text:str,
    layout:TextLayout,
    color_method:ColorMethod = ColorMethod.GRAYSCALE,
) -> None:
    """テキスト描画

    Args:
        drawer (ImageDraw.ImageDraw): ImageDraw
        text_pos (tuple[int, int]): 描画位置
        text (str): テキスト
        layout (TextLayout): レイアウト
        color_method (ColorMethod, optional): _description_. Defaults to ColorMethod.GRAYSCALE.
    """
    if layout.is_shadow:
        drawer.text(
            (text_pos + layout.get_shadow_offset()).xy,
            text,
            layout.get_shadow_color(color_method),
            layout.font,
            layout.anchor,
            layout.spacing,
            stroke_width=layout.shadow_weight,
            stroke_fill=layout.get_shadow_color(color_method),
        )

    if layout.is_outline:
        drawer.text(
            text_pos.xy,
            text,
            layout.get_color(color_method),
            layout.font,
            layout.anchor,
            layout.spacing,
            stroke_width=layout.outline_weight,
            stroke_fill=layout.get_outline_color(color_method),
        )
    else:
        drawer.text(
            text_pos.xy,
            text,
            layout.get_color(color_method),
            layout.font,
            layout.anchor,
            layout.spacing,
        )


def apply_font_decoration(
    bbox:BoundingBox,
    outline_weight:int,
    shadow_weight:int,
    shadow_offset:Int2,
) -> None:
    """フォント修飾を考慮してバウンディングボックスを再計算します。

    Args:
        bbox (BoundingBox): バウンディングボックス
        outline_weight (int): 縁取りの太さ
        shadow_weight (int): 影の太さ
        shadow_offset (Int2): 影の位置
    """
    if outline_weight == 0 and shadow_weight == 0 and shadow_offset.x == 0 and shadow_offset.y == 0:
        return

    bbox.xmin += min(-outline_weight, shadow_offset.x - shadow_weight)
    bbox.ymin += min(-outline_weight, shadow_offset.y - shadow_weight)
    bbox.xmax += max( outline_weight, shadow_offset.x + shadow_weight)
    bbox.ymax += max( outline_weight, shadow_offset.y + shadow_weight)


def find_smallest_bounding_rectangle(
    image:npt.NDArray[np.uint8],
    threshold:int,
) -> BoundingBox:
    """_summary_

    Args:
        image (npt.NDArray[np.uint8]): _description_
        threshold (int): _description_

    Returns:
        BoundingBox: _description_
    """
    mask = np.where(image > threshold)
    if len(mask[0]) == 0 and len(mask[1]) == 0:
        return BoundingBox(0, 0, *image.shape[::-1])

    ymin, xmin = np.min(mask, axis=1).tolist()
    ymax, xmax = np.max(mask, axis=1).tolist()
    return BoundingBox(xmin, ymin, xmax, ymax)
