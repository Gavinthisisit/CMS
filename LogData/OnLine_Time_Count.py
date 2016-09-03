#coding=utf-8

import sys,os
import string

def getAction(action):
    t = action.index('\\')
    s1 = action[t+1:]
    t = s1.index('\\')
    s2 = s1[t+1:]
    t = s2.index('\\')
    return s2[t+1:]

def Log_time_action_Count(filename):
    action_type_set = set()
    obj = open(filename,'r')
    line = obj.readline()
    if line == '':
        return {},set()
    b = line.split('\t')
    num = string.atoi(b[0])
    log_count_all = {}
    line = obj.readline()
    log_count_one = {}
    action_count = {}
    flag = 0
    pretime = 0
    timecount = 0
    while line:
        b = line.split()        
        if len(b) == 1:
            log_count_one['OL_Time'] = timecount
            log_count_one['Action_Count'] = action_count
            log_count_all[num] = log_count_one
            log_count_one = {}
            timecount = 0
            action_count = {}
            flag = 0
            num = string.atoi(b[0])
            line = obj.readline()
            continue
                            #deal with each line in log file
        
                            #online time count
        if len(b) <1:
            continue
        if flag == 0:
            timecount = 0
            pretime = string.atoi(b[6])
            flag = 1
        else:
            curtime = string.atoi(b[6])
            time = curtime - pretime
            if(time <= 600):
                timecount += time
            pretime = curtime
        #action count
        acstring = b[2]
        action = getAction(acstring)
        if action not in action_type_set:
            action_type_set.add(action)
        if action_count.has_key(action):
            action_count[action] += 1
        else:
            action_count[action] = 1
        line = obj.readline()
    log_count_one['OL_Time'] = timecount
    log_count_one['Action_Count'] = action_count
    log_count_all[num] = log_count_one
    obj.close()
    return log_count_all,action_type_set
    
def PrintFile(outfilename,log_count_all,action_type_set):
    out = open(outfilename,'w')
    line = 'Author\t'
    tmpstr = ''
    for type in action_type_set:
        tmpstr += '%s\t' % (type)
    line += tmpstr
    line += '%s\t%s' % ('ActionCount','Time')
    out.write(line+'\n')
    for num in log_count_all:
        log_count_one = log_count_all[num]
    #n.append(string.atoi(num))
        line = '%s\t' % (num)
        action_count = log_count_one['Action_Count']
        tmpstr = ''
        count = 0
        for action in action_type_set:
            if action in action_count:
                tmpstr += '%s\t' % (action_count[action])
                count += int(action_count[action])
            else:
                tmpstr += '%s\t' % (0)
        line += tmpstr
        line += '%s\t%s' % (count,log_count_one['OL_Time'])
        out.write(line+'\n')
    out.close()

if __name__ == '__main__':
    dir = "D:/Dataprocess/LogData/"
    filelist = os.listdir(dir)
    for file in filelist:
        filename = dir + '/' + file
        log_count_all,action_type_set = Log_time_action_Count(filename)
        outfilename = dir + 'OO_Time_' + file
        print outfilename
        PrintFile(outfilename,log_count_all,action_type_set)
