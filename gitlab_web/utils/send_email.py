# coding:utf-8
# smtplib模块负责连接服务器和发送邮件
# MIMEText：定义邮件的文字数据
# MIMEImage：定义邮件的图片数据
# MIMEMultipart：负责将文字图片音频组装在一起添加附件
import smtplib  # 加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def send_email(receive,account_info=None):
    sender = 'hyf_accountsharing@163.com'  # 发件人邮箱账号
    # receive = 'yfan_hu@qq.com'  # 收件人邮箱账号
    passwd = 'bigcdatbdha2019'
    mailserver = 'smtp.163.com'
    port = '25'
    sub = 'hyf_accountsharing注册回执'

    try:
        msg = MIMEMultipart('related')
        msg['From'] = formataddr(["sender", sender])  # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["receiver", receive])  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = sub
        #文本信息
        #txt = MIMEText('this is a test mail', 'plain', 'utf-8')
        #msg.attach(txt)

        # #附件信息
        # attach = MIMEApplication(open("D:\xx\\tool\pycharm\\1.csv").read())
        # attach.add_header('Content-Disposition', 'attachment', filename='1.csv')
        # msg.attach(attach)

        #正文显示图片
        if account_info:
            body = """
            <b>尊敬的先生/女士:</b> 
            <br>
            <p>恭喜您注册成功！<a href='http://49.235.210.9/hyf2019.com'>点击此处进入网站</a></p>
            <p>您的账户名为：{}</p>
            <p>您的密码为：{}</p>
            <p>您的验证码为：{}</p>
            <br>
            <p>hyf_accountsharing团队致</p>
            <br>
            """.format(account_info['admin_username'],account_info['admin_password'],account_info['admin_verification_code'])
        else :
            body = """
            <b>尊敬的先生/女士:</b> 
            <br>
            <p>很遗憾的通知您，您在我们网站的注册请求被驳回！</p>
            <p>回复此邮件详询</p>
            <br>
            <p>hyf_accountsharing团队致</p>
            <br>
            """
        # <img src="cid:image"><br>
        text = MIMEText(body, 'html', 'utf-8')
        # f = open('D:\xx\pip.png', 'rb')
        # pic = MIMEImage(f.read())
        # f.close()
        # pic.add_header('Content-ID', '<image>')
        msg.attach(text)
        # msg.attach(pic)

        server = smtplib.SMTP(mailserver, port)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(sender, passwd)  # 发件人邮箱账号、邮箱密码
        server.sendmail(sender, receive, msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        print('email sent : success')
        return True
    except Exception as e:
        print('email sent : fail')
        print(e)
        return False