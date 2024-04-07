import random
import numpy as np
import numpy.typing as npt
from PIL import Image

from reinlib.types.rein_int2 import Int2
from reinlib.types.rein_size2d import Size2D
from reinlib.types.rein_alpha_blend_mode import AlphaBlendMode
from reinlib.utility.rein_math import lerp


__all__ = [
    "random_pil_crop",
    "alpha_composite",
    "create_gradient_alpha",
]


def random_pil_crop(
    image:Image.Image,
    crop_size:Size2D,
    crop_step:Int2,
    resize_resample:Image.Resampling = Image.Resampling.BILINEAR,
) -> Image.Image:
    """画像のランダム切り抜き

    Args:
        image (Image.Image): 画像
        crop_size (Size2D): 切り抜きサイズ
        crop_step (Int2): 切り抜き開始位置のランダム幅
        resize_resample (Image.Resampling, optional): 画像サイズが切り抜きサイズ未満のリサイズ補間法. Defaults to Image.Resampling.BILINEAR.

    Returns:
        Image.Image: 切り抜き後の画像
    """
    image_size = Size2D(*image.size)

    # resize if smaller than crop size
    if image_size.width < crop_size.width or image_size.height < crop_size.height:
        pixels = crop_size.width - image_size.width if image_size.width < crop_size.width else crop_size.height - image_size.height
        image = image.resize((image_size.width + pixels, image_size.height + pixels), resample=resize_resample)
        image_size = Size2D(*image.size)  # update image size

    # set crop point
    x_range, y_range = image_size.width - crop_size.width, image_size.height - crop_size.height
    x, y = random.randrange(0, x_range + 1, crop_step.x), random.randrange(0, y_range + 1, crop_step.y)

    return image.crop((x, y, x + crop_size.width, y + crop_size.height))


def alpha_composite(
    src:npt.NDArray[np.uint8],
    dst:npt.NDArray[np.uint8],
    alpha:npt.NDArray[np.float32 | np.float64],
    mode:AlphaBlendMode=AlphaBlendMode.STRAIGHT,
) -> npt.NDArray[np.uint8]:
    """透明度合成

    Args:
        src (npt.NDArray[np.uint8]): Base
        dst (npt.NDArray[np.uint8]): Blend
        alpha (npt.NDArray[np.float32 | np.float64]): 透明度
        mode (AlphaBlendMode, optional): 合成方法. Defaults to AlphaBlendMode.STRAIGHT.

    Returns:
        npt.NDArray[np.uint8]: 合成結果
    """
    if mode is AlphaBlendMode.STRAIGHT:
        result = (src * alpha) + (dst * (1.0 - alpha))
    elif mode is AlphaBlendMode.PREMULTIPLIED:
        result = src + (dst * (1.0 - alpha))
    else:
        assert False, f"not support mode, {mode}."

    return np.clip(result, 0.0, 255.0).astype(np.uint8)


def create_gradient_alpha(
    size:Size2D,
    top_alpha:int,
    bottom_alpha:int,
    is_shape_newaxis:bool = True,
    is_float64:bool = True,
) -> npt.NDArray[np.uint8 | np.float64]:
    """上部から下部にかけて線形補間な透明度を作成

    Args:
        size (Size2): 画像サイズ
        top_alpha (int): 上部の透明度 (0 ~ 255)
        bottom_alpha (int): 下部の透明度 (0 ~ 255)
        is_shape_newaxis (bool, optional): (h, w, 1) を要求する場合はTrue, (h, w) の場合はFalse. Defaults to True.
        is_float64 (bool, optional): [0.0 ~ 1.0] を要求する場合はTrue, [0 ~ 255] の場合はFalse Defaults to False.

    Returns:
        npt.NDArray[np.uint8 | np.float64]: 透明度
    """
    # 上部から下部のグラデーションを作成
    alpha = [lerp(top_alpha, bottom_alpha, y_pos / size.height) for y_pos in range(size.height)]
    alpha = np.tile(alpha, (size.width, 1))
    alpha = np.transpose(alpha, (1, 0))
    if is_shape_newaxis:
        alpha = alpha[..., np.newaxis]
    if not is_float64:
        alpha = alpha.astype(np.uint8)
    else:
        alpha = alpha / 255.0
    return alpha
