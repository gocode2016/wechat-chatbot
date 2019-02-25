import time
import hashlib
from lxml import etree
from flask import request
from flask import Flask, make_response    # 这些是本例中所有用到的库
import xml.etree.ElementTree as ET


class Message:
    def __init__(self, req):
        self.request = req
        self.token = 'token'
        self.AppID = 'wx04df28a3b87ada99'
        self.AppSecret = 'wx04df28a3b87ada99'

class Content():
    def __init__(self):
        self.ToUserName = 'me'
        self.FromeUserName = 'unknown'
        self.MsgType = 'text'
        self.Content = ''
        self.MsgId = 0

class Config(Message):
    def __init__(self, req):
        super(Config, self).__init__(req)
        self.signature = req.args.get('signature')    # 这里分别获取传入的四个参数
        self.timestamp = req.args.get('timestamp')
        self.nonce = req.args.get('nonce')
        self.echostr = req.args.get('echostr')
        self.return_code = 'Invalid'

    def verify(self):
        data = sorted([self.token, self.timestamp, self.nonce])    # 字典排序
        string = ''.join(data).encode('utf-8')    # 拼接成字符串
        hashcode = hashlib.sha1(string).hexdigest()    # sha1加密
        if self.signature == hashcode:
            self.return_code = self.echostr



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        message = Config(request)
        message.verify()
        return message.return_code

    elif request.method == "POST":
        print('hi')
        xml_str = request.stream.read()
        xml = ET.fromstring(xml_str)
        toUserName=xml.find('ToUserName').text
        fromUserName = xml.find('FromUserName').text
        createTime = xml.find('CreateTime').text
        msgId = xml.find('MsgId').text
        msgType = xml.find('MsgType').text
        if msgType != 'text':
            reply = """
            <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            </xml>
            """ % (
                fromUserName, 
                toUserName, 
                createTime, 
                'text', 
                'Unknow Format, Please check out'
                )
            return reply
        else:
            content = xml.find('Content').text
            msgId = xml.find('MsgId').text
            print(content)
            responses = content.strip("吗？") + " !"
            reply = """
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[%s]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    </xml>
                    """ % (fromUserName, toUserName, createTime, msgType, responses)
            return reply            
if __name__ == "__main__":
    app.run(port=80,debug=True)