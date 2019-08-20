import requests
from lxml import etree
import time
from PIL import Image
import pytesseract

def verifyImg():
    verify = "http://hd.chinatax.gov.cn/fagui/kaptcha.jpg"
    res = requests.get(verify)
    res = res.content
    with open("a.png", "wb") as f:
        f.write(res)
    img = Image.open("a.png")
    print(pytesseract.image_to_string(img))

def run():
    # body = {"articleField01": "",
    #         "articleField02": "",
    #         "articleField03": "2018",
    #         "articleField06": "",
    #         "taxCode": 320000,
    #         "cPage": 9998,
    #         "randCode": "56t6u8fn",
    #         "flag": 1,
    #         "scount": 4}
    with open("res.csv", "w") as file:
        for i in range(9999):
            time.sleep(1)
            try:
                url = "http://hd.chinatax.gov.cn/fagui/action/InitCredit.do?articleField03=2018&taxCode=320000&flag=1&cPage=" + str(
                    i)
                res = requests.get(url)
                res = res.content.decode()
                if res.find("您当前的访问行为存在异常") > -1:
                    print("您当前的访问行为存在异常")
                    verifyImg()

                    return
                html = etree.HTML(res)
                trs = html.xpath("//td[@class='sv_hei']//tr")
                trs = trs[1:]
                for tr in trs:
                    line = []
                    compnyId = tr.xpath("td[1]/text()")[0]
                    compnyName = tr.xpath("td[2]/text()")[0]
                    print(compnyName)
                    line.append(compnyId)
                    line.append(compnyName)
                    line.append("2018")
                    file.write(",".join(line) + "\n")
                print("success", i)

            except:
                print("fail", i)


if __name__ == '__main__':
    run()
