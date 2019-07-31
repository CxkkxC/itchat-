import time
from threading import Timer
import requests
import json
import itchat
from itchat.content import *
# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
def tuling(info):
  appkey = "f461f3c34bc0401fbcfddded709b8b24"
  url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
  req = requests.get(url)
  content = req.text
  data = json.loads(content)
  answer = data['text']
  return answer

def isMsgFromMyself(msgFromUserName):
    # 检查是否自己发送的
    global myName
    return myName == msgFromUserName

'''
# 注册文本消息，绑定到text_reply处理函数
# text_reply msg_files可以处理好友之间的聊天回复
@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
  itchat.send('%s' % tuling(msg['Text']),msg['FromUserName'])
itchat.run()
#itchat.logout()#退出登录
'''
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    global zhuRenReply, timerSet, noReply, t
    if isMsgFromMyself(msg['FromUserName']):
        #print("有人回复")
        zhuRenReply = False
        noReply = False
        try:
            t.cancel()
            #print("计时器清零")
            timerSet = False
        except:
            pass
        return None
    
    if zhuRenReply:
        defaultReply = '我已经接收到你的消息: ' + msg['Text']
        reply = tuling(msg['Text'])
        return reply or defaultReply
    else:
        noReply = True
        if not timerSet:
            print("等待图灵机器人开启开始计时")
            t = Timer(59, sendBusyStatus,[msg['FromUserName']])
            '''
            #计时函数
            Timer(interval, function, args=[], kwargs={}) 
            interval: 指定的时间(秒数) 
            function: 要执行的方法 
            args/kwargs: 方法的参数
            '''
            t.start()
            timerSet = True
            '''  
            t.cancel()
            cancel()方法都是为了清除任务队列中的任务
            '''

def sendBusyStatus(UserName):
    global noReply, zhuRenReply, timerSet
    print("一分钟已到图灵机器人开启")
    if noReply:
        itchat.send("主人一分钟内没回复，说明我的主人没空噢！让我先陪你聊一会吧", UserName)
        zhuRenReply = True
        timerSet = False
        
itchat.auto_login()
zhuRenReply, timerSet, noReply = False, False, False
t=0
myName = itchat.get_friends(update=True)[0]['UserName']
itchat.run()
