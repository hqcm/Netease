from Crypto.Cipher import AES
import base64
import requests
import sys
import binascii
import os
import json
from Netease_crack import Crack


class Neteasedownlodmusic(object):
    "根据歌曲名下载网易歌曲"

    def __init__(self, music_name):
        self.id_url = "http://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        self.music_url = "https://music.163.com/weapi/song/enhance/player/url?csrf_token="
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'referer':
            'http://music.163.com/',
        }
        self.music_name = music_name
        self.crack = Crack()

    def getMusicid(self, musician):
        "得到歌曲的id"
        flag = False
        text = {"s": self.music_name, "type": 1}
        html = self.getHtml(text, self.id_url)
        html = html["result"]["songs"]
        for song in html:
            if (song["ar"][0]["name"] == musician):
                flag = True
                break
        if flag:
            return song["id"]
        else:
            print("您要下载的歌曲可能由于版权问题不存在!")
            exit()

    def getMusicinfo(self):
        "得到歌曲id和歌手名字"
        text = {"s": self.music_name, "type": 1}
        html = self.getHtml(text, self.id_url)
        if html["result"]["songCount"] == 0:
            print("您要下载的歌曲不存在!")
            exit()
        else:
            html = html["result"]["songs"][0]
            music_id = html["id"]  #id方便下载歌曲
            musician = html["ar"][0]["name"]  #用作命名
            return music_id, musician

    def downloadMusic(self, *args):
        "下载歌曲"
        if args:
            musician = args[0]
            music_id = self.getMusicid(musician)
        else:
            music_id, musician = self.getMusicinfo()
        text = {
            "ids": "[" + str(music_id) + "]",
            "br": 320000,
            "csrf_token": ""
        }
        html = self.getHtml(text, self.music_url)
        music_url = html["data"][0]["url"]
        #下载到本文件夹中,以歌手名作为文件夹名
        folder = os.path.join(sys.path[0], musician)
        if not os.path.exists(folder):
            os.makedirs(folder)
        name = os.path.join(folder,
                            (self.music_name + " - " + musician + ".mp3"))
        music = requests.get(music_url)
        with open(name, "wb") as f:
            f.write(music.content)

    def getHtml(self, text, url):
        "网页请求"
        text = json.dumps(text)
        data = self.crack.getData(text)
        html = requests.post(url, headers=self.headers, data=data).json()
        return html


if __name__ == '__main__':
    music_name = input("请输入要下载的歌曲的名字：")  #将所有输入默认为字符串处理，并返回字符串类型
    dlm = Neteasedownlodmusic(music_name)
    dlm.downloadMusic()
    print("下载成功请按空格键,然后回车；输入歌手名字可重新进行精确搜索：")
    musician = input()
    if musician.isspace():  #检测字符串是否只包含空格
        exit()
    else:
        dlm.downloadMusic(musician)