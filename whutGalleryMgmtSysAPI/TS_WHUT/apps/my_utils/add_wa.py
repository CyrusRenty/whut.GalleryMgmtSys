"""
给图片增加水印
"""
from PIL import Image

wa_path = '/home/aiyane/project/TS_WHUT/media/images/wa/wa.png'
root_path = '/home/aiyane/project/TS_WHUT/media/images/main/'


def add_wa(path, target_path):
    """
    path: 图片路径
    target_path: 目标路径
    """
    # target_path = target_path.rsplit('.', 1)[0]
    im = Image.open(path)
    # im.convert("JPEG")
    wa = Image.open(wa_path)
    # wa = wa.resize(im.size)
    w1, h1 = im.size
    w2, h2 = wa.size

    # if w1 > h1:
    h3 = (h1 // 10)
    w3 = int(h3/h2*w2)
    # else:
    #     w3 = (w1 // 10)
    #     h3 = int(w3/w2*h2)

    wa = wa.resize((w3, h3))

    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))

    # 两张水印
    # layer.paste(wa, (w3//2, 0))
    # layer.paste(wa, (w1//2, 0))
    layer.paste(wa, (w3//2, h1//3+h3))
    layer.paste(wa, (w1//2, h1//3+h3))
    # layer.paste(wa, (w3//2, h1-h3))
    # layer.paste(wa, (w1//2, h1-h3))
    layer = layer.rotate(45)

    out = Image.composite(layer, im, layer)
    out.save(root_path+target_path)
