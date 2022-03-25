from flask import Flask, request, jsonify
import json
import imaplib
import email
import time
import requests


def is_chinese(string):

    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False



def GetEmails(lt):

    TodayEmailCount = 0
    UnseenEmailCount = 0
    From = ''
    Title = ''


    imaplib.Commands['ID'] = ('AUTH')
    conn = imaplib.IMAP4_SSL(port='993', host='imap.163.com')
    conn.login('WXJ921374497@163.com', 'xxxxxx')# 第一个参数是邮箱名，第二个是imap授权码（好像叫这个名字）

    # 上传客户端身份信息 随便填
    args = ("Mr.w", "client", "contact", "WXJ921374497@163.com", "version", "1.0.0", "vendor", "myclient")

    typ, dat = conn._simple_command('ID', '("' + '" "'.join(args) + '")')

    conn.select(readonly=True)  # 设置为readonly 否则未读邮件会被更改为已读
    unseendata = conn.search(None,'UNSEEN')
    UnseenEmailCount = len(unseendata[1][0].split())


    data = conn.search(None, 'ALL')  # 返回一个元组，data为此邮箱的所有未读邮件数据
    #邮件列表
    msgList = data[1]
    lenv = len(msgList[0].split())

    mons = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

    year=lt.tm_year
    mon = lt.tm_mon
    day = lt.tm_mday


    for i in range(1,30):
        # try:
            #测试出最后一个就是第一封
            if i <lenv+1:
                last = msgList[0].split()[lenv-i]
                #取最后一封
                type, datas = conn.fetch(last, '(RFC822)')
                # print("11",datas[0][1])

                # 用email库获取解析数据 ignore太重要了，因为不知道它，代码多调了一个小时 参考CSDN博主 WotChin

                msg=email.message_from_string(datas[0][1].decode("utf-8","ignore"))
                # msg = email.message_from_string(str(datas[0][1]))  # 用email库获取解析数据
                # print(type(msg))
                msgCharset = email.header.decode_header(msg.get('Subject'))[0][1]  # 获取邮件标题并进行进行解码，通过返回的元组的第一个元素我们得知消息的编码
                # print("---",msg.get('From').split('<')[-1].split('>')[0])


                if msg.get('Date').split(",")[-1].split(" ")[0] is "":
                    time = msg.get('Date').split(",")[-1].split(" ")[1:4]
                else:

                    time = msg.get('Date').split(",")[-1].split(" ")[0:3]
                print(time)
                if int(time[0])==int(day) and int(mons[time[1]])==int(mon) and int(time[2])== int(year):
                    print("Today has new Email!")
                    TodayEmailCount = TodayEmailCount+1

                if msgCharset is None:
                    msg1 = msg.get('Subject')

                else:
                    msg1 = email.header.decode_header(msg.get('Subject'))[0][0].decode(msgCharset)  # 获取标题并通过标题进行解码

                if i == 1:
                    From = msg.get('From').split('<')[-1].split('>')[0]
                    Title = msg1
                    print(Title)
                    Title = Title.replace("\n", "")
                    Title = Title.replace("\r", "")
                    Title = Title.replace("\\n", "")
                    Title = Title.replace("\\r", "")
                    print(Title)
                    if is_chinese(Title):
                        Title = "Chinese EMail"

        # except:
        #     print("error in ",i)
    print(TodayEmailCount,UnseenEmailCount,From,Title)
    if UnseenEmailCount is 0 :
        Title = ""
        From =  ""
    json_data = {'TodayEmailCount': TodayEmailCount,
                 'UnseenEmailCount':UnseenEmailCount,
                 'From':From,
                 'Title':Title}
    return json_data

app = Flask(__name__)
app.debug = True

@app.route('/test1/', methods=['POST'])
def test1():
    json_data = {'time': time.localtime()}
    return jsonify(json_data)

@app.route('/mail/', methods=['GET', 'POST'])
def GetEmail():
    url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
    r = requests.get(url)
    data = json.loads(r.text).get('data')['t']
    data = list(data)
    data[10] = '.'
    data = ''.join(data)
    lt = time.localtime(float(data))
    json_data = GetEmails(lt)
    print(json_data)
    return jsonify(json_data)

@app.route('/whatever/', methods=['GET', 'POST'])

def WTF():
    return






if __name__ == '__main__':
    # 192.168.147.240
    app.run(host='192.168.147.240', port=8888)
    # 指定地址和端口号