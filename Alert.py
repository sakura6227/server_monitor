import psutil
import copy
import Email
import time

class Alert(object):
    def __init__(self):
        self.alertInfos = ''

    # alert, send email to admin
    def alert(self, emailInfo, Receiver, logger):
        if len(self.alertInfos) >0:
            t = time.strftime('%a, %d %b %Y %H:%M:%S %z')
            tmpEmail = Email.Email()
            tmpEmail.setBaseInfo(emailInfo)
            tmpEmail.sendMails(t + '\n' + self.alertInfos, Receiver, logger)
            # print  t + '\n' + self.alertInfos
            # Log.log_Info(self.alertInfos);
            self.alertInfos = ''

    # week report
    def alert_week(self, emailInfo, Receiver, logger, weekInfo):
        t = time.strftime('%a, %d %b %Y %H:%M:%S %z')
        tmpEmail = Email.Email()
        tmpEmail.setBaseInfo(emailInfo)
        tmpEmail.sendMails(t + '\n' + weekInfo, Receiver, logger)

    # cpu alert, send top 10 process' cpu percent
    def cpuAlert(self, cpuInfo):
        alertInfo = 'CPU Number is ' + str(cpuInfo[0]) + '\n'
        alertInfo += 'Current rate in each CPU: ' + '\n'
        count = 1
        for cpu in cpuInfo[1] :
            alertInfo += '      #' + str(count) + '     ' + str(cpu) + '%\n'
            count += 1

        procs = psutil.process_iter()
        pinfos = {}
        for p in procs:
            try:
                pinfo = p.as_dict(attrs=['name', 'cpu_percent'])
            except psutil.NoSuchProcess:
                print 'error: can not get proc info'
            else:
                pinfos[pinfo['name']] = pinfo['cpu_percent']

        pinfos = sorted(pinfos.iteritems(), key=lambda d: d[1], reverse=True)
        pinfos = pinfos[0:10]

        for p in pinfos :
            alertInfo += '      ' + str(p) + '\n'

        self.alertInfos += alertInfo
        return alertInfo

    # mem alert, send top 10 process' mem percent
    def memAlert(self, memInfo):
        alertInfo = 'Physical memory: ' + self.sizeConvert(memInfo[0].total) + ' total ' + str(memInfo[0].percent) + '% used ' + self.sizeConvert(memInfo[0].available) + ' available' +'\n'
        alertInfo += 'Swap Memory: ' + self.sizeConvert(memInfo[1].total) + ' total ' + str(memInfo[1].percent) + '% used ' + self.sizeConvert(memInfo[1].free) + ' free' +'\n'
        alertInfo += 'Current Memory Infomation: ' + '\n'

        procs = psutil.process_iter()
        pinfos = {}
        for p in procs:
            try:
                pinfo = p.as_dict(attrs=['name', 'memory_percent'])
            except psutil.NoSuchProcess:
                print 'error: can not get proc info'
            else:
                pinfos[pinfo['name']] = round(pinfo['memory_percent'], 2)

        pinfos = sorted(pinfos.iteritems(), key=lambda d: d[1], reverse=True)
        pinfos = pinfos[0:10]

        for p in pinfos:
            alertInfo += '      ' + str(p) + '\n'

        self.alertInfos += alertInfo
        return alertInfo

    # disk alert, send percentage of free, size of disk, free size, used size
    def diskAlert(self, diskInfo):
        alertInfo = 'Disk: ' + self.sizeConvert(diskInfo[0].total) + ' total ' + str(diskInfo[0].percent) + '% used ' + self.sizeConvert(diskInfo[0].free) + ' free' + '\n'

        self.alertInfos += alertInfo
        return alertInfo

    # net alert, send current net rate
    def netAlert(self, netInfo, interface):
        # print netInfo, interface
        alertInfo = 'Net ' + interface + ': upload speed: ' + str(netInfo[interface][0]) + 'KB/s download speed: ' + str(netInfo[interface][1]) + 'KB/s\n'

        self.alertInfos += alertInfo
        return alertInfo

    # process alert, send the process which is not running
    def procAlert(self, procName):
        alertInfo = 'Not Running Process are: '
        for _procName in procName:
            alertInfo +=  _procName + '  '
        alertInfo += '\n'

        self.alertInfos += alertInfo
        return alertInfo

    def sizeConvert(self, size):
        _size = copy.deepcopy(size)
        try :
            _size = int(_size)
        except:
            _size = 0
        tb = _size / (1 << 40)
        _size -= tb * (1 << 40)
        gb = _size / (1 << 30)
        _size -= gb * (1 << 30)
        mb = _size / (1 << 20)
        ans = ''
        if tb != 0:
            ans += str(tb) + 'TB '
        if gb != 0:
            ans += str(gb) + 'GB '
        if mb != 0:
            ans += str(mb) + 'MB'
        if tb == 0 and gb == 0 and mb == 0:
            ans = str(_size) + 'KB'
        return ans
