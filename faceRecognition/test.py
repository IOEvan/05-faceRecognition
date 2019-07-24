#coding:utf-8   #强制使用utf-8编码格式
from time import ctime,sleep
import requests
import json

desti_url = 'http://wechat.laixuanzuo.com/index.php/reserve/index.html?f=wechat&from_code=WwsBBVEBBQs%3D&n=5d2c82b7a68bb'
web_data = requests.get(desti_url)
