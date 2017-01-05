#coding=utf-8

import os,sys

reload(sys)
sys.setdefaultencoding('utf-8')



def get_Home_Work_Data(homework_dir, logdata_dir, code_outdir, test_outdir):

    '''
    homework_dir = 'D:\Dataprocess\homework'
    logdata_dir = 'D:\Dataprocess\LogTimeData'

    code_outdir = 'D:\Dataprocess\Home_Data\data_bak'
    test_outdir = 'D:\Dataprocess\Test Data'
    '''
    
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
        if i < 10:
            outname = code_outdir + '\\' + '0%s' % (i) +'_homedata.txt'
        else:
            outname = code_outdir + '\\' + str(i) +'_homedata.txt'
        outfd = open(outname,'w')
        line = '学生\t代码成绩\t测试成绩\t提交时间\t动作统计\t在线时长\n'
        outfd.write(line)
        for user_id in work_dict:
            code_grade = work_dict[user_id][0]
            uploadtime = work_dict[user_id][1]
            if user_id in test_dict:
                if test_dict[user_id][0] != 'None':
                    test_grade = 0.0 - float(test_dict[user_id][0])
                else:
                    test_grade = test_dict[user_id][0]
            else:
                test_grade = 'None'
                print user_id
            if user_id in log_dict:
                action_count = log_dict[user_id][0]
                time_count = log_dict[user_id][1]
            else:
                print workname,logname,user_id
                action_count = 0
                time_count = 0
            line = '%s\t%s\t%s\t%s\t%s\t%s' % (user_id,code_grade,test_grade,uploadtime,action_count,time_count)        
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
    