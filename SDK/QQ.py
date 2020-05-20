import requests
from lxml import etree
import json
import re


class QQMusic(object):

    def __init__(self):
        self.apis = {
            "search_url": "http://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp",
            "palysong_url": "https://i.y.qq.com/v8/playsong.html",
            "get_profile_url": "https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg",
            "get_profile_order_url": "https://c.y.qq.com/fav/fcgi-bin/fcg_get_profile_order_asset.fcg",
            "get_diss_songs_url": "https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg",
        }
        self.agents = {
            "ios": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46",
            "pc": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/81.0.4044.129 Safari/537.36 "
        }
        self.headers = {
            "referer": "http://m.y.qq.com",
            "User-Agent": self.agents['ios'],
            # cookie需要修改成自己的
            "cookie": ""
        }

    # 搜索音乐
    def search(self, keyword, n=10):
        parmas = {"w": keyword, "format": "json", "p": 1, "n": n}
        res = requests.get(self.apis['search_url'], params=parmas, headers=self.headers).json()
        songs = res['data']['song']['list']
        return [song['songmid'] for song in songs]

    # 获取音乐链接
    def getSongUrl(self, mid):
        params = {
            "songmid": mid,
            "ADTAG": "myqq",
            "from": "myqq",
            "channel": "10007100"
        }
        text = requests.get(self.apis['palysong_url'], params=params, headers=self.headers).text
        html = etree.HTML(text)
        try:
            return html.xpath('/html/body/audio[1]/@src')[0]
        except IndexError:
            pass

    # 获取歌单列表
    def getDissLists(self):
        dissList = []
        params = {
            "g_tk_new_20200303": 925150183,
            "g_tk": 908742994,
            "loginUin": 123456789,
            "hostUin": 0,
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "yqq.json",
            "needNewCode": 0,
            "cid": 205360838,
            "ct": 20,
            "userid": 0,
            "reqfrom": 1,
            "reqtype": 0
        }
        headers = {
            "cookie": self.headers['cookie'],
            "referer": "https://y.qq.com/portal/profile.html",
            "user-agent": self.agents['pc']
        }
        res = requests.get(self.apis['get_profile_url'], params=params, headers=headers).json()
        userid = res['data']['creator']['uin']
        myLove = res['data']['mymusic'][0]
        dissList.append({
            "name": "我喜欢",
            "dissid": myLove["id"],
            "num": myLove['num0']
        })
        dissList += [
            {
                "name": diss['title'],
                "dissid": diss['dissid'],
                "num": int(diss['subtitle'].split('首')[0])
            } for diss in res['data']['mydiss']['list']
        ]
        params['cid'] = '205360956'
        params['reqtype'] = 3
        params['sin'] = 0
        params['ein'] = 10
        params['userid'] = userid
        res = requests.get(self.apis['get_profile_order_url'], params=params, headers=headers).json()
        dissList += [
            {
                "name": diss['dissname'],
                "dissid": diss['dissid'],
                "num": diss['songnum']
            } for diss in res['data']['cdlist']
        ]
        return dissList

    # 获取榜单歌曲
    # id 62 飙升榜
    # id 26 热歌榜
    # id 27 新歌榜
    # id 4 流行指数榜
    # id 60 抖音排行榜
    def getTopList(self, id):
        url = f"https://i.y.qq.com/n2/m/share/details/toplist.html?ADTAG=myqq&from=myqq&channel=10007100&id={id}"
        res = requests.get(url, headers=self.headers).text
        results = re.findall('<script>var firstPageData = (.*?)</script>', res, re.S)
        results = json.loads(results[0])
        songs = [
            {
                "name": song['name'],
                "singer": ' '.join([sing['name'] for sing in song['singer']]),
                "mid": song['mid']
            } for song in results['songInfoList']
        ]
        return songs

    # 获取歌单音乐
    def getDissSongs(self, dissid, page=1, num=10):
        headers = {
            "cookie": self.headers['cookie'],
            "referer": "https://y.qq.com/portal/profile.html",
            "user-agent": self.agents['pc']
        }
        params = {
            "type": 1,
            "json": 1,
            "utf8": 1,
            "onlysong": 1,
            "nosign": 1,
            "new_format": 1,
            "song_begin": (page - 1) * num,
            "song_num": num,
            "ctx": 1,
            "disstid": dissid,
            "_": 1588724818395,
            "g_tk_new_20200303": 925150183,
            "g_tk": 908742994,
            "loginUin": 123456789,
            "hostUin": 0,
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "yqq.json",
            "needNewCode": 0
        }
        res = requests.get(self.apis['get_diss_songs_url'], params=params, headers=headers).json()
        songs = res['songlist']
        return ([
            {
                "name": song['name'],
                "mid": song['mid']
            } for song in songs
        ])
