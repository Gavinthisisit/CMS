#coding=utf-8
'''
    count the entropy of distribution
'''
import os,sys
from numpy import *

def distEclud(vecA, vecB):
    sum = 0.0
    for i in range(len(vecA)):
        sum += power(vecA[i] - vecB[i],2)
    return sqrt(sum)
    
def count_Entropy(datadir):
    filelist = os.listdir(datadir)
    for datafile in filelist:
        datafilename = datadir + '\\' + datafile
        obj = open(datafilename,'r')
        flines = obj.readlines()
        data_dict = {}
        for line in flines:
            fields = line.strip('\n').split('\t')
            stu = fields[0]
            code_point = fields[1]
            test_point = fields[2]
            data_dict[stu] = [float(code_point),float(test_point)]
        entropy = 0
        for line in flines:
            fields = line.strip('\n').split('\t')
            stu = fields[0]
            tester = fields[3]
            entropy += distEclud(data_dict[stu],data_dict[tester])
        
        print datafilename,entropy
'''
        obj = open(datafilename,'w')
        line = '%s\n' % (entropy)
        obj.write(line)
        obj.writelines(flines)
        obj.close()
'''        
if __name__ == '__main__':
    filedir = 'D:\Dataprocess\pre_MapData'
    count_Entropy(filedir)