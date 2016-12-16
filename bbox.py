'''
creat the connection on the map

'''



# coding=utf-8


import os,sys

datadir = 'D:\Dataprocess\Home_Data\data'

testdir = 'D:\Dataprocess\pre_MapData'
print testdir
datalist = os.listdir(datadir)
testlist = os.listdir(testdir)

print testlist
flen = len(datalist)
for i in range(flen):
    datafile = datalist[i]
    testfile = testlist[i]
    testfilename = testdir + '\\' +testfile
    obj = open(testfilename,'r')
    test_dict = {}
    for line in obj.readlines():
        fields = line.strip('\n').split('\t')
        tested = fields[0]
        test_point = fields[2]
        test_dict[tested] = test_point
    obj.close()
    datafilename = datadir + '\\' + datafile
    obj = open(datafilename,'r')
    flines = obj.readlines()
    flen = len(flines)
    print datafilename,'-----',testfilename
    for i in range(flen):
        line = flines[i]
        fields = line.strip('\n').split('\t')
        stu = fields[0]
        test_point = fields[2]
        if test_point == 'None' and stu in test_dict:
            fields[2] = test_dict[stu]
        else:
            print stu
        line = '%s\t%s\t%s\t%s\t%s\t%s\n' % (fields[0],fields[1],fields[2],fields[3],fields[4],fields[5])
        flines[i] = line
    
    obj = open(datafilename,'w')
    line = '%s\t%s\t%s\t%s\t%s\t%s\n' % ('user', 'code_point', 'test_point', 'time_level', 'action_count', 'time_count')
    obj.write(line)
    obj.writelines(flines)
    obj.close()