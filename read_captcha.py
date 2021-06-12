import easyocr
import matplotlib.pyplot

def decode_captcha():
    reader = easyocr.Reader(['en'], gpu=False)
    image = matplotlib.pyplot.imread('captcha.png', 0)
    result = reader.readtext(image)
    if len(result) == 0:
        return "", -1
    return result[0][1], result[0][2]