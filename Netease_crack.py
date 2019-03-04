from Crypto.Cipher import AES
import base64
import requests
import sys
import binascii
import os
import json


class Crack(object):
    "网易data参数破解"

    def __init__(self):
        self.iv = b"0102030405060708"
        self.EncSecKey_param1 = "010001"
        self.EncSecKey_param2 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.first_key = b"0CoJUm6Qyw8W8jud"
        self.data = {
            "params": "",
            "encSecKey": "",
        }

    def getData(self, text):
        "得到post请求中的data参数"
        #两个参数中用到的second_key要相同
        second_key = self.createKey(16)
        self.data["params"] = self.getParams(text, second_key)
        self.data["encSecKey"] = self.getEncSecKey(second_key)
        return self.data

    def getParams(self, text, second_key):
        "得到第一个参数：params"
        #两次aes加密
        text = self.encrypt(text, self.first_key)
        text = self.encrypt(text, second_key)
        return text

    def getEncSecKey(self, second_key):
        "得到第二个参数：EncSecKey"
        #由于EncSecKey所需要的第一个参数为随机值，而后两个数为定值，故可以采用固定的EncSecKey值，见Neteasedownlodmusic1.py
        second_key = second_key[::-1]  #从后往前复制一遍（倒序），-1为步长
        rs = pow(
            int(binascii.hexlify(second_key), 16),
            int(self.EncSecKey_param1, 16),
            int(self.EncSecKey_param2, 16))  #pow(x,y,z)≈x**y%z，因为x,y都不能为float型
        #format中的"x"表示将rs转化为16进制
        return format(rs, "x").zfill(256)

    def createKey(self, size):
        "产生16个2进制数"
        #首先产生随机的16个随机值（包括数字和字母，二进制），然后转换为16进制（纯数字，每位数据会转化为二位16进制数，转换后数据长度变为32
        return binascii.hexlify(os.urandom(size))[:16]

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


if __name__ == '__main__':
    pass

    