#-*- coding:utf-8 -*-

from src import Global
from src.TryRun import TryRun
from re import compile
from src.Print import Print

@TryRun
def Judge(Msg, KeyWords = '', ReWords = '', Type = 'Plain', target = '', mode = 'strict'):
    '''
    判断函数，对消息链中的消息进行判断
    KeyWords传入关键词，可以为字符串，list或者tuple
    ReWords传入正则匹配表达式
    Type可以判断消息类型
    target判断Type为At时的@对象
    '''

    #解析消息链，记录消息类型及出现的位置Locate
    Words = {}; Locate = 0
    for i in Msg['messageChain']:
        if i['type'] in Words:
            Words[i['type']].append(Locate)
        else:
            Words[i['type']]=[Locate,]
        Locate += 1

    if Type == 'Plain':
        if KeyWords:
            if type(KeyWords) == str:
                KeyWords = [KeyWords,]

            #默认值为True，当不相等时赋值为False
            flag = True
            #没有文字消息
            if 'Plain' not in Words:
                return False
            #逐条消息链进行解析
            for i in Words['Plain']:
                TextList = Msg['messageChain'][i]['text'].split()
                if len(TextList) < len(KeyWords):
                    return False
                for a,b in zip(KeyWords, TextList):
                    if a != b:
                        flag = False
                if flag:
                    return True
                else:
                    flag = True
            return False
        elif ReWords:
            Re = compile(ReWords)
            if 'Plain' not in Words:
                return False
            for i in Words['Plain']:
                if Re.search(Msg['messageChain'][i]['text']):
                    return True
            return False
        else:
            raise Exception('缺少必要的判断参数')
    if Type == 'At':
        if 'At' not in Words:
            return False
        if target:
            for i in Words['At']:
                if target == str(Msg['messageChain'][i]['target']):
                    return True
            return False
        else:
            return False
    if Type == 'Image':
        if 'Image' in Words:
            return True
        else:
            return False
    if Type == 'Quote':
        if 'Quote' in Words:
            return True
        else:
            return False
    raise Exception('未指定判断的类型')
