#!/usr/bin/python3
#-*- coding:utf-8 -*-

################   import area  #################
from src import Global

def Print(*args, **kwargs):
    '''
    一个对print进行了包装的函数，当PyBot进程成为守护进程时不会进行输出
    '''
    if not Global.daemon:
        print(*args, **kwargs)
