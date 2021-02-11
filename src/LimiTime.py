#-*- coding:utf-8 -*-

from multiprocessing import Process
from src.SendMsg import SendMsg
from src import Global
from src.Daemon import Daemon
from sys import exit

def LimiTime(delayTime):
    '''
    时间控制装饰器，为需要控制运行时间的功能提供时间控制
    由于join会阻塞程序运行，所以以子进程方式实现
    
    !!!
    使用该装饰器的程序尽量以exit结束程序
    目前并不清楚两个拥有相同sessionKey的进程监听统一机器人会发生什么不可描述的事情
    !!!

    delayTime：运行时间，单位 s
    LogMsg = None：需要发送的消息，默认为None，即不发送消息(实验性，不推荐用)
    '''
    def decorator(func):
        def NewFunc(*args,**kw):
            #克隆子进程用以监视process进程，防止阻塞父进程
            DaeStatus = Daemon(Exit = False)
            if DaeStatus == 1:
                return 0
            elif DaeStatus == -1:
                exit(0)
            p = Process(target=func, args=args, kwargs=kw)
            p.start()
            p.join(delayTime)
            if p.is_alive():
                p.terminate()
               # if LogMsg:
               #     SendMsg(Global.AdminQQ, targetType = 'Friend', Text = LogMsg)

            exit(0)

        return NewFunc
    return decorator

@LimiTime(20)
def Test(delayTime):
    '''
    时间控制装饰器Test函数
    '''
    from time import sleep
    sleep(delayTime)
    SendMsg(Global.AdminQQ, targetType = 'Friend', Text = 'awaken')
    exit(0)
