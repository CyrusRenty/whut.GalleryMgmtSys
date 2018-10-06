"""
给图片增加水印
"""
from PIL import Image
from TS_WHUT.settings import MEDIA_ROOT

wa_path = MEDIA_ROOT + '/wa/wa.png'
root_path = MEDIA_ROOT + '/main/'


def add_wa(path, target_path):
    """
    path: 图片路径
    target_path: 目标路径
    """
    im = Image.open(path)
    wa = Image.open(wa_path)
    w1, h1 = im.size
    w2, h2 = wa.size

    h3 = (h1 // 10)
    w3 = int(h3/h2*w2)

    wa = wa.resize((w3, h3))

    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))

    # 两张水印
    layer.paste(wa, (w3//2, h1//3+h3))
    layer.paste(wa, (w1//2, h1//3+h3))
    layer = layer.rotate(45)

    out = Image.composite(layer, im, layer)
    # 压缩
    try:
        out.resize(out.size, Image.ANTIALIAS).save(root_path + target_path, quality=75)
    except OSError:
        pass
