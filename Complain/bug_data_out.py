#coding=utf-8
import MySQLdb

def getMessage(message):
    retval = ''
    init = message.find('<')
    if(init != 0):
        retval = message[0:init]
        message = message[init+1:]
    while len(message) != 0:
        first = message.find('>')
        second = message.find('<')
        diff = second-first
        if second == -1:
            break
        if diff > 1:
            retval = retval + message[first+1:second]
        message = message[second+1:]
    return retval

con = MySQLdb.connect(host="localhost",user='root',passwd='12345678',db = 'course',charset='utf8')
cursor = con.cursor()

complain_dict = {}
sql = "SELECT * FROM `mdl_complain` where course=7"
cursor.execute(sql)
complain_result = cursor.fetchall()
for ret in workshop_result:
    complain_id = ret[0]
    complain_name = ret[2]
    if complain_id not in complain_dict:
        complain_dict[complain_id] = [complain_name]

sql = "SELECT id,complainid,title,userid,timecreated FROM `mdl_complain_discussions`"
cursor.execute(sql)
dis_result = cursor.fetchall()
for ret in sub_result:
    complain_id = ret[1]
    userid = ret[3]
	title = ret[2]
    discussion_id = ret[0]
    timecreated = ret[4]
    if complain_id in complain_dict:
        complain_dict[complain_id].append([discussion_id,title,userid,timecreated])
sql = "SELECT * FROM `mdl_complain_posts`"
cursor.execute(sql)
post_result = cursor.fetchall()
discussion_dict = {}
parent_dict = {}
for ret in post_result:
    post_id = ret[0]
    parentid = ret[2]
    user_id = ret[3]
    discussion_id = ret[1]
    raw_message = ret[8]
	message = getMessage(raw_message)
    if discussion_id not in discussion_dict:
        discussion_dict[discussion_id] = []
		discussion_dict[discussion_id].append([post_id,parentid,userid,message])
	else:
		discussion_dict[discussion_id].append([post_id,parentid,userid,message])
	if parent != '0':
		parent_dict[parentid] = post_id
reply_dict = {}
for id in complain_dict:
	complaindir = './Complain/' + complain_dict[id][0]
	os.mkdir(complaindir)
    discussion_list = complain_dict[id]
    title = '作者\tAdvice\tIncomplete\tError\tCrash\tDoc\t测试时间\t分数\t评测人\n'

    out.write(title)
    for discussion in discussion_list[1:]:
        print discussion
        discussion_id = discussion[0]
		title = discussion[1]
        author = discussion[2]
        time = discussion[3]
		filename = complaindir+'/'+filename+'.txt'
		out = open(filename,'w')
		post_list = discussion_dict[discussion_id]
		tab_dict = {}
		if len(post_list) == 1:
			reply_dict[discussion_id] = 'None'
		else:
			reply_dict[discussion_id] = 'Yes'
		for post in post_list:
			parent_id = post[1]
			post_id = post[0]
			user_id = post[2]
			post_message = post[3]
			if parent_id  != '0':
				tab_dict[post_id] = tab_post[parent_id] + 1
				line = '\t'*tab_dict[post_id] + '%s\t%s' % (post_message,user_id)
				out.write(line+'\n')
			else:
				post_id = post[0]
				user_id = post[2]
				post_message = post[3]
				tab_dict[post_id] = 0
				line = '\t'*tab_dict[post_id] +'%s\t%s' % (post_message,user_id)
				out.write(line+'\n')
		out.close()
	filename = complaindir + '/' + 'Replay_Count.txt'
	out = open(filename,'w')
	for id in reply_dict		
		line = '%s\t%s' % (id,reply_dict[id])
		out.write(line+'\n')
	out.close()
