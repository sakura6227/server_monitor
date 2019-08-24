import xml.dom.minidom
from collections import namedtuple

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class Configure(Singleton):
    def __init__(self, configureFilePath):
        try:
            self.xml = xml.dom.minidom.parse(configureFilePath)
        except IOError:
            print 'can not open ' + configureFilePath + ' , please check the file'
            exit(-1)
        else:
            print 'open the file success, reading the file now'

    def getEmail(self):
        EmailConfig = namedtuple('EmailConfig', ['host', 'user', 'password', 'sender'])

        host = self.getElement(tagName='email', attr='host')
        user = self.getElement(tagName='email', attr='user')
        password = self.getElement(tagName='email', attr='password')
        sender = self.getElement(tagName='email', attr='sender')

        return EmailConfig._make([str(host), str(user), str(password), str(sender)])

    def getRecevier(self):
        receivers = []
        tags = self.getTags(tagName='receiver')

        for rec in tags:
            receivers.append(str(rec.getAttribute('address')))

        return receivers

    def getCpu(self):
        CpuConfig = namedtuple('CpuConfig', ['up', 'down', 'wait_time'])
        up = self.getElement(tagName='cpu_upper_limit')
        down = self.getElement(tagName='cpu_lower_limit')
        wait_time = self.getElement(tagName='cpu_wait_time')

        return CpuConfig._make([up, down, wait_time])

    def getMem(self):
        MemConfig = namedtuple('MemConfig', ['up', 'down', 'wait_time'])
        up = self.getElement(tagName='mem_upper_limit')
        down = self.getElement(tagName='mem_lower_limit')
        wait_time = self.getElement(tagName='mem_wait_time')

        return MemConfig._make([up, down, wait_time])

    def getDisk(self):
        DiskConfig = namedtuple('DiskConfig', ['limit'])
        limit = self.getElement(tagName='disk_alert_limit')

        return DiskConfig._make([limit])

    def getNet(self):
        NetConfig = namedtuple('NetConfig', ['up_up', 'up_down', 'down_up', 'down_down', 'wait_time', 'interface'])
        up_up = self.getElement(tagName='net_upload_upper_limit')
        up_down = self.getElement(tagName='net_upload_lower_limit')
        down_up = self.getElement(tagName='net_down_upper_limit')
        down_down = self.getElement(tagName='net_down_lower_limit')
        wait_time = self.getElement(tagName='net_wait_time')
        interface = self.getElement(tagName='net_interface')

        return NetConfig._make([up_up, up_down, down_up, down_down, wait_time, interface])

    def getProc(self):
        procName = []
        tags = self.getTags('proc')

        for proc in tags:
            procName.append(str(proc.getAttribute('name')))

        return procName

    def getNetInterface(self):
        intrefaces = []
        tags = self.getTags('net_interface')

        for interface in tags:
            intrefaces.append(str(interface.getAttribute('value')))

        return intrefaces

    def getInterval(self):
        return self.getElement('interval')

    # def getLogFilePath(self):
    #     return self.getElement(tagName='log', attr='filepath')

    def getTags(self, tagName):
        root = self.xml.documentElement
        tags = root.getElementsByTagName(tagName)

        return tags

    def getElement(self, tagName, attr='value'):
        tags = self.getTags(tagName)[0]

        return tags.getAttribute(attr)