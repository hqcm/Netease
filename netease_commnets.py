from Netease_crack import Crack
from Netease_downlodmusic import Neteasedownlodmusic


class Neteasehotcomments(object):
    "获取网易歌曲首页的热门评论"

    def __init__(self, music_name):
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'referer':
            'http://music.163.com/',
        }
        self.crack = Crack()
        self.dlm = Neteasedownlodmusic(music_name)

    def getHotcomments(self):
        "获得热门评论"
        music_id = self.dlm.getMusicinfo()
        rid = "R_SO_4_" + str(music_id[0])
        url = url = "https://music.163.com/weapi/v1/resource/comments/%s?csrf_token=" % rid
        text = {
            "rid": rid,
            "offset": "0",  #（评论页数-1）×20
            "total": "true",  #在第一页为true，其余为false
            "limit": "20",
            "csrf_token": ""
        }
        html = self.dlm.getHtml(text, url)
        html = html["hotComments"]
        for i in html:
            print(i["user"]["nickname"] + ": " + i["content"] +
                  "#######点赞数: " + str(i["likedCount"]))


if __name__ == '__main__':
    music_name = input("请输入要获得热门评论的歌曲的名字：")
    nhc = Neteasehotcomments(music_name)
    nhc.getHotcomments()