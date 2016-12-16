#coding=utf-8

import os,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines

def getFileLines(filename):
    obj = open(filename)
    return obj.readlines()

def getData(filelines):
    for line in filelines:
        fields = line.strip("\n").split('\t')
        x_point = fields[1]
        y_point = fields[2]
        if x_point == 'None':
            x_point = random(-20,0)
        if y_point == 'None':
            y_point = random(-20,0)
        if author_id not in point_dict:
            t = ['None','None','None']
            t[0] = point
            t[2] = tester_id
            point_dict[author_id] = t
        else:
            point_dict[author_id][0] = point
            point_dict[author_id][2] = tester_id
        
        if tester_id not in point_dict:
            t = ['None','None','None']
            t[1] = point
            point_dict[tester_id] = t
        else:
            point_dict[tester_id][1] = point
    print min
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