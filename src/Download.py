#-*- coding:utf-8 -*-

from src.TryRun import TryRun
from src.Daemon import Daemon
from sys import exit
from requests import get as rget
from os import environ, remove
from os import makedirs as mkdirs

###########################################################
# Q:如何让Download不阻塞程序执行(已解决)
# A:Daemon方法有问题
# A:子线程方法有待尝试
###########################################################

@TryRun
def Download(Url, Name, Path = None, Dae = False):
    '''
    下载模块，配合色图模块使用，但我还是分离了出来，以供开发更多用途
    Url：下载链接
    Name：文件保存名称
    Path = None：文件保存路径，默认为$HOME/Downloads/PyBot
    Dae = False：是否以子进程的形式启动下载，这将分离出一个单独的子进程进行下载，以保证不会阻塞主进程
    '''
    if Dae:
        Status = Daemon(Exit = False)
    else:
        Status = 0
    if Status == 1:
        pass
    elif Status == -1:
        exit(0)
    else:
        SavePath = environ['HOME'] + '/Downloads/PyBot'
        try:
            f=open(SavePath + '/.test', 'w')
            f.close()
        except:
            mkdirs(SavePath + '/')
        Name = str(Name)
        #新建同名文件存储链接，以防下载失败
        if Path:
            try:
                f = open(SavePath + '/' + Path + '/.test', 'w')
                f.close()
            except:
                mkdirs(SavePath + '/' + Path)
            with open(SavePath + '/' + Path + '/' + Name, 'w') as f:
                f.write(Url)
        else:
            with open(SavePath + '/' + Name, 'w') as f:
                f.write(Url)
        proxies = {'http':'http://127.0.0.1:7890'}
        Results = rget(Url, proxies = proxies)
        if Path:
            with open(SavePath + '/' + Path + '/' + Name, 'wb') as f:
                f.write(Results.content)
        else:
            with open(SavePath + '/'  + Name, 'wb') as f:
                f.write(Results.content)
        if Dae:
            return 0
        else:
            exit(0)
