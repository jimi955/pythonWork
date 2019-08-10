import re
import requests

loc = "安徽省阜阳市颍泉区"
res = ""
try:
    res = re.search("(\w+省)?(\w+?)市", loc).group(2)
except Exception as e:
    res = ""

if res != "":
    params = {'address': loc, 'output': 'json', 'key': 'b25c4aa693f08a670b149a4b58bac1d0'}
    response = requests.get('https://restapi.amap.com/v3/geocode/geo', params=params)
    # if (response.status_code != 200):
    #     return None
    result = response.json()
    # geo_doc = {'PID': fieldValue, 'UPDATEDDATE': datetime.datetime.now()}
    geo_location = result.get('geocodes')
    # if geo_location is None:
    #     return None
    # if len(geo_location) == 0:
    #     return None

    geo_location = geo_location[0]
    try:
        city = geo_location.get('city')
    except:
        pass
print(res)
