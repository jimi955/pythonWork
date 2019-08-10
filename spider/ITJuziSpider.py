import requests
from pprint import pprint
import json


class ITJuziSpider:
    def __init__(self):
        self.url = "https://www.itjuzi.com/api/authorizations"
        self.authorization = ""
        self.cookie = ""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.form = {
            'account': '17355891658',
            'password': 'lbxxzgx66'
        }
        self.page = 1
        self.data = {'city': [],
                     'currency': [],
                     'equity_ratio': '',
                     'ipo_platform': '',
                     'keyword': '',
                     'location': '',
                     'page': 1,
                     'pagetotal': '60006',
                     'per_page': '20',
                     'prov': '',
                     'round': [],
                     'scope': '',
                     'selected': '',
                     'status': '',
                     'sub_scope': '',
                     'time': [],
                     'total': '0',
                     'type': '1',
                     'valuation': [],
                     'valuations': ''
                     }

    def getCookie(self, url, headers, form):
        res = requests.post(url, headers=headers, data=form)
        self.headers['Authorization'] = json.loads(res.content.decode())['data']['token']
        self.headers['Cookie'] = res.headers['Set-Cookie']
        self.headers['Content-Length'] = '262'
        del self.headers['User-Agent']

    def run(self, url, page):

        self.getCookie(self.url, self.headers, self.form)
        # pprint(self.headers)
        self.data['page'] = page
        res1 = requests.post(url, headers=self.headers, data=self.data)
        print(res1.content.decode())


if __name__ == '__main__':
    itjuzi = ITJuziSpider()
    itjuzi.run("https://www.itjuzi.com/api/investevents", 123)

