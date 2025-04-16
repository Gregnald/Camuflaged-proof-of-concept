from pyzbar.pyzbar import decode
from PIL import Image

def scan_it(qr):
    img = Image.open(qr)
    result = decode(img)
    return result[0][0].decode('utf-8')