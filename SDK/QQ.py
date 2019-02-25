import requests
import json
import time
import random
from urllib import parse


def search(name):
    try:
        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remotep" \
              "lace=txt.yqq.center&searchid=50495243386587389&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&" \
              "p=1&n=20&w=%s&g_tk=421181271&loginUin=779956774&hostUin=0&format=json&inCharset=utf8&" \
              "outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0" % name
        res = requests.get(url).json()
        if res['code'] != 0:
            return print("暂未找到歌曲，请稍后试试吧")
        else:
            return res['data']
    except Exception as e:
        print(e)


def getMusicByMid(mid):
    guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
    data = {
        "req": {
            "module": "CDN.SrfCdnDispatchServer",
            "method": "GetCdnDispatch",
            "param": {
                "guid": str(guid),
                "calltype": 0,
                "userip": ""
            }
        },
        "req_0": {
            "module": "vkey.GetVkeyServer",
            "method": "CgiGetVkey",
            "param": {
                "guid": str(guid),
                "songmid": [mid],
                "songtype": [0],
                "uin": "779956774",
                "loginflag": 1,
                "platform": "20"
            }
        },
        "comm": {
            "uin": 779956774,
            "format": "json",
            "ct": 24,
            "cv": 0
        }
    }
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey7158580598206303&g_tk=421181271&loginUin=779956774&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%s' % parse.quote(json.dumps(data))
    res = requests.get(url).json()
    return res['req']['data']['sip'][0] + res['req_0']['data']['midurlinfo'][0]['purl']


getMusicByMid('001OyHbk2MSIi4')
