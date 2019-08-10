import requests
from lxml import etree
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh,zh-CN;q=0.9",
    "Host": "www.jxacc.net",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.jxacc.net/m/view.php?aid=859",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
}
file = open("jiangxi.csv", "w")
failedfile = open("failedPage.txt", "w")
successfile = open("successPage.txt", "w")
file.write("纳税人识别号,纳税人名称,评价年度,税务机关\n")

# for page in range(1, 5):
for page in range(1, 38):
    time.sleep(2)
    url = "http://www.jxacc.net/m/view.php?aid=859&pageno=" + str(page)
    try:
        # body = {
        #     "currpage": str(page)
        # }
        res = requests.get(url, headers=headers)
        res = res.content.decode("GBK")
        # print(res)
        html = etree.HTML(res)
        trs = html.xpath("//table//tr/td/p[2]/text()")
        trs = trs[1:]
        if len(trs) == 0:
            trs = html.xpath("//table//tr/td/text()")
            print("数量：" + str(len(trs)))
        else:
            print("数量：" + str(len(trs)))

        for tr in trs:
            try:
                line = str(tr)
                line = line.replace(" ", ",").replace("\r\n", "")
                file.write(line + "\n")
            except Exception as e:
                print(111, e)
        print(str(page) + "成功")
        successfile.write(str(page) + "\n")

    except Exception as e:
        print(str(page) + "失败")
        failedfile.write(str(page) + "\n")
file.close()
failedfile.close()
successfile.close()
