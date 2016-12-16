#coding=utf-8

import os,sys

dir_path = 'D:\Dataprocess\Code Data'
file_list = os.listdir(dir_path)
for file in file_list:
    lines = open(dir_path+'\\'+file,'r').readlines()
    flen = len(lines)
    for i in range(flen):
        line = lines[i]
        fields = line.strip('\n').split('\t')
        fields[2] = float(fields[2])/10
        strTmp = fields[0]
        for f in fields[1:]:
            if f != '':
                strTmp += "\t%s" % (f)
        strTmp += '\n'
        lines[i] = strTmp
    open(dir_path+'\\'+file,'w').writelines(lines)
