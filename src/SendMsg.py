#-*- coding:utf-8 -*-

from src import Global
from src.TryRun import TryRun
from requests import post
from json import loads, dumps
#from src.Print import Print

@TryRun
def SendMsg(target, Text = '', ImageUrl = '', ImageID = '',
        AtID = '', msgChain = '', targetType = 'Group',
        AtAll = False, mode = False
        ):
    '''
    发送消息函数
    对应参数项代表对应消息类型
    图片发送有两种方式：url上传，ID发送服务器缓存
    mode = True会启用旧的图片发送方式(尽管不被开发者推荐使用)
    AtAll@全体，AtID@个人，不发送群消息时自动忽略
    AtAll会覆盖掉AtID
    targetType = ：Group(群)，Friend(好友)，Temp(临时会话)
    msgChain会覆盖掉前面所有的信息，谨慎传參
    '''
    target = int(target)
    SendFlag = False
    if targetType not in ['Group', 'Friend', 'Temp']:
        raise Exception('错误的发送对象 targetType: ', targetType)

    if mode:
        Msg = {
                'sessionKey':Global.sessionKey,
                'target':target,
                'group':target,
                'urls':[ImageUrl,]
                }
#        Print(Msg)
        a = post(Global.ListenURL + '/send' + targetType + 'Message', dumps(Msg))
        return a.text
    else:
        Msg = {
                'sessionKey':Global.sessionKey,
                'target':target,
                'messageChain':[]
                }
        if AtAll and targetType == 'Group':
            Msg['messageChain'].append({
                'type':'AtAll'
                })
            SendFlag = True
        if ImageID:
            Msg['messageChain'].append({
                'type':'Image',
                'imageID':ImageID
                })
            SendFlag = True
        if ImageUrl:
            Msg['messageChain'].append({
                'type':'Image',
                'url':ImageUrl
                })
            SendFlag = True
        if AtID:
            Msg['messageChain'].append({
                'type':'At',
                'target':AtID
                })
            SendFlag = True
        if Text:
            Msg['messageChain'].append({
                'type':'Plain',
                'text':Text
                })
            SendFlag = True
        if msgChain:
            Msg['messageChain'] = msgChain

        if not SendFlag:
            return 0
        if len(Msg['messageChain']) < 1:
            raise Exception('错误!消息链为空，请检查参数')
#        Print('发送消息:\n',Msg)
        post(Global.ListenURL + '/send' + targetType + 'Message', dumps(Msg))
