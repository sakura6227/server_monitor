import smtplib
import copy
import time
import Loger
import Configure
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

class Email(object):
    # sender predefine
    # region
    sender = ''
    mail_host = ''
    mail_user = ''
    mail_pass = ''
    # endregion

    def __init__(self, receiver = None):
        # config = Configure.Configure('./config.xml')
        # self.logger = Loger.Loger(config.getLogFilePath())
        if receiver == None:
            self.receivers = []
        else:
            self.receivers = copy.deepcopy(receiver)

    def sendBaseMail(self, content, receiver, logger):
        msg = MIMEText(_text=content, _subtype='plain', _charset='utf-8')
        msg['From'] = self.addressFormat('Server Alert <%s>' % self.sender)
        msg['To'] = self.addressFormat('Admin <%s>' % receiver)
        msg['Subject'] = Header('Server Alert', 'utf-8').encode()
        msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            # smtpObj.set_debuglevel(1)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, receiver, msg.as_string())
            smtpObj.quit()
        except:
            # print 'send %s failed' % receiver
            logger.log_Error('EMAIL_SEND_FAILED %s' % receiver)

    def sendMails(self, content, receviers, logger):
        for recv in receviers:
            self.sendBaseMail(content, recv, logger)

    def addressFormat(self, add):
        name, address = parseaddr(add)
        return formataddr((Header(name, 'utf-8').encode(), address))

    def setBaseInfo(self, info):
        self.mail_host = info.host
        self.mail_pass = info.password
        self.mail_user = info.user
        self.sender = info.sender
