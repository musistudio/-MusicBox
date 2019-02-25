## 基于Python3的简单音乐爬取

#### 使用方法

1. 引入SDK
```python3
from SDK import QQ        # 引入QQ音乐
from SDK import Netease   # 引入网易云音乐
```

2. 搜索歌曲
```python
# 使用QQ音乐搜索
QQ.search('歌曲名字')
# 使用网易云音乐搜索
Netease.search('歌曲名字')
```

3. 获取歌曲URL
```python3
# 使用QQ音乐获取
QQ.getMusicByMid(搜索歌曲得到的mid)
# 使用网易云音乐获取
Netease.getMusicById(搜索歌曲得到的id)
```