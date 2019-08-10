import requests
from pprint import pprint
import json


class ZhaoDaoSpider:
    def __init__(self):
        self.url = "https://www.zdao.com/site/search?keywords=" + "深圳平安综合金融服务有限公司"
        self.authorization = ""
        self.cookie = ""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            # 'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.form = {
            'account': '17355891658',
            'password': 'lbxxzgx66'
        }
        self.data = {}

    # def getCookie(self, url, headers, form):
    #     res = requests.post(url, headers=headers, data=form)
    #     self.headers['Authorization'] = json.loads(res.content.decode())['data']['token']
    #     self.headers['Cookie'] = res.headers['Set-Cookie']
    #     self.headers['Content-Length'] = '262'
    #     del self.headers['User-Agent']

    def run(self):
        # for i in range(2):
        res = requests.get(self.url, headers=self.headers)
        print(res.content.decode())
        print(res.status_code)


if __name__ == '__main__':
    itjuzi = ZhaoDaoSpider()
    itjuzi.run()
