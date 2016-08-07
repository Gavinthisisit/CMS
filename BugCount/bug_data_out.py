#coding=utf-8
import MySQLdb

con = MySQLdb.connect(host="localhost",user='root',passwd='12345678',db = 'course',charset='utf8')
cursor = con.cursor()

workshop_dict = {}
sql = "SELECT * FROM `mdl_workshop` where course=7"
cursor.execute(sql)
workshop_result = cursor.fetchall()
for ret in workshop_result:
    workshop_id = ret[0]
    workshop_name = ret[2]
    if workshop_id not in workshop_dict:
        workshop_dict[workshop_id] = [workshop_name]
submission_dict = {}
sql = "SELECT id,workshopid,authorid,timecreated,grade FROM `mdl_workshop_submissions`"
cursor.execute(sql)
sub_result = cursor.fetchall()
for ret in sub_result:
    submission_id = ret[0]
    authorid = ret[2]
    workshop_id = ret[1]
    uploadtime = ret[3]
    sub_grade = ret[4]
    if workshop_id in workshop_dict:
        workshop_dict[workshop_id].append([submission_id,authorid,uploadtime,sub_grade])
sql = "SELECT * FROM `mdl_workshop_assessments`"
cursor.execute(sql)
assessment_result = cursor.fetchall()
assessment_dict = {}
for ret in assessment_result:
    assessment_id = ret[0]
    reviewerid = ret[2]
    assess_grade = ret[6]
    assess_grading = ret[7]
    assess_time = ret[4]
    sub_id = ret[1]
    if sub_id not in assessment_dict:
        assessment_dict[sub_id] = [assessment_id,reviewerid,assess_time]

sql = 'SELECT * FROM `mdl_workshopform_oo`'
cursor.execute(sql)
type_result = cursor.fetchall()
type_dict = {}
for ret in type_result:
    workshop_id = ret[1]
    description = ret[3]
    type_id = ret[0]
    if workshop_id not in type_dict:
        tmp = dict{}
        if 'other' in description or 'advice' in description:
            tmp[type_id] = 'other'
        elif 'comp' in description:
            tmp[type_id] = 'incomplete'
        elif 'error' in description or 'wrong' in description:
            tmp[type_id] = 'error'
        elif 'crash' in description:
            tmp[type_id] = 'crash'
        elif 'Doc' in description:
            tmp[type_id] = 'Document Comment'
        else:
            print 'Warning!!%s\t%s' % (type_id,description)
        type_dict[workshop_id] = tmp
    else:
        if 'other' in description or 'advice' in description:
            type_dict[workshop_id][type_id] = 'other'
        elif 'comp' in description:
            type_dict[workshop_id][type_id] = 'incomplete'
        elif 'error' in description or 'wrong' in description:
            type_dict[workshop_id][type_id] = 'error'
        elif 'crash' in description:
            type_dict[workshop_id][type_id] = 'crash'
        elif 'Doc' in description:
            type_dict[workshop_id][type_id] = 'Document Comment'
        else:
            print 'Warning!!!%s\t%s' % (type_id,description)
            
sql = 'SELECT * FROM `mdl_workshop_grades`'
cursor.execute(sql)
bugs_result = cursor.fetchall()
bugs_dict = {}
for ret in bugs_result:
    ass_id = ret[1]
    dimension_id = ret[3]
    grade = ret[4]
    if ass_id not in bugs_dict:
        tmp = {}
        tmp[dimension_id] = 1
        bugs_dict[ass_id] = tmp
    else:
        if dimension_id not in bugs_dict[ass_id]:
            bugs_dict[ass_id][dimension_id] = 1
        else:
            bugs_dict[ass_id][dimension_id] += 1

        
for id in workshop_dict:
    filename = './Bug/'+workshop_dict[id][0]+'.txt'
    print filename
    out = open(filename,'w')
    submission_list = workshop_dict[id]
    title = '作者\tAdvice\tIncomplete\tError\tCrash\tDoc\t测试时间\t分数\t评测人\n'

    out.write(title)
    for submission in submission_list[1:]:
        print submission
        submission_id = submission[0]
        author = submission[1]
        grade = submission[3]
        
        if submission_id in assessment_dict:
            reviewerid = assessment_dict[submission_id][1]
        else:
            reviewerid = ''
        assessment_id = assessment_dict[submission_id][0]
        assessment_time = assessment_dict[submission_id][2]
        bug_count = [0,0,0,0,0]
        bug_tmp = bug_dict[assessment_id]
        for dim_id in bug_tmp:
            description = type_dict[id][dim_id]
            if 'other' in description or 'advice' in description:
                bug_count[0] = bug_tmp[dim_id]
            elif 'comp' in description:
                bug_count[1] = bug_tmp[dim_id]
            elif 'error' in description or 'wrong' in description:
                bug_count[2] = bug_tmp[dim_id]
            elif 'crash' in description:
                bug_count[3] = bug_tmp[dim_id]
            elif 'Doc' in description:
                bug_count[4] = bug_tmp[dim_id]
            else:
                print 'Warning!!%s\t%s' % (description)
        
        line = '%s\t%s\t%s\t%s' % (author,bug_count[0],bug_count[1],bug_count[2].bug_count[3],bug_count[4],assessment_time,grade,reviewerid)
        line = line+'\n'
        print line
        out.write(line)
    out.close()
con.close()
