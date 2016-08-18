#coding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")

log_dir = 'D:\Dataprocess\Log'
work_dir = 'D:\Dataprocess\homework'


def setLevel(grade):
    if point == 'None':
        return 'E'
    if round(float(point)) < -20.0:
        return 'D'
    elif round(float(point)) >= -20.0 and round(float(point)) < -5.0:
        return 'C'
    elif round(float(point)) >= -5.0 and round(float(point)) < -1.0:
        return 'B'
    elif round(float(point)) >= -1.0 and round(float(point)) <= 0.0:
        return 'A'

file_list = os.listdir(work_dir)            
for file in file_list:
    filename = work_dir + '/' + file
    lines = open(filename,'r').readlines()
    lines[0] = lines[0].strip('\n') + '\t作业等级\n'
    flen = len(lines)-1
    for i in range(1,flen):
        fields = lines[i].strip('\n').split('\t')
        point = fields[1]
        level = setLevel(point)
        lines[i] = lines[i].strip('\n') + '\t%s\n' % (level)
    open(filename,'w').writelines(lines)