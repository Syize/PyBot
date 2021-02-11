#-*- coding:utf-8 -*-

from requests import get as rget
from json import dumps, loads
from src.Download import Download
from src.LimiTime import LimiTime
from src.SendMsg import SendMsg
from src import Global
from random import randint

@LimiTime(180)
def Setu(*args, **kwargs):
    '''
    色图函数，通过调用Lolicon的setu API获取p站链接并发送
    通过独立的进程发送图片，所有的参数都会传递给SendMsg函数
    必须的参数只有target和targetType = ''，请谨慎传入其他参数
    其他具体参数请看SendMsg函数
    '''
    #先调用API获取链接，达到调用次数之后发送已保存的图片
    APIKEY = '34705994602111f77bc924'
    REQ = {
            'apikey':APIKEY,
            'size1200':True
            }
    SetuData = loads(rget('https://api.lolicon.app/setu/', dumps(REQ)).text)
    #判断是否调用成功
    if SetuData['code'] != 0:
        SendMsg(*args, Text = '已达到调用次数限制', **kwargs)
        if 'SetuDic' not in dir(Global):
            try:
                from os import listdir, environ
                Global.SetuDic = {}
                Global.SetuDic['list'] = [ f for f in listdir(environ['HOME'] + '/Downloads/PyBot/Setu') if not f.startswith('.')]
                Global.SetuDic['num'] = len(Global.SetuDic['list'])
            except:
                SendMsg(*args, Text = '你还没有保存图片', **kwargs)
        Url = 'http://localhost:34000/' + Global.SetuDic['list'][randint(0, Global.SetuDic['num'])]
        SendMsg(*args, ImageUrl = Url, **kwargs)

        exit(0)
    Pid = SetuData['data'][0]['pid']
    Url = SetuData['data'][0]['url']
    SendMsg(*args, ImageUrl = Url, **kwargs)
    #SendMsg(*args, Text = Url, ImageUrl = Url, **kwargs)
    Download(Url, Pid, Path = 'Setu')
    Global.SetuDic['num'] += 1
    Global.SetuDic['list'].append(str(Pid))
    exit(0)

#Test
#@TryRun
#def Setu():
#    Url = 'https://i.pixiv.cat/img-original/img/2019/12/20/17/46/25/78384488_p0.png'
#    Download(Url, 'test.png', Path = '/home/syize/App/MiraiLoader/PyBot/Data/Setu')
#    return Url
