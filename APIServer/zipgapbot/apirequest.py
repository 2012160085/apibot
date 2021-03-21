import json
import xmltodict
import requests
import time
from . import logger
@logger.log_with_trycatch
def getContent(datadict):
    resultCode = datadict['response']['header']['resultCode']
    itemlist = datadict['response']['body']['items']
    if itemlist is None:
        itemlist = []
    else:
        itemlist = itemlist['item']
        if isinstance(itemlist,dict):
            itemlist = [itemlist]
    totalCount = datadict['response']['body']['totalCount']
    return resultCode, totalCount, itemlist
@logger.log_with_trycatch
def dictfromxml(xmlStr):
    dict_type = xmltodict.parse(xmlStr)
    json_type = json.dumps(dict_type)
    dict2_type = json.loads(json_type)
    return getContent(dict2_type)

@logger.log_with_trycatch
def get_response(url,params):
    res = requests.get(url,params=params)
    time.sleep(0.1)
    return dictfromxml(res.text)
