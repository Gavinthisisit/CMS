#!bin/python

#coding=utf-8

import sys,os

def data_PreProcess(dirpath):

    dirpath = 'D:\Dataprocess\Home_Data\data_bak'

    file_list = os.listdir(dirpath)

    if len(file_list) <= 0:
        sys.exit(1)
    else:
        for file in file_list:
            filename = dirpath+'\\'+file
            obj = open(filename,'r')
            max_time = 0
            min_time = 2000000000
            tmp_dict = {}
            for line in obj.readlines()[1:]:
                fields = line.strip('\n').split('\t')
                author = fields[0]
                code_grades = fields[1]
                test_grades = fields[2]
                uploadtime = int(fields[3])
                #viewer = fields[3]
                action_count = fields[4]
                time_count = fields[5]
                if max_time < uploadtime:
                    max_time = uploadtime
                if min_time > uploadtime:
                    min_time = uploadtime
                if author not in tmp_dict:
                    if code_grades != 'None':
                        tmp_dict[author] = [code_grades,test_grades,uploadtime,action_count,time_count]
            obj.close()
            print max_time,min_time
            interval = (max_time-min_time)/10
            outfilename = filename    #file.strip('.txt')+'_timeeven.txt'
            out = open(outfilename,'w')
            for uid in tmp_dict:
                info = tmp_dict[uid]
                code_grades = info[0]
                test_grades = info[1]
                uploadtime = info[2]
                uploadtime_level = (uploadtime-min_time)/interval
                action_count = info[3]
                time_count = info[4]
                line = '%s\t%s\t%s\t%s\t%s\t%s' % (uid,code_grades,test_grades,float(uploadtime_level)/10,float(action_count)/100,float(time_count)/1000)
                out.write(line+'\n')
            out.close()
            
        
            
         