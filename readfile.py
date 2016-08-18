#coding=utf-8

import codecs,os,sys

log_dir = 'D:\Dataprocess\Log'

filelist = os.listdir(log_dir)

filename = log_dir + '/' + filelist[9]
fd = open(filename,'r')
print filename
for line in fd.readlines():
    fields = line.strip('\n').split('\t')
    print len(fields)
