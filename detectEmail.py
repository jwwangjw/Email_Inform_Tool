import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import requests


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def savefile(filename, data, path):
    try:
        filepath = path + filename
        print('Save as: ' + filepath)
        f = open(filepath, 'wb')
    except:
        print(filepath + ' open failed')
        # f.close()
    else:
        f.write(data)
        f.close()


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def print_info(msg):
    content_header = ""
    content_result = ""
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            else:
                hdr, addr = parseaddr(value)
                name = decode_str(addr)
                value = name + ' < ' + addr + ' > '
        content_header = content_header + header + ':' + value + "\n"
    for part in msg.walk():
        filename = part.get_filename()
        content_type = part.get_content_type()
        charset = guess_charset(part)
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode=True)
            if filename != None or filename != '':
                content_result = content_result + 'Accessory: ' + filename + "\n"
        else:
            email_content_type = ''
            content = ''
            if content_type == 'text/plain':
                email_content_type = 'text'
            # elif content_type == 'text/html':
            # email_content_type = 'html'
            if charset:
                content = part.get_payload(decode=True).decode(charset)
            if content_type == "text/plain":
                content_result = content_result + content + "\n"
    return content_header, content_result


email = '******@163.com'
# 163邮箱授权码
password = '*******'
pop3_server = 'pop.163.com'
count = 0
id = 0
while (count >= 0):
    server = poplib.POP3(pop3_server, 110)
    server.user(email)
    server.pass_(password)
    print('Message: %s. Size: %s' % server.stat())

    resp, mails, objects = server.list()
    index = len(mails)
    resp, lines, octets = server.retr(index)
    # 邮件取出的信息是bytes，转换成Parser支持的str
    if id == octets:
        continue
    else:
        lists = []
        for e in lines:
            lists.append(e.decode())
        msg_content = '\r\n'.join(lists)
        msg = Parser().parsestr(msg_content)
        content_header, content_res = print_info(msg)
        print(content_res)
        # 将sendkey替换为在server酱中获取的sendkey，建议使用企业微信
        api = "https://sctapi.ftqq.com/sendkey.send"
        data = {
            "text": content_header,
            "desp": content_res
        }
        req = requests.post(api, data=data)
    if count == 0:
        id = octets
    count = count + 1
server.quit()
