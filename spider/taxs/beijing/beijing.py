import requests
from lxml import etree
import time

file = open("beijing.csv", "w", encoding='utf-8')
failedfile = open("failedPage.txt", "w")
successfile = open("successPage.txt", "w")
file.write("序号,单位名称,纳税人识别号,主管税务机关,评价结果,评价年度\n")

# for page in range(1, 3):
for page in range(1, 5615):
    time.sleep(1)
    try:
        res = requests.get(
            "http://beijing.chinatax.gov.cn/bjsat/office/jsp/ajqy/query.jsp?page_num=" + str(
                page) + "&dwmc=&BeginTime=&EndTime=&nsrsbh=&ssny=2018")

        html = res.content.decode("GBK")

        # print(html)

        html = etree.HTML(html)

        trs = html.xpath("//table[@class='table_input']//tr")
        if trs != None and len(trs) > 0:
            trs = trs[2:-1]
            print("第" + str(page) + "页数据条数：" + str(len(trs)))
            for tr in trs:
                try:
                    num = tr.xpath("td[1]/text()")[0].replace("\r\n", "").strip()
                    comname = tr.xpath("td[2]/a/text()")[0].replace("\r\n", "").strip()
                    pid = tr.xpath("td[3]/text()")[0].replace("\r\n", "").strip()
                    partment = tr.xpath("td[4]/text()")[0].replace("\r\n", "").strip()
                    result = tr.xpath("td[5]/text()")[0].replace("\r\n", "").strip()
                    year = tr.xpath("td[6]/text()")[0].replace("\r\n", "").strip()
                    line = num + "," + comname + "," + pid + "," + partment + "," + result + "," + year + "\n"
                    file.write(line)
                except Exception as e:
                    print(e)
        print("第" + str(page) + "页成功")
        successfile.write(str(page) + "\n")
    except Exception as e:
        print("第" + str(page) + "页出了错")
        failedfile.write(str(page) + "\n")

file.close()
failedfile.close()
successfile.close()
