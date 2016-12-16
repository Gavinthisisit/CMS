#coding=utf-8

import os,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines

def getFileLines(filename):
    obj = open(filename)
    return obj.readlines()

def getData(filelines):
    
    return point_dict

def WriteFile(point_dict,filename):
    outObj = open(filename,'w')
    for t in point_dict:
        record = point_dict[t]
#        if record[0] == 'None':
#            continue
        line = "%s\t%s\t%s\t%s" % (t,record[0],record[1],record[2])
        outObj.write(line+'\n')

if __name__ == '__main__':
    datadir = 'D:\Dataprocess\homework'
    outdir = 'D:\Dataprocess\pre_MapData'
    filelist = os.listdir(datadir)
    for file in filelist:
        filename = datadir + '\\' +file
        flines = getFileLines(filename)
        p_dict = getData(flines)
        WriteFile(p_dict,outdir+'\\'+file)