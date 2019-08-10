#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import re
import time
import json
import requests
import base64
import hashlib


class ApiException(Exception):
    def __init__(self, errCode, errMsg):
        self.errCode = errCode
        self.errMsg = errMsg


class AbstractApi(object):
    def __init__(self, entCode):
        self.entCode = entCode
        return

    def getAccessToken(self):
        raise NotImplementedError

    def refreshAccessToken(self):
        raise NotImplementedError

    def httpCall(self, urlType, args=None):
        shortUrl = urlType[0]
        method = urlType[1]
        response = {}
        for retryCnt in range(0, 3):
            if 'POST' == method:
                url = self.__makeUrl(shortUrl)
                response = self.__httpPost(url, args)
            elif 'GET' == method:
                url = self.__makeUrl(shortUrl)
                url = self.__appendArgs(url, args)
                response = self.__httpGet(url)
            else:
                raise ApiException(-1, "unknown method type")

            # check if token expired
            if self.__tokenExpired(int(response.get('result'))):
                self.__refreshToken(shortUrl)
                retryCnt += 1
                continue
            else:
                break

        return self.__checkResponse(response)

    @staticmethod
    def __appendArgs(url, args):
        if args is None:
            return url

        for key, value in args.items():
            if '?' in url:
                url += ('&' + key + '=' + value)
            else:
                url += ('?' + key + '=' + value)
        return url

    @staticmethod
    def __makeUrl(shortUrl):
        base = "https://cloud.hecom.cn"
        if shortUrl[0] == '/':
            return base + shortUrl
        else:
            return base + '/' + shortUrl

    def __appendToken(self, url):
        if 'SUITE_ACCESS_TOKEN' in url:
            return url.replace('SUITE_ACCESS_TOKEN', self.getSuiteAccessToken())
        elif 'PROVIDER_ACCESS_TOKEN' in url:
            return url.replace('PROVIDER_ACCESS_TOKEN', self.getProviderAccessToken())
        elif 'ACCESS_TOKEN' in url:
            return url.replace('ACCESS_TOKEN', self.getAccessToken())
        else:
            return url

    def __httpPost(self, url, args):
        realUrl = self.__appendToken(url)
        # print(realUrl, args)
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'entCode': self.entCode
        }
        if 'token' not in realUrl:
            headers['accessToken'] = self.getAccessToken()
        return requests.post(realUrl, headers=headers, data=json.dumps(args, ensure_ascii=False).encode('utf-8')).json()

    def __httpGet(self, url):
        realUrl = self.__appendToken(url)
        # print(realUrl)
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'entCode': self.entCode
        }
        if 'token' not in realUrl:
            headers['accessToken'] = self.getAccessToken()
        return requests.get(realUrl, headers=headers).json()

    def __post_file(self, url, media_file):
        return requests.post(url, file=media_file).json()

    @staticmethod
    def __checkResponse(response):
        errCode = int(response.get('result'))
        errMsg = response.get('desc')

        if errCode is 0:
            return response
        else:
            raise ApiException(errCode, errMsg)

    @staticmethod
    def __tokenExpired(errCode):
        if errCode == 204 or errCode == 42001 or errCode == 42007 or errCode == 42009:
            return True
        else:
            return False

    def __refreshToken(self, url):
        self.refreshAccessToken()


CORP_API_TYPE = {
    'GET_ACCESS_TOKEN': ['/customize/open/api/common/token', 'POST'],
    'GET_BIZ_DATALIST': ['/customize/api/data/v1/bizData/getBizDataListWithoutPermission', 'POST'],
}


class CorpApi(AbstractApi):
    def __init__(self, entCode, key, secret):
        super(CorpApi, self).__init__(entCode)
        self.key = key
        self.secret = secret
        if os.path.exists('./access.token'):
            with open('./access.token', 'rb') as ifp:
                self.access_token = ifp.readline().decode('utf-8').strip('\r\n ')
            if len(self.access_token) == 0:
                self.access_token = None
        else:
            self.access_token = None

    def getAccessToken(self):
        if self.access_token is None:
            self.refreshAccessToken()
        return self.access_token

    def refreshAccessToken(self):
        timestamp = str(int(round(time.time() * 1000)))
        signature = base64.b64encode(
            hashlib.sha256(("%s-%s-%s" % (self.key, self.secret, timestamp)).encode('utf-8')).digest()).decode('utf-8')

        response = self.httpCall(
            CORP_API_TYPE['GET_ACCESS_TOKEN'],
            {
                'entCode': self.entCode,
                'appKey': self.key,
                'timestamp': timestamp,
                'signature': signature
            })
        self.access_token = response.get('data').get('accessToken')
        with open('./access.token', 'wb') as ofp:
            ofp.write(self.access_token.encode('utf-8'))

    def getBizDataListWithoutPermission(self, body):
        results = []
        pageNo = 1
        pageSize = 20
        totalCount = None
        while True:
            body['page'] = {
                "pageNo": pageNo,
                "pageSize": pageSize
            }
            response = self.httpCall(
                CORP_API_TYPE['GET_BIZ_DATALIST'],
                body
            )
            if not totalCount:
                totalCount = response.get('data').get('totalCount')
                results = response.get('data')
            else:
                results['records'].extend(response.get('data').get('records'))
                if len(results['records']) == totalCount:
                    break

            pageNo = pageNo + 1
        return results


import argparse
from jsonschema import validate

META_SCHEMA = {
    "type": "object",
    "meta": {
        "metaName": {"type": "string"},
        "fields": {"type": "array"}
    },
    "filter": {
        "type": "object",
        "conj": {"type": "string"},
        "expr": {"type": "string"}
    },
    "scope": {"type": "number"},
    "sorts": {"type": "array"}
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--meta', help='Meta json file path.')
    parser.add_argument('-o', '--output', help="Output csv file path.")
    args = parser.parse_args()
    # meta = args.meta
    meta = "meta_customers.json"
    # output = args.output
    output = "meta_customers.csv"
    print("22222222222222222222")
    if not meta or not output:
        parser.print_help()
        sys.exit(0)

    with open(meta, 'rb') as ifp:
        meta = json.load(ifp)
        validate(instance=meta, schema=META_SCHEMA)

    api = CorpApi('koios', 'WGz9ANC7lw9BmvJl',
                  'JaTIAKcpevJ4nZ1xk2BPaemVSCAoOHgo')

    result = api.getBizDataListWithoutPermission(meta)
    print(result)

    fields = ['code', 'metaName']
    fields.extend(meta['meta']['fields'])
    with open(output, 'wb') as ofp:
        # write csv headers
        header = ','.join(fields) + '\n'
        ofp.write(header.encode('utf-8'))

        for record in result['records']:
            line = []
            for f in fields:
                try:
                    if type(record[f]) == int:
                        line.append(str(record[f]))
                    elif type(record[f]) == dict:
                        line.append('"%s"'% record[f])
                    else:
                        line.append(record[f])
                except Exception as e:
                    line.append("null")
            ofp.write((",".join(line) + "\n").encode('utf-8'))
