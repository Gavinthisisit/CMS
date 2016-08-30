#coding=utf-8

import os,sys

reload(sys)
sys.setdefaultencoding('utf-8')

homework_dir = 'D:\Dataprocess\homework'
logdata_dir = 'D:\Dataprocess\LogTimeData'

code_outdir = 'D:\Dataprocess\Code Data'
test_outdir = 'D:\Dataprocess\Test Data'

homework_list = os.listdir(homework_dir)
log_list = os.listdir(logdata_dir)
i = 0
for work in homework_list:
    work_dict = {}
    test_dict = {}
    workname = homework_dir+'\\'+work
    work_fd = open(workname,'r')
    for line in work_fd.readlines()[1:]:
        fields = line.strip('\n').split('\t')
        user_id = fields[0]
        work_dict[user_id] = [fields[1],fields[2]]
        test_id = fields[3]
        test_dict[test_id] = [fields[1]]
    log_dict = {}
    logname = logdata_dir+'\\'+log_list[i]
    log_fd = open(logname,'r')
    for line in log_fd.readlines()[1:]:
        fields = line.strip('\n').split('\t')
        user_id = fields[0]
        action_count = fields[-2]
        time_count = fields[-1]
        log_dict[user_id] = [action_count,time_count]
    i += 1
 ##作业数据   
    outname = code_outdir + '\\' + str(i)+'_codedata.txt'
    outfd = open(outname,'w')
    line = '学生\t成绩\t提交时间\t动作统计\t在线时长\n'
    outfd.write(line)
    for user_id in work_dict:
        grade = work_dict[user_id][0]
        uploadtime = work_dict[user_id][1]
        if user_id in log_dict:
            action_count = log_dict[user_id][0]
            time_count = log_dict[user_id][1]
        else:
            print workname,logname,user_id
            action_count = 0
            time_count = 0
        line = '%s\t%s\t%s\t%s\t%s' % (user_id,grade,uploadtime,action_count,time_count)        
        outfd.write(line+'\n')
    outfd.close()
##测试数据    
    outname = test_outdir + '\\' + str(i)+'_testdata.txt'
    outfd = open(outname,'w')
    line = '学生\t成绩\t动作统计\t在线时长\n'
    outfd.write(line)
    for user_id in test_dict:
        grade = test_dict[user_id][0]
        if user_id in log_dict:
            action_count = log_dict[user_id][0]
            time_count = log_dict[user_id][1]
        else:
            print workname,logname,user_id
            action_count = 0
            time_count = 0
        line = '%s\t%s\t%s\t%s' % (user_id,grade,action_count,time_count)        
        outfd.write(line+'\n')
    outfd.close()