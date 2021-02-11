#!/bin/sh

echo "examine files.."
cd ..
if [ ! -f mcl.jar ]
then
	echo "没有检测到MiraiLoader: mcl.jar，请检查文件是否完整、名字是否正确"
	exit 1
fi
MiraiPATH=`pwd`
cd PyBot
chmod +x PyBotMain.py
echo "Install execute \"QQBot\""

cat>QQBot<<EOF
#!/bin/bash

BOTPATH=$MiraiPATH
DAEMON="0"

cd \$BOTPATH

while getopts ":dhs:" opt
do
        case \$opt in
                d)
                        DAEMON="1";;
                s)
                        A=\$OPTARG;;
		h)
			Help=1;;
        esac
done

if [ "\$A" == "start" ]
then
        JPID=\`ps afx | grep mcl | grep Sl | awk '{print \$1}'\`
        PyPID=\`ps -e | grep PyBotMain | awk '{print \$1}'\`
        if [ "\$DAEMON" != "1" ]
        then
                echo "不以守护进程启动脚本时，请使用screen或者tmux以使服务不会意外中止"
        fi

        #检查文件结构是否正确
        if [ "\$JPID" == "" ]
        then
                echo "正在检查文件..."
                if [ ! -d ./PyBot/Data ]
                then
                        mkdir -p PyBot/Data
                        touch PyBot/Data/setting
                fi

                echo "启动mirai服务..."
                nohup java -jar mcl.jar 1>mcl.log 2>1 &
                sleep 5s
        else
                echo "MiraiLoader已启动，PID: \$JPID"
        fi
        if [ "\$PyPID" == "" ]
        then
                echo "启动Bot服务..."
                cd PyBot
                if [ "\$DAEMON" == "1" ]
                then
                        ./PyBotMain.py \$*
                        JPID=\`ps afx | grep mcl | grep Sl | awk '{print \$1}'\`
                        PyPID=\`ps -e | grep PyBotMain | awk '{print \$1}'\`
                        echo "Done!"
                        echo "MiraiLoader运行PID: \$JPID"
                        echo "PyBotMain运行PID: \$PyPID"
                else
                        ./PyBotMain.py \$*
                fi
        else
                echo "PyBot已启动，PID: \$PyPID"
        fi
elif [ "\$A" == "stop" ]
then
        JPID=\`ps afx | grep mcl | grep Sl | awk '{print \$1}'\`
        PyPID=\`ps -e | grep PyBotMain | awk '{print \$1}'\`
        if [ "\$PyPID" != "" ]
        then
                kill "\$PyPID"
        fi
        if [ "\$JPID" != "" ]
        then
                kill "\$JPID"
        fi
        echo "Done!"
elif [ "\$A" == "restart" ]
then
        if [ "\$DAEMON" != "1" ]
        then
                echo "不以守护进程启动脚本时，请使用screen或者tmux以使服务不会意外中止"
        fi

        PyPID=\`ps -e | grep PyBotMain | awk '{print \$1}'\`
        if [ "\$PyPID" != "" ]
        then
                kill "\$PyPID"
        fi
        cd "\$BOTPATH/PyBot"
        ./PyBotMain.py \$*
        PyPID=\`ps -e | grep PyBotMain | awk '{print \$1}'\`
        echo "Restart Finished!"
        echo "PyBotMain PID: \$PyPID"
elif [ "\$Help" == 1 ]
then
	echo "Usage: QQBot -s [start|restart|stop] (-d|-m|-M)"
	echo "\t-s start: 启动MiraiLoader及PyBot\n\n\t   restart: 重启PyBot\n\n\t   stop: 结束MiraiLoader及PyBot"
	echo "\t-d 以守护进程运行PyBot\n\t-m 启用PyBot邮件托管功能\n\n-M 重新设置邮件信息"
else
        echo "错误的命令"
fi
EOF
chmod +x QQBot

if [ -d "$HOME/.local/bin" ]
then
	echo "cp QQBot >> ~/.local/bin"
	cp QQBot "$HOME/.local/bin/"
else
	if [ -d "/usr/local/bin" ]
	then
		echo "cp QQBot >> /usr/local/bin"
		echo "Please Enter Password"
		sudo cp QQBot /usr/local/bin/
	fi
fi
rm QQBot
echo "Generate Folders"
if [ ! -d Data ]
then
	mkdir Data
	touch Data/setting
fi
echo "Installation done"
echo "Usage:"
echo "    QQBot -s [start|restart|stop] (-d|-h)"
