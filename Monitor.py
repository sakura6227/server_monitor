import psutil
import Configure
import SystemInfo
import Alert
import time
import Loger
import threading

def cpuInfoCheck(cpuInfo):
    count = 0
    for rate in cpuInfo:
        if rate >= systemInfo.cpu_upper_limit or rate <= systemInfo.cpu_lower_limit:
            count += 1
    if count == len(cpuInfo):
        return True
    return False


def memInfoCheck(memInfo):
    if memInfo.percent >= systemInfo.mem_upper_limit or memInfo.percent <= systemInfo.mem_lower_limit:
        return True
    return False


def diskInfoCheck(diskInfo):
    if diskInfo.percent >= systemInfo.disk_alert_limit:
        return True
    return False


def netInfoCheck(netInfo, interface):
    try:
        speed = netInfo[interface]
    except:
        return True
    if (speed[0] >= systemInfo.net_upload_upper_limit or speed[0] <= systemInfo.net_upload_lower_limit) and (
                    speed[1] <= systemInfo.net_down_lower_limit or speed[1] >= systemInfo.net_down_upper_limit):
        return True
    return False


def weekReport():
    _errorType = ['PROC_ERROR', 'CPU_RATE', 'EMAIL_SEND_FAILED', 'NET_RATE', 'DISK_SPACE', 'MEM_RATE']
    file = open('Monitor-' + logFileName + '.log', 'r')

    global logFileName
    logFileName = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    global logger
    logger = Loger.Loger('Monitor-' + logFileName + '.log')

    errorDict = logAnalyse(file)
    report = 'Week Report\n'

    cpuError = 'CPU abnormal times: ' + str(errorDict[_errorType[1]])
    procError = 'Process abnormal exit times: ' + str(errorDict[_errorType[0]])
    emailError = 'Mail sent the number of errors: ' + str(errorDict[_errorType[2]])
    netError = 'Network traffic anomaly times: ' + str(errorDict[_errorType[3]])
    diskError = 'Full capacity of hard disk times: ' + str(errorDict[_errorType[4]])
    memError = 'Insufficient memory times: ' + str(errorDict[_errorType[5]])

    alertcenter.alert_week(emailInfo=mailInfo, Receiver=receiver, logger=logger, weekInfo=(report + cpuError + '\n' + procError + '\n' + emailError + '\n' + netError + '\n' + diskError + '\n' + memError))

    global t
    t = threading.Timer(60 * 60 * 24 * 7, weekReport)
    t.start()

def logAnalyse(file):
    _errorType = ['PROC_ERROR', 'CPU_RATE', 'EMAIL_SEND_FAILED', 'NET_RATE', 'DISK_SPACE', 'MEM_RATE']
    errorDict = {}

    for _error in _errorType:
        errorDict[_error] = 0

    for line in file:
        line = str(line)
        line = line.split()
        logTime = str(line[0]) + ' ' + str(line[1])
        logType = str(line[2])

        if 'ERROR' == logType:
            errorType = str(line[3])
            errorDict[errorType] += 1
        elif 'DEBUG' == logType:
            print 'do debug'
        elif 'INFO' == logType:
            print 'do info'
        else:
            print 'can not handle this %s' % logType

    return errorDict

def deBugOutPut():
    pids = psutil.pids()
    systemInfo.getMemInfo(pids)
    print systemInfo.processInfo_mem

