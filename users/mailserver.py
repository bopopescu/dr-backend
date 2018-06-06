import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import get_template

from templates import verificationEmail, forgetOtp
# logger = get_task_logger(__name__)
# username = 'tnpnotifier@gmail.com'
# password = 'tnpnotify.exe'
# fromaddr = 'tnpinfo@gmail.com'
# server_name = "smtp.gmail.com"
# port = 587
# print "korkudeepak"
server_name = "smtp.iitd.ernet.in"
port = 25
username = "ee3140505@iitd.ac.in"
fromaddr = 'ee3140505@iitd.ac.in'
password = "Korku02Alisha2"
# server = smtplib.SMTP(server_name, port)
# server.set_debuglevel(1)
# server = smtplib.SMTP(server_name, port)
# server.ehlo()
# server.starttls()
# server.login(username, password)

print "korku"

class MailServer(object):
    # username = 'tnpnotifier@gmail.com'
    # password = 'tnpnotify.exe'
    # fromaddr = 'tnpinfo@gmail.com'
    # server_name = "smtp.gmail.com"
    # port = 587

    server_name = "smtp.iitd.ernet.in"
    port = 25
    username = "ee3140505@iitd.ac.in"
    fromaddr = 'ee3140505@iitd.ac.in'
    password = "Korku02Alisha2"
    # server = smtplib.SMTP(server_name, port)
    print "ttls"

    def __init__(self, subject, toaddrs):
        self.toaddrs  = toaddrs
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = subject
        self.msg['From'] = self.fromaddr
        self.msg.add_header('reply-to', '<>')
        self.server = smtplib.SMTP(server_name, port)
        # print "ttlstatti"
        self.server.ehlo()
        # print "ttlsgoo"
        self.server.starttls()
        # print "ttls"
        self.server.login(self.username, self.password)

    # def attach(self, filename, f):
    #     attachment = MIMEText(f.read())
    #     attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    #     self.msg.attach(attachment)
    #
    def message_body(self, text):
        self.msg.attach(MIMEText(text,'html'))

    def send(self):
        self.msg['To'] = self.toaddrs
        self.server.sendmail(self.fromaddr, self.toaddrs, self.msg.as_string())
        self.quit()

    def quit(self):
        self.server.quit()


def sendemail(subject,toaddrs,msg):
    server=MailServer(subject,toaddrs)
    server.message_body(msg)
    server.send()

# @task()
def sendtemplatemail(subject,toaddrs,msg,**kwargs):
    # try:
        server=MailServer(subject,toaddrs)
        server.message_body(msg)
        server.send()
    # except Exception as e:
    #     logger.info("Unable to send email. Error: " + str(e))


def send_registration_mail(toaddrs,user_name,otp):
    subject ="Welcome to messfeedback System"
    msg = 'The link for email verification is '+' '+'http://127.0.0.1:8080/verifyemail?email_token='+otp
    kwargs = {'user_name':user_name,'otp':otp}
    sendtemplatemail(subject=subject,toaddrs=toaddrs,msg=msg,vars=kwargs)

def send_verification_mail(toaddrs,user_name,otp):
    subject ="Welcome to messfeedback System"
    href='http://localhost:8000/#!/verifyemail?email_token='+otp
    kwargs = {'user_name':user_name,'otp':otp}
    msg = verificationEmail(user_name, otp, href)
    sendtemplatemail(subject=subject,toaddrs=toaddrs,msg=msg,vars=kwargs)

def send_forgotpassword_mail(toaddrs,user_name,otp):
    subject = "Welcome to messfeedback System"
    msg = forgetOtp(user_name, otp)
    kwargs = {'user_name':user_name,'otp':otp}
    sendtemplatemail(subject=subject,toaddrs=toaddrs,msg=msg,vars=kwargs)
