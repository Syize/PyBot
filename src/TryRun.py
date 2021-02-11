#-*- coding:utf-8 -*-

from traceback import format_exc
from src import Global
from src.Print import Print
from requests import post
from json import dumps

def TryRun(func):
    '''
    错误捕获装饰器，发生错误时会自动向超级管理员发送错误信息
    '''
    def ReplyErr(*args, **kw):
        try:
            ReplyMsg = func(*args, **kw)
            return ReplyMsg
        except Exception:
            ErrLog = '有错误发生!\n运行日志:\n' + format_exc()
            Print('\nWARNNING:\n', ErrLog)

            #发送给超级管理员
            msg = {
                    'sessionKey':Global.sessionKey,
                    'target':Global.AdminQQ,
                    'messageChain':[{
                        'type':'Plain',
                        'text':ErrLog
                        }]
                    }
            post(Global.ListenURL + '/sendFriendMessage',
                    dumps(msg))
            return ErrLog
    return ReplyErr
