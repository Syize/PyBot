#-*- coding:utf-8 -*-

from src import Global
from requests import post
from json import loads, dumps
from src.TryRun import TryRun

@TryRun
def JoinGroup(Msg):
    '''
    让Bot自动同意拉群申请，已在主函数中禁用
    '''
    Response = {
            'sessionKey':Global.sessionKey,
            'eventId':Msg['eventId'],
            'fromId':Msg['fromId'],
            'groupId':Msg['groupId'],
            'operate':0,
            'message':'已同意申请'
            }
    post(Global.ListenURL + '/resp/botInvitedJoinGroupRequestEvent', dumps(Response))
