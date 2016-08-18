#codeing=utf-8

import sys,os

log_dir = 'D:\Dataprocess\Log'
homework_dir = 'D:\Dataprocess\homework'

log_files = os.listdir(log_dir)
homework_files = os.listdir(homework_dir)
log_list = []
for file in log_files:
    log_list.append(file)
i = 0
for file in homework_files:
    delete_list = []
    point_dict = {}
    fd = open(homework_dir+ '/' + file,'r')
    for line in fd.readlines()[1:]:
        fields = line.strip('\n').split('\t')
        print file,fields
        user_id = fields[0]
        if len(fields) < 6:
            continue
        level = fields[4]
        if user_id in point_dict:
            print 'Warning!!!%s' % (user_id)
        else:
            point_dict[user_id] = level
    print file,log_list[i]
    lines = open(log_dir+'/'+log_list[i],'r').readlines()
    flen = len(lines)-3
    lines[0] = lines[0].strip('\n')+'\tlevel\n'
    print lines[0]
    for j in range(1,flen):
        line = lines[j].strip('\n').split('\t')
        user_id = line[0]
        if user_id in point_dict:
            lines[j] = lines[j].strip('\n')+'\t%s\n' % (point_dict[user_id])
    open(log_dir+'/'+log_list[i],'w').writelines(lines)
    i += 1