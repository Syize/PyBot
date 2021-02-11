#!/usr/bin/python3
#-*- coding:utf-8 -*-

####################  comments  ######################
# files tree:
# PyBot
# |----------
# |         |
# src     Data
# |         |
# *.py   setting
######################################################


####################  import area  ###################

#custom package
from traceback import format_exc
from sys import exit, argv
from requests import get, post
from json import loads, dumps
import asyncio
from websockets import connect
from getopt import getopt

#DIY package
from src import Global
from src.Print import Print
from src.TryRun import TryRun
from src.Judge import Judge
from src.SendMsg import SendMsg
from src.Daemon import Daemon, Signal
from src.Setu import Setu
from src.LimiTime import Test
from src.JoinGroup import JoinGroup


#######################################################


####################  Global variate  #################
URL = 'http://0.0.0.0:8080'
Global.ListenURL = URL

#######################################################


######################  Functions  ####################
def GetOpt():
    opts, args = getopt(argv[1:], "ds:")
    for i in opts:
        if '-d' in i[0]:
            Global.daemon = True

def ReleaseKey():
    '''
    释放session
    '''
    a = post(URL + '/release', dumps({
        'sessionKey':Global.QQSet['sessionKey'],
        'qq':Global.QQSet['QQNumber']
        }))
    if loads(a.text)['code'] == 0:
        Print('旧sessionKey释放成功')
    else:
        Print('错误! text:\n', a.text)

def CheckSocket():
    '''
    Check websocket
    检查插件的websocket是否开启
    '''
    PluginStatus = get(URL + '/config?sessionKey='
            + Global.sessionKey)
    if loads(PluginStatus.text)['enableWebsocket']:
        Print('Websocket监听已开启')
    else:
        PluginStatus = post(URL + '/config', dumps({
            'sessionKey':Global.sessionKey,
            'enableWebsocket':True
            }))
#        Print('Websocket:\n', PluginStatus.text)
        if loads(PluginStatus.text)['msg'] == 'success':
            Print('Websocket监听已开启')
        else:
            exit('开启Websocket监听失败，退出')

def Auth():
    '''
    认证激活sessionKey
    '''
    GetKey = post(URL + '/auth', dumps({
        'authKey':Global.authKey
        }))
    Global.sessionKey = loads(GetKey.text)['session']
#    Print('sessionKey', Global.sessionKey)
    a = post(URL + '/verify', dumps({
        'sessionKey':Global.sessionKey,
        'qq':Global.QQSet['QQNumber']
        }))
#    Print('校验sessioin:\n', a.text)

def InitQQSet():
    '''
    更新配置
    '''
    Global.QQSet = {}
    Global.QQSet['QQNumber'] = input('请输入机器人QQ:')
    Global.QQSet['AdminQQ'] = input('请输入超级管理员QQ:')
    Auth()
    Global.QQSet['sessionKey'] = Global.sessionKey

def Init():
    '''
    初始化，获取sessionKey或authKey(并认证激活sessionKey)
    检查Websocket监听状态
    '''
    Print('检查配置...')
    if input('是否使用已有配置?y/n:') == 'y':
        try:
            with open('Data/setting', 'r') as f:
                QQSet = loads(f.read())
            if 'QQNumber' not in QQSet:
                QQSet['QQNumber'] = input('请输入机器人QQ:')
            if 'AdminQQ' not in QQSet:
                QQSet['AdminQQ'] = input('请输入超级管理员QQ:')
            if 'sessionKey' not in QQSet:
                Auth()
                QQSet['sessionKey'] = Global.sessionKey
            else:
                Global.QQSet = QQSet
                ReleaseKey()
                Auth()
                QQSet['sessionKey'] = Global.sessionKey
            Global.QQSet = QQSet
            Global.QQNumber = QQSet['QQNumber']
            Global.AdminQQ = QQSet['AdminQQ']
        except Exception:
            Print(format_exc())
            Print('配置为空')
            InitQQSet()
    else:
        InitQQSet()
    #写入配置
    with open('Data/setting', 'w') as f:
        f.write(dumps(Global.QQSet))
    CheckSocket()

async def run():
    '''
    异步监听消息
    '''
    url = 'ws://0.0.0.0:8080/all?sessionKey=' + Global.sessionKey
    async with connect(url) as WS:
        while True:
            Msg = loads(await WS.recv())
            Print('\nMsg:\n', Msg)
            Reply(Msg)

def ReplyFriend(Msg):
    '''
    好友消息回复函数
    '''
    target = str(Msg['sender']['id'])
    if Judge(Msg, KeyWords = 'LimiTime'):
        SendMsg(target, targetType = 'Friend', Text = 'Test Starts')
        Test(10)
        return 0
    #测试指令：test
    if Judge(Msg, KeyWords = 'test') and target == Global.AdminQQ:
        SendMsg(target, targetType = 'Friend', Text = 'Hi!\n我能收到你的消息!:)')
        return 0
    #通用指令：say hello
    if Judge(Msg, KeyWords = ['say', 'hello']):
        SendMsg(target, targetType = 'Friend', Text = 'Hello:)很高兴见到你')
        return 0
    #色图
    if Judge(Msg, ReWords = "来点[\S\s]*好康的"):
        Setu(target, targetType = 'Friend')
        return 0


def ReplyGroup(Msg):
    '''
    群消息回复函数
    '''
    target = Msg['sender']['group']['id']
    
    #通用指令：say hello
    if Judge(Msg, KeyWords = ['say', 'hello']):
        SendMsg(target, Text = 'Hello:)很高兴见到你')
        return 0

    #色图
    if Judge(Msg, ReWords = "来点[\S\s]*好康的"):
        Setu(target)
        return 0


def ReplyTemp(Msg):
    '''
    临时消息回复函数
    '''
    pass


#@TryRun
def Reply(Msg):
    '''
    回复消息函数
    '''
    #空消息
    if len(Msg) < 1:
        return 0
    #好友消息
    if Msg['type'] == 'FriendMessage':
        ReplyFriend(Msg)
    #群消息
    if Msg['type'] == 'GroupMessage':
        ReplyGroup(Msg)
    #临时消息
    if Msg['type'] == 'TempMessage':
        ReplyTemp(Msg)
    #if Msg['type'] == 'BotInvitedJoinGroupRequestEvent':
    #    JoinGroup(Msg)
    #    return 0
    if Msg['type'] == 'BotOfflineEventForce':
        Print('已在另一台设备登录QQ，退出服务...')
        exit(1)


def main():
    GetOpt()
    Init()
    Signal()
    #转为守护进程
    if Global.daemon:
        Daemon()
    asyncio.get_event_loop().run_until_complete(run())

if __name__ == '__main__':
    main()
