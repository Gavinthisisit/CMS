#coding=utf-8
import MySQLdb
import sys,os
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

def getConnection():
    try:
        con = MySQLdb.connect(host="localhost",user='root',passwd='12345678',db = 'course',charset='utf8')
        cursor = con.cursor()
    except Exception,e:
        print 'DataBase Connection Error!errmsg=%s' % (e)
    return cursor

def getComplainData(cursor):
    complain_dict = {}
    sql = "SELECT * FROM `mdl_complain` where course=7"
    cursor.execute(sql)
    complain_result = cursor.fetchall()
    for ret in complain_result:
        complain_id = ret[0]
        complain_name = ret[3]
        if complain_id not in complain_dict:
            complain_dict[complain_id] = [complain_name]

    sql = "SELECT id,complain,name,userid,timemodified FROM `mdl_complain_discussions`"
    cursor.execute(sql)
    dis_result = cursor.fetchall()
    for ret in dis_result:
        complain_id = ret[1]
        userid = ret[3]
        title = ret[2]
        discussion_id = ret[0]
        timecreated = ret[4]
        if complain_id in complain_dict:
            complain_dict[complain_id].append([discussion_id,title,userid,timecreated])
    return complain_dict
def getDiscussionData(cursor):
    sql = "SELECT * FROM `mdl_complain_posts`"
    cursor.execute(sql)
    post_result = cursor.fetchall()
    discussion_dict = {}
    parent_dict = {}
    first_post_dict = {}
    for ret in post_result:
        post_id = ret[0]
        parentid = ret[2]
        user_id = ret[3]
        discussion_id = ret[1]
        raw_message = ret[8]
        message = getMessage(raw_message)
        if parentid == 0:
            first_post_dict[discussion_id] = [post_id]
        if discussion_id not in discussion_dict:
            discussion_dict[discussion_id] = []
            discussion_dict[discussion_id].append([post_id,parentid,user_id,message])
        else:
            discussion_dict[discussion_id].append([post_id,parentid,user_id,message])
        if parentid != '0':
            parent_dict[parentid] = post_id
    return discussion_dict,parent_dict,first_post_dict
def PrintFile(complain_dict,discussion_dict,parent_dict,first_post_dict):
    reply_dict = {}
    for id in complain_dict:
        complaindir = './Complain/' + complain_dict[id][0]
        os.mkdir(complaindir)
        discussion_list = complain_dict[id]
        for discussion in discussion_list[1:]:
            print discussion
            discussion_id = discussion[0]
            title = discussion[1]
            author = discussion[2]
            time = discussion[3]
            filename = complaindir+'/'+title+'.txt'
            out = open(filename,'w')
            post_list = discussion_dict[discussion_id]
            tab_dict = {}
            pre_id = first_post_dict[discussion_id]
            tab_dict[pre_id] = 0
            tmpid = parent_dict[pre_id]
            while tmpid:
                tab_dict[tmpid] = tab_dict[pre_id] + 1
                pre_id = tmpid
                if pre_id in parent_dict:
                    tmpid = parent_dict[pre_id]
                else:
                    tmpid = 0
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
                #tab_dict[post_id] = tab_dict[parent_id] + 1
                line = '\t'*tab_dict[post_id] + '%s\t%s' % (post_message,user_id)
                out.write(line+'\n')
            else:
                post_id = post[0]
                user_id = post[2]
                post_message = post[3]
                #tab_dict[post_id] = 0
                line = '\t'*tab_dict[post_id] +'%s\t%s' % (post_message,user_id)
                out.write(line+'\n')
        out.close()
        filename = complaindir + '/' + 'Replay_Count.txt'
        out = open(filename,'w')
        for id in reply_dict:
            line = '%s\t%s' % (id,reply_dict[id])
            out.write(line+'\n')
        out.close()

def _delete_dir_and_file(dirpath):
    try:
        if not os.path.isfile(dirpath):
            list = os.listdir(dirpath)
            for dir_or_file in list:
                _delete_dir_and_file(dirpath+'/'+dir_or_file)
            os.rmdir(dirpath)
        os.remove(dirpath)
    except Exception,e:
        print '_delete_dir_and_file failed! name=%s,errmsg=%s' % (dirpath,e)
        sys.exit(0)
def _init_(dirname):
    try:
        if os.path.exists(dirname):
            file_list = os.listdir(dirname)
            if len(file_list) != 0:
                _delete_dir_and_file(dirname)
        
        else:
            os.mkdir(dirname)
    except Exception,e:
        print "_init_ failed! err:%s\tdirname:%s"  % (e,dirname)
        sys.exit(1)

if __name__ == '__main__':
    dirname = './Complain'
    _init_(dirname)
    cursor = getConnection()
    complain_dict = getComplainData(cursor)
    discussion_dict,parent_dict,first_post_dict = getDiscussionData(cursor)
    PrintFile(complain_dict,discussion_dict,parent_dict,first_post_dict)
