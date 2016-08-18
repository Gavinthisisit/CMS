#coding=utf-8
file1 = 'log_file.out'
file2 = 'mdl_logstore_standard_log.out'

log_dict3 = {}
log_dict6 = {}
log_dict7 = {}
log_dict9 = {}
log_dict10 = {}
log_dict11 = {}
log_dict12 = {}
log_dict16 = {}
log_dict17 = {}
log_dict18 = {}
log_dict19 = {}

def getLogData(filename):
    min = 9999999999
    max = 0
    for line in open(filename,'r'):
        fields = line.strip('\n').split('\t')
        uId = fields[2]
        arr = []
        brr = []
        fields[3] = fields[3].strip(' ')
        if len(fields[3]) != 10: 
            continue
        try:
            timecreated = int(fields[3])
        except Exception,e:
            print 'Error!!!%s' % (e)
            continue
        if timecreated > max:
            max = timecreated
        if timecreated < min:
            min = timecreated
        if timecreated>1456965600 and timecreated<1457078400:
            if log_dict3.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict3[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict3[uId] = brr
        elif timecreated>1457521200 and timecreated<1457668800:
            if log_dict6.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict6[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict6[uId] = brr
        elif timecreated>1458100800 and timecreated<1458280800:
            if log_dict7.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict7[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict7[uId] = brr
        elif timecreated>1459735800 and timecreated<1460008800:
            if log_dict9.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict9[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict9[uId] = brr
        elif timecreated>1460710800 and timecreated<1460826000:
            if log_dict10.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict10[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict10[uId] = brr
        elif timecreated>1461322800 and timecreated<1461484800:
            if log_dict11.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict11[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict11[uId] = brr
        elif timecreated>1462323600 and timecreated<1462456800:
            if log_dict12.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict12[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict12[uId] = brr
        elif timecreated>1463104800 and timecreated<1463198400:
            if log_dict16.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict16[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict16[uId] = brr
        elif timecreated>1463752800 and timecreated<1463806800:
            if log_dict17.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict17[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict17[uId] = brr
        elif timecreated>1464962400 and timecreated<1465016400:
            if log_dict18.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict18[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict18[uId] = brr
        elif timecreated>1465646400 and timecreated<1465711200:
            if log_dict19.has_key(uId) == False:
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            else:
                brr = log_dict19[uId]
                id = fields[0]
                event = fields[1]
                arr = [id,event,timecreated]
                brr.append(arr)
            log_dict19[uId] = brr
    print max,min
def Print(outname,log_dict):
    out = open(outname,'w')
    for d in log_dict:
        brr = log_dict[d]
        out.write(str(d)+'\n')
        for b in brr:
            line = ''
            for a in b:
                
                line += line + '%s' % (a) +' '
            line = line+'\n'
            out.write(line)
    out.close()
 
if __name__ == '__main__':
    dir = "D:/Dataprocess/LogData/"
    getLogData(file1)
    getLogData(file2)
    Print(dir + 'log_sqlOut_3.txt',log_dict3)
    Print(dir + 'log_sqlOut_6.txt',log_dict6)
    Print(dir + 'log_sqlOut_7.txt',log_dict7)
    Print(dir + 'log_sqlOut_9.txt',log_dict9)
    Print(dir + 'log_sqlOut_10.txt',log_dict10)
    Print(dir + 'log_sqlOut_11.txt',log_dict11)
    Print(dir + 'log_sqlOut_12.txt',log_dict12)
    Print(dir + 'log_sqlOut_16.txt',log_dict16)
    Print(dir + 'log_sqlOut_17.txt',log_dict17)
    Print(dir + 'log_sqlOut_18.txt',log_dict18)
    Print(dir + 'log_sqlOut_19.txt',log_dict19)
