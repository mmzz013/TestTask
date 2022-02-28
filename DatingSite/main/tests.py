from django.test import TestCase
import requests
from PIL import Image, ImageEnhance


#
# api_token = 'F9XjtPU7chctOMlnXk46vtr3Owq5V0wMqrYE9eNggacbF9KJrEvT95MUKCyWqsgOL7KqvWn8qSY78MaNabbP0VB6b4'
# watermark = '/static/main/img/water.png'
# photos = '/static/main/img/ns.jpeg'
# position = 'bottom-right'
# url = 'https://watermark.smm.media/api/watermark/create'
#
# params = {
#     'api_token': 'F9XjtPU7chctOMlnXk46vtr3Owq5V0wMqrYE9eNggacbF9KJrEvT95MUKCyWqsgOL7KqvWn8qSY78MaNabbP0VB6b4',
#     'watermark': 'https://free-png.ru/wp-content/uploads/2021/01/telegram_PNG10-e9a6ae3e-450x450.png',
#     'photos': 'https://svirtus.cdnvideo.ru/fJuUhjmvRX_aviPp8-ZrrABhwX0=/5x86:1200x723/1200x1200/filters:quality(100)'
#               '/https://hb.bizmrg.com/cybersportru-media/8d/8de1de204b76ff3bfaad8a6e28e0f0ce.jpg'
#               '?m=18c62aa10078c6cda2e46dc468ac8ae3',
#     'position': 'bottom-right',
# }
#
# response = requests.post(url, json=params)

def add_watermark(image, watermark, opacity=1):
    assert 0 <= opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    layer.paste(watermark, (1, 1))
    return Image.composite(layer, image, layer)


img = Image.open('main/static/main/img/ns.jpeg')
water = Image.open('main/static/main/img/water.png')
result = add_watermark(img, water)
result.save('main/static/main/img/result.png')
