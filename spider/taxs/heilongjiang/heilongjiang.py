import requests
from lxml import etree
import time

url = "http://heilongjiang.chinatax.gov.cn/module/search/index.jsp?field=field_2292:1,field_2293:1&i_columnid=3587"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh,zh-CN;q=0.9",
    "Cache-Control": "max-age=0",
    "Host": "heilongjiang.chinatax.gov.cn",
    "Origin": "http://heilongjiang.chinatax.gov.cn",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://heilongjiang.chinatax.gov.cn/module/search/index.jsp?field=field_2292:1,field_2293:1&i_columnid=3587&currpage=11",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
}
file = open("heilongjiang.csv", "w")
failedfile = open("failedPage.txt", "w")
successfile = open("successPage.txt", "w")
file.write("编号	纳税人识别号,纳税人名称,信用级别,评价年度,税务机关\n")

# for page in range(1, 5):
for page in range(1, 525):
    time.sleep(2)
    try:
        body = {
            "currpage": str(page)
        }
        res = requests.post(url, headers=headers, data=body)
        res = res.content.decode("utf-8")
        # print(res)
        html = etree.HTML(res)
        trs = html.xpath("//table[@class='dzchaxun']//tr")
        print("数量：" + str(len(trs)))
        for tr in trs:
            try:
                line = []
                line.append(tr.xpath("td[1]/text()")[0])
                line.append(tr.xpath("td[2]/text()")[0])
                line.append(str(tr.xpath("td[3]/text()")[0]))
                line.append(tr.xpath("td[4]/text()")[0])
                line.append(tr.xpath("td[5]/text()")[0])
                file.write(",".join(line) + "\n")
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
