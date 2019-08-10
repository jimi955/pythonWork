import requests
import json
from pprint import pprint

# addTagUrl = "http://localhost:7080/internal/v1/rest/tag"
addTagUrl = "http://slb.hz.koios.site:7080/internal/v1/rest/tag"
# addTagRulesUrl = "http://localhost:7080/internal/v1/rest/tagField"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Content-Type": "application/json"
}


# def getTagBody(tagName, category, order=1000, isDisplay=False):
#     body = {
#         "tagName": tagName,
#         "category": category,
#         "order": order,
#         "isDisplay": isDisplay
#     }
#     return body
#
#
# def getTagRulesBody(tagName, db, collection, projection, target, pidKey, opt, conditionType="All"):
#     body = {
#         "tagName": tagName,
#         "conditionType": conditionType,  # any/all
#         "enabled": True,
#         "conditions": [
#             {
#                 "target": target,
#                 "type": "mongo",
#                 "db": db,
#                 "collection": collection,
#                 "projection": projection,
#                 "pidKey": pidKey,
#                 "opt": opt
#             }
#         ]
#     }
#     return body


def main():
    tagInfo = []
    with open("tag.json", "r+", encoding="UTF-8") as f:
        tagInfo = f.read()
    tagInfos = json.loads(tagInfo)
    for tagInfo in tagInfos:
        # pprint(tagInfo)
        # body = getTagBody(tagInfo["tagName"], tagInfo["category"])
        res = requests.post(addTagUrl, data=json.dumps(tagInfo), headers=headers)
        pprint(res.status_code)
        pprint(res.content.decode())


if __name__ == '__main__':
    main()
