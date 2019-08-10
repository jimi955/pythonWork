import requests
import json
import time


class Spider:
    def __init__(self):
        self.accessToken = ""
        self.uid = "c574581071287431168"
        self.empCode = "10078203682"
        self.entCode = 'koios'
        self.clientTag = 'web'
        self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"

        self.headers = {
            "accesstoken": "",
            "clienttag": self.clientTag,
            "empcode": self.empCode,
            "entcode": self.entCode,
            "uid": self.uid,
            "obj": "",
            "user-agent": self.UA,
            "content-type": "application/json",
            "origin": "https://cloud.hecom.cn",
            "referer": "",
            "act": "list",
            "app": "std"
        }

    def login(self):
        # 登陆获取 accessToken
        data = {
            "account": "15902117110",
            "password": "6jOXJwKQdKIUcvkwB2AkS0itf2n8prfr",
            "clientTag": "web"
        }
        headers = {
            "User-Agent": self.UA,
            "Referer": "https://cloud.hecom.cn/login",
            "Content-Type": "application/json",
            "Origin": "https://cloud.hecom.cn"
        }
        logindo_url = "https://tc.cloud.hecom.cn/hecom-tenancy/cloud/user/login.do"
        logindores = requests.post(logindo_url, data=json.dumps(data), headers=headers)
        if logindores.status_code == 200:
            loginres = json.loads(logindores.content.decode())
            token = loginres['data']['accessToken']
            with open("asscestoken.txt", "w+") as f:
                f.write(token)

            # 登陆验证
            timed = str(round(time.time() * 1000))
            login_url = "https://cloud.hecom.cn/universe/user/login"
            body = {"accessToken": token, "clientTag": self.clientTag, "empCode": self.empCode,
                    "entCode": self.entCode,
                    "time": timed, "uid": self.uid}
            headers = {
                "user-agent": self.UA,
                "content-type": "application/json"
            }
            login_res = requests.post(login_url, data=json.dumps(body), headers=headers)
            print(login_res.content.decode())
        else:
            print("登陆失败>>" + logindores.status_code)

    def getContents(self, page_num, element, content_url, referer):
        body = {'filter': {'conj': 'advance', 'expr': ''},
                'meta': {'metaName': element},
                'page': {'pageNo': page_num, 'pageSize': 20},
                'scope': 1,
                'sorts': [{'field': 'updatedOn', 'orderType': 0}]
                }
        self.headers['accesstoken'] = self.accessToken
        self.headers['obj'] = element
        self.headers['referer'] = referer
        res = requests.post(content_url, data=json.dumps(body),
                            headers=self.headers)
        res = json.loads(res.content.decode())
        companys = res['data']['records']
        print("<<<<第%d页请求成功>>>>" % page_num)
        return companys

    def getDetail(self, id, element, detail_url, referer):

        data = {
            "code": id,
            "dynamicType": 0,
            "metaName": element,
            "pageNo": 1,
            "pageSize": 10
        }
        self.headers['accesstoken'] = self.accessToken
        self.headers['obj'] = element
        self.headers['referer'] = referer
        res = requests.post(detail_url, data=json.dumps(data),
                            headers=self.headers)

        res = json.loads(res.content.decode())
        res = res['data']['records']
        # print(res)
        infos = []
        for r in res:
            info = {}
            # print(r)
            if "flowUpContent" in r.keys():
                if "name" in r['flowUpContent'].keys():
                    info['name'] = r['flowUpContent']['name']
                else:
                    info['name'] = 'None'
                if "content" in r['flowUpContent'].keys():
                    info['content'] = r['flowUpContent']['content']
                else:
                    info['content'] = 'None'
            else:
                info['name'] = 'None'
                info['content'] = 'None'

            if 'createdBy' in r.keys():
                if 'name' in r['createdBy']:
                    info['createdBy'] = r['createdBy']['name']
                else:
                    info['createdBy'] = 'None'
            else:
                info['createdBy'] = 'None'
            if 'createdOn' in r.keys():
                info['createdOn'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(round(int(r['createdOn']) / 1000)))
            else:
                info['createdOn'] = 'None'
            infos.append(info)
        return infos

    def download_process_clue(self, pagesize, element, filename, content_url, detail_url, referer):
        with open(filename, "wb+") as file:
            tableheader = ['companyName', 'mobilephone', 'createdOn', 'name', 'content', 'createdBy',
                           'createdOn']
            file.write((",".join(tableheader) + "\n").encode('utf-8'))
            for page_num in range(1, pagesize):
                companys = self.getContents(page_num, element, content_url, referer)
                for company in companys:
                    oneCompany = []
                    activeInfo = self.getDetail(company['id'], element, detail_url, referer)
                    if "companyName" in company.keys():
                        oneCompany.append(company['companyName'])
                    else:
                        oneCompany.append("None")
                    if "mobilephone" in company.keys():
                        oneCompany.append(company['mobilephone'])
                    else:
                        oneCompany.append("None")
                    if "createdOn" in company.keys():
                        oneCompany.append(time.strftime("%Y-%m-%d %H:%M",
                                                        time.localtime(round(company['createdOn'] / 1000))))
                    else:
                        oneCompany.append("None")
                    if len(activeInfo) > 0:
                        for info in activeInfo:
                            for value in info.values():
                                oneCompany.append("%s" % value.replace("\n", ""))
                    print(oneCompany)
                    file.write((",".join(oneCompany) + "\n").encode('utf-8'))

    def download_process_opportunity(self, pagesize, element, filename, content_url, detail_url, referer):
        with open(filename, "wb+") as file:
            tableheader = ['customer', 'createdOn', 'name', 'content', 'createdBy',
                           'createdOn']
            file.write((",".join(tableheader) + "\n").encode('utf-8'))
            for page_num in range(1, pagesize):
                companys = self.getContents(page_num, element, content_url, referer)
                for company in companys:
                    oneCompany = []
                    activeInfo = self.getDetail(company['id'], element, detail_url, referer)
                    if "customer" in company.keys():
                        if "name" in company['customer'].keys():
                            oneCompany.append(company['customer']['name'])
                    else:
                        oneCompany.append("None")
                    if "createdOn" in company.keys():
                        oneCompany.append(time.strftime("%Y-%m-%d %H:%M",
                                                        time.localtime(round(company['createdOn'] / 1000))))
                    else:
                        oneCompany.append("None")
                    if len(activeInfo) > 0:
                        for info in activeInfo:
                            for value in info.values():
                                oneCompany.append("%s" % value.replace("\n", ""))
                    print(oneCompany)
                    file.write((",".join(oneCompany) + "\n").encode('utf-8'))

    def init(self):
        with open("asscestoken.txt", "r+") as f:
            self.accessToken = f.readline()

    def sleep(self, hours):
        time.sleep(60 * 60 * hours)

    def run(self):
        while True:
            try:
                self.init()
                content_url = "https://cloud.hecom.cn/universe//paas/app/std/list"
                detail_url = "https://cloud.hecom.cn/universe//paas/app/std/dynamic/list.do"
                pageSize = 21
                referer = "https://cloud.hecom.cn/clue"
                self.download_process_clue(pageSize, 'clue', 'clue.csv', content_url, detail_url, referer)

                referer = "https://cloud.hecom.cn/opporapp"
                self.download_process_opportunity(pageSize, 'opportunity', 'opportunity.csv', content_url, detail_url,
                                                  referer)
            except Exception as e:
                print(e)
                # self.login()
            break
            self.sleep(24 * 7)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
