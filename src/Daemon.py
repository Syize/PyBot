#-*- coding:utf-8 -*-

from sys import exit, stdout, stderr, stdin
from os import fork, chdir, umask, setsid, dup2
import signal
#from atexit import register

#忽略子进程信号，防止产生僵尸进程
def Signal():
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

#守护进程函数
def Daemon(pid_file = None, Exit = True):
    '''
    创建守护进程

    传入Exit = False使得父进程不会退出，
    返回1时表示父进程的Daemon执行完毕，
    返回-1表示一级子进程的Daemon执行完毕(此时你可以执行exit以使一级子进程退出
    '''

    #fork第一子进程
    pid = fork()
    #子进程pid为0,父进程大于0
    if pid:
        if Exit:
            exit(0)
        else:
            return 1

    #切换工作目录
    chdir('/')
    #重设文件权限掩码
    umask(0)
    #子进程成为新的会话和进程组长
    setsid()
    #第二次fork
    _pid = fork()
    if _pid:
        if Exit:
            exit(0)
        else:
            return -1
    #第二子进程已成为守护进程
    #重定向标准输入输出错误描述符

    #刷新缓冲区
    stdout.flush()
    stderr.flush()
    #dup2函数将一个文件描述符复制到另一个文件描述符
    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        dup2(read_null.fileno(), stdin.fileno())
        dup2(write_null.fileno(), stdout.fileno())
        dup2(write_null.fileno(), stderr.fileno())

#可选部分，谨慎考虑之后决定通过ps afx | grep XXX | grep Sl的方式获得PID
    #写入pid
#    if pid_file:
#        with open(pid_file, 'w') as f:
#            f.write(str(getpid()))
