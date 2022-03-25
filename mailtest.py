#-*- encoding: utf-8 -*-
#-*- encoding: gbk -*-
import imaplib
import email
import re
import chardet
# import InfoOutPut



# 添加缺失的命令
imaplib.Commands['ID'] = ('AUTH')

conn = imaplib.IMAP4_SSL(port='993', host='imap.163.com')
conn.login('WXJ921374497@163.com', 'HMHGNBDSPCRAFMOV')

# 上传客户端身份信息
args = ("Mr.w", "client", "contact", "WXJ921374497@163.com", "version", "1.0.0", "vendor", "myclient")
typ, dat = conn._simple_command('ID', '("' + '" "'.join(args) + '")')
print(conn._untagged_response(typ, dat, 'ID'))
conn.select()
data = conn.search(None, 'ALL')  # 返回一个元组，data为此邮箱的所有邮件数据
#邮件列表
msgList = data[1]
len = len(msgList[0].split())
#最后一封
last = msgList[0].split()[len-2]
#取最后一封
type, datas = conn.fetch(last, '(RFC822)')
print(datas)

#把取回来的邮件写入txt文档

msg=email.message_from_string(datas[0][1].decode("utf-8"))#用email库获取解析数据
msgCharset = email.header.decode_header(msg.get('Subject'))[0][1]  # 获取邮件标题并进行进行解码，通过返回的元组的第一个元素我们得知消息的编码
print("------",msg)
print(msgCharset)
msg1=email.header.decode_header(msg.get('Subject'))[0][0].decode(msgCharset)#获取标题并通过标题进行解码
# print("Message %s\n%s\n"%(msg1))#打印输出标题
with open('email.txt','w')as f:
    # coding = chardet.detect(datas[0][1])
    # print(coding)
    f.write(msg1)
conn.logout()






