from PIL import Image
import pytesseract
import requests

def verifyImg():
    # verify = "http://hd.chinatax.gov.cn/fagui/kaptcha.jpg"
    verify = "https://www.baidu.com/img/bd_logo1.png?qua=high"
    res = requests.get(verify)
    res = res.content
    with open("a.png", "wb") as f:
        f.write(res)
    img = Image.open("C:\\Users\\jimi\\Desktop\\homework\\pythonWork\\spider\\test\\a.png")
    print(pytesseract.image_to_string(img))


if __name__ == '__main__':
    verifyImg()
