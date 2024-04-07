# ReinLib

主にReinVisionOCRで使用している汎用型や関数などを纏めたライブラリです。

標準モジュール名と重複を防ぐためにファイル名の頭文字に `rein_` を付与しています。

```
.
└── reinlib
    ├── ttkbootstrap
    │   ├── rein_image_button.py
    │   │   └── ImageButton
    │   ├── rein_image_layer_canvas.py
    │   │   ├── LayerId
    │   │   └── ImageLayerCanvas
    │   └── rein_scrollable_canvas.py
    │       └── ScrollableCanvas
    ├── types
    │   ├── rein_alpha_blend_mode.py
    │   │   └── AlphaBlendMode
    │   ├── rein_blend_mode.py
    │   │   └── BlendMode
    │   ├── rein_bounding_box.py
    │   │   └── BoundingBox
    │   ├── rein_float_bounding_box.py
    │   │   └── FloatBoundingBox
    │   ├── rein_float_minmax.py
    │   │   └── FloatMinMax
    │   ├── rein_float2_abc.py
    │   │   └── Float2Abstract
    │   ├── rein_float2.py
    │   │   └── Float2
    │   ├── rein_float4_abc.py
    │   │   └── Float4Abstract
    │   ├── rein_int2_abc.py
    │   │   └── Int2Abstract
    │   ├── rein_int2.py
    │   │   └── Int2
    │   ├── rein_int4_abc.py
    │   │   └── Int4Abstract
    │   └── rein_size2d.py
    │       └── Size2D
    └── utility
        ├── rein_image.py
        │   ├── random_pil_crop
        │   ├── alpha_composite
        │   └── create_gradient_alpha
        └── rein_math.py
            ├── clamp
            ├── saturate
            └── lerp
```
