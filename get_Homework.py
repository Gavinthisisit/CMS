#coding=utf-8

import os,sys


dir = 'D:\Dataprocess\homework'

filelist = os.listdir(dir)

for file in filelist:
    filename = dir + '\\' + file
    lines = open(dir+'\\'+file ,'r').readlines()
    flen = len(lines)
    for i in range(flen):
        line = lines[i]
        fields = line.strip('\n').split('\t')
        if len(fields) < 6:
            continue
        line = '%s\t%s\t%s\t%s\t%s\n' % (fields[0],fields[1],fields[2],fields[3],fields[4])
        lines[i] = line
    open(filename,'w').writelines(lines)
