# -*- coding: utf-8 -*-
import time
def area_convert(value):
    if value == None or value == "":
        return ""
    for area in ("华南", "华北", "东北", "华东", "华中", "西北", "西南"):
        if value.__contains__(area):
            return area
    return value

def date_time_convert(value):
    value = value[:value.index("日")]
    value = value.replace("月", "-")
    date = time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.strptime("2018-" + value, '%Y-%m-%d')))))
    return date.replace("2018-", "")

def market_date_time_convert(value):
    value = value[:value.index("日")]
    datas = value.split("】")
    if(len(datas) > 0):
        return datas[1].replace("月", "-")
    return ""

def market_updown_convert(value):
    return "0" if value == None or value == '' else value;