if __name__ == '__main__':
    # config setter
    config = Configure.Configure('./config.xml')

    # log file
    logFileName=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    logger = Loger.Loger('Monitor-' + logFileName + '.log')

    # system info get
    systemInfo = SystemInfo.SystemInfo(pids=None, processName=None)

    # alert center
    alertcenter = Alert.Alert()

    # process names
    processNames = []

    # email info
    mailInfo = None
    receiver = []

    # alert limit define
    # region

    # alert limit configure
    cpuAlertCount = int(systemInfo.cpu_wait_time)
    cpuAlertCounter = 0

    memAlertCount = int(systemInfo.mem_wait_time)
    memAlertCounter = 0

    netAlertCount = int(systemInfo.net_wait_time)
    netAlertCounter = 0

    alertIgnore = {'cpu': 0,
                   'mem': 0,
                   'net': 0,
                   'disk': 0,
                   'pro': 0}

    # interval time
    interval = 0.0

    # endregion

    systemInfo.setCpuLimit(config.getCpu())
    systemInfo.setDiskLimit(config.getDisk())
    systemInfo.setMemLimit(config.getMem())
    systemInfo.setNetLimit(config.getNet())
    interval = float(str(config.getInterval()))
    processNames = config.getProc()
    mailInfo = config.getEmail()
    receiver = config.getRecevier()
    interface = config.getNet().interface

    # start timer -- week report
    t = threading.Timer(60 * 60 * 24 * 7, weekReport)
    t.start()

    # preread the process info
    procs = psutil.process_iter()
    pinfos = {'':0}
    for p in procs:
        try:
            pinfo = p.as_dict(attrs=['name', 'cpu_percent'])
        except psutil.NoSuchProcess:
            print 'error: can not get proc info'
        else:
            pinfos[pinfo['name']] = pinfo['cpu_percent']

    while True:
        weekReport()
        exit(0)

        alertcenter.alertInfos = ''
        # check cpu usage rate
        systemInfo.getCpuInfo()
        if cpuAlertCounter > cpuAlertCount:
            # call the alert moduel
            # print 'cpu alert'
            if alertIgnore['cpu'] <= 0 :
                alertcenter.cpuAlert(systemInfo.sysInfo_cpu)
                alertIgnore['cpu'] = 100 * cpuAlertCount
                logger.log_Error('CPU_RATE')

            alertIgnore['cpu'] -= 1
            cpuAlertCounter = 0
        if cpuInfoCheck(systemInfo.sysInfo_cpu[1]):
            cpuAlertCounter += 1
        else:
            cpuAlertCounter = 0

        # check mem usage rate
        systemInfo.getMemInfo()
        if memAlertCounter > memAlertCount:
            # calthe alert moduel
            # report the top 10 process
            # print 'mem alert'
            if alertIgnore['mem'] <= 0:
                alertcenter.memAlert(systemInfo.sysInfo_mem)
                alertIgnore['mem'] = 100 * memAlertCount
                logger.log_Error('MEM_RATE')

            alertIgnore['mem'] -= 1
            memAlertCounter = 0
        if memInfoCheck(systemInfo.sysInfo_mem[0]):
            memAlertCounter += 1
        else:
            memAlertCounter = 0

        # check disk usage rate
        systemInfo.getDiskInfo()
        if diskInfoCheck(systemInfo.sysInfo_disk[0]):
            # call alert moduel
            # report the detail usage
            # print 'disk alert'
            if alertIgnore['disk'] == 0 :
                alertcenter.diskAlert(systemInfo.sysInfo_disk)
                alertIgnore['disk'] = 1
                logger.log_Error('DISK_SPACE')
        else:
            alertIgnore['disk'] = 0

        # check net usage rate
        systemInfo.getNetInfo()
        if netAlertCounter > netAlertCount:
            # call alert moduel
            # report the up/download speed
            # print 'net alert'
            if alertIgnore['net'] <= 0 :
                alertcenter.netAlert(interface=interface, netInfo=systemInfo.sysInfo_net)
                alertIgnore['net'] = 100 * netAlertCount
                logger.log_Error('NET_RATE')
            alertIgnore['net'] -= 1
            netAlertCounter = 0
        if netInfoCheck(systemInfo.sysInfo_net, interface):
            netAlertCounter += 1
        else:
            netAlertCounter = 0

        # check process info
        notExist = systemInfo.getPidByProcessName(processName=processNames)
        if notExist != None and len(notExist) > 0:
            if alertIgnore['pro'] == 0 :
                # print notExist
                alertcenter.procAlert(notExist)
                logger.log_Error('PROC_ERROR ' + str(notExist))
                alertIgnore['pro'] = 1
        else:
            alertIgnore['pro'] = 0

        alertcenter.alert(emailInfo=mailInfo, Receiver=receiver, logger=logger)

        time.sleep(interval)

        # end of main