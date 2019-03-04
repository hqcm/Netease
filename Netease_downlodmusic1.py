from Crypto.Cipher import AES
import base64
import requests
import sys


class Neteasedownlodmusic(object):
    def __init__(self):
        self.iv = b"0102030405060708"
        self.first_key = b"0CoJUm6Qyw8W8jud"

    def encrypt(self, text, key):
        "AES加密"
        # text(str)不是16的倍数需要补足为16的倍数
        missing_padding = 16 - len(text) % 16
        if missing_padding:
            text += chr(missing_padding) * missing_padding
        # text和key要为二进制
        encryptor = AES.new(key, AES.MODE_CBC, self.iv)
        encrypt_text = encryptor.encrypt(text.encode("utf-8"))  # text转化为二进制
        encrypt_text = base64.b64encode(encrypt_text).decode("utf-8")
        return encrypt_text

    def getParams(self, text):
        "得到第一个参数：params"
        #两次aes加密
        text = self.encrypt(text, self.first_key)
        text = self.encrypt(text, self.iv)
        return text


if __name__ == '__main__':
    music_id = 497527639
    text = "{\"ids\":\"[%d]\",\"br\":128000,\"csrf_token\":\"\"}" % int(
        music_id)
    dlm = Neteasedownlodmusic()
    params = dlm.getParams(text)
    url = "https://music.163.com/weapi/song/enhance/player/url?csrf_token="
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'referer':
        'http://music.163.com/',
    }
    data = {
        "params": params,
        "encSecKey": "852f924c411794129a46e17f5ef95a5e9b5388a599201fd6308529beffc8add2c4677a25ad8360fb57f559605c08f010dc97b724547082e89714b4829427c8be7e13573112c2cc41ec38e8dce0d51cf4d35b1f698119f4f88c1c51542f1957dcb2d5716122b136b6859cb35a7e9cc8deb24f24245a7b1093df8146dabf2874a4",
    }
    html = requests.post(url, headers=headers, data=data).json()
    music_url = html["data"][0]["url"]
    name = sys.path[0] + "/%s.mp3" % html["data"][0]['id']
    music = requests.get(music_url)
    with open(name, "wb") as f:
        f.write(music.content)
