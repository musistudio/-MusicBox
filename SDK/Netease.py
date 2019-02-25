import requests


def search(name):
    try:
        url = 'http://music.163.com/api/cloudsearch/pc'
        data = {
            's': name,
            'type': '1',
            'limit': '30',
            'total': 'true',
            'offset': '0'
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        }
        res = requests.post(url, data=data, headers=headers).json()
        if res["code"] == 200:
            return res["result"]["songs"]
        else:
            return print("暂未获取到该歌曲")
    except Exception as e:
        print(e)


def getMusicById(id):
    url = 'http://music.163.com/api/song/enhance/player/url'
    data = {
        "ids": '["{}"]'.format(id),
        "br": "320000"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    res = requests.post(url, data=data, headers=headers)
    print(res.text)

# search('十一年')
# getMusicById("143403")