# PyBot

依赖于MiraiLoader及mirai-http-api插件的，Python写成的QQ机器人

## 启动过程

1.  启动MiraiLoader，并使用nohup将其挂到后台(**请配置好MiraiLoader的自动登录帐号选项**)
2.  启动PyBot

## 安装

已经写好了一个安装脚本install.sh，只需执行即可

```bash
cd path/to/your/MiraiLoader
git clone https://github.com/Syize/PyBot.git
cd PyBot
chmod +x install.sh
./install.sh
```

## 使用方式

**请先配置好MiraiLoader的自动登录帐号选项，以及设置好你自己的sessionKey(大小写字母数字混合，否则脚本不会使用)**

**然后到src/Global.py中，将你自己的sessionKey填入到对应位置**

**若要使用Setu功能，推荐去 [Lolicon](https://api.lolicon.app/#/setu) 那里申请一个APIKEY，然后在src/Setu.py中更改**

```bash
QQBot -h	#打印出简略的帮助信息
	  -s start|restart|stop		#启动|重启Python进程|停止
	  -d	#以守护进程形式在后台运行
```

一般使用如下命令即可

```bash
QQBot -s start -d
```

要是想看打印出的信息(其实没啥好看的)

```bash
QQBot -s start
```

重启(并不会杀掉MiraiLoader进程，若想完全重启请先stop)

```bash
QQBot -s restart -d
```



