import requests


def fieldTransfer(fieldValue, doc):
    province_code_desc_map = {
        11: "北京市",
        12: "天津市",
        13: "河北省",
        14: "山西省",
        15: "内蒙古自治区",
        21: "辽宁省",
        22: "吉林省",
        23: "黑龙江省",
        31: "上海市",
        32: "江苏省",
        33: "浙江省",
        34: "安徽省",
        35: "福建省",
        36: "江西省",
        37: "山东省",
        41: "河南省",
        42: "湖北省",
        43: "湖南省",
        44: "广东省",
        45: "广西壮族自治区",
        46: "海南省",
        50: "重庆市",
        51: "四川省",
        52: "贵州省",
        53: "云南省",
        54: "西藏自治区",
        61: "陕西省",
        62: "甘肃省",
        63: "青海省",
        64: "宁夏回族自治区",
        65: "新疆维吾尔自治区"
    }

    province_code_desc_pre_map = {
        11: "北京",
        12: "天津",
        13: "河北",
        14: "山西",
        15: "内蒙古",
        21: "辽宁",
        22: "吉林",
        23: "黑龙江",
        31: "上海",
        32: "江苏",
        33: "浙江",
        34: "安徽",
        35: "福建",
        36: "江西",
        37: "山东",
        41: "河南",
        42: "湖北",
        43: "湖南",
        44: "广东",
        45: "广西",
        46: "海南",
        50: "重庆",
        51: "四川",
        52: "贵州",
        53: "云南",
        54: "西藏",
        61: "陕西",
        62: "甘肃",
        63: "青海",
        64: "宁夏",
        65: "新疆"
    }
    try:
        dom = doc.get('DOM', None)
        province = doc.get('PROVINCE', None)
        if (any([dom is None, province is None])):
            return None
        province_code = int(province)
        province_desc_pre = province_code_desc_pre_map.get(province_code, None)
        province_desc = province_code_desc_map.get(province_code, None)
        if any([province_desc_pre is None, province_desc is None]):
            return None
        dom = str(dom).replace('#', '号')
        if (not dom.startswith(province_desc_pre)):
            city_index = dom.find('市')
            if city_index == -1 or city_index >= len(dom) / 2:
                dom = province_desc + dom
        params = {'address': dom, 'output': 'json', 'key': 'b25c4aa693f08a670b149a4b58bac1d0'}
        response = requests.get('https://restapi.amap.com/v3/geocode/geo', params=params)
        if (response.status_code != 200):
            return None
        result = response.json()
        geo_doc = {'PID': fieldValue, 'UPDATEDDATE': ""}
        geo_location = result.get('geocodes')
        if geo_location is None:
            return None
        if len(geo_location) == 0:
            return None

        geo_location = geo_location[0]
        try:
            location = geo_location.get('location')
            geo_doc['LON'] = float(location.split(',')[0])
            geo_doc['LAT'] = float(location.split(',')[1])
        except:
            pass
        province_gaode = ''.join(geo_location.get('province')) if isinstance(geo_location.get('province'),
                                                                             list) else str(
            geo_location.get('province'))
        geo_doc['province'] = province_gaode
        geo_doc['country'] = ''.join(geo_location.get('country')) if isinstance(geo_location.get('country'),
                                                                                list) else str(
            geo_location.get('country'))
        geo_doc['town'] = ''.join(geo_location.get('township')) if isinstance(geo_location.get('township'),
                                                                              list) else str(
            geo_location.get('township'))
        geo_doc['city'] = ''.join(geo_location.get('city')) if isinstance(geo_location.get('city'), list) else str(
            geo_location.get('city'))
        geo_doc['street'] = ''.join(geo_location.get('street')) if isinstance(geo_location.get('street'),
                                                                              list) else str(
            geo_location.get('street'))
        geo_doc['district'] = ''.join(geo_location.get('district')) if isinstance(geo_location.get('district'),
                                                                                  list) else str(
            geo_location.get('district'))
        geo_doc['address'] = dom
        geo_doc["invalidAddr"] = False
        if province_desc != province_gaode:
            return None
        # 此处可以编写处理逻辑
        return geo_doc
    except Exception:
        pass
    return None
