import os,sys

reload(sys)
sys.setdefaultencoding("utf-8")

#coding=utf-8
import MySQLdb

def getRecords(dirpath):
    con = MySQLdb.connect(host="localhost",user='root',passwd='',db = 'moodle2',charset='utf8')
    cursor = con.cursor()
    sql = "select id from mdl_forum where course = '2'"
    forum = []
    cursor.execute(sql)
    forum_results = cursor.fetchall()
    all_content_file = "all_content.txt"
    allObj = open(al l_content_file,'w')
    for ret in forum_results:
        forum.append(ret[0])
    
    for id in forum:
        dirname = dirpath + '/forum_'
        dirname += str(id)
        os.mkdir(dirname)
        sql = "select * from mdl_forum_discussions where forum = '%s'" % str(id)
        discussion = []
        cursor.execute(sql)
        results = cursor.fetchall()
        for ret in results:
            discussion.append(ret[0])
        dic  = {}
        
        for dis in discussion:
            
            sql = "select * from mdl_forum_posts where discussion = '"+str(dis)+"'"
            cursor.execute(sql)
            results = cursor.fetchall()
            sub,message = creatDic(results)
            dic[sub] = message
            filename = 'forum_out_'
            filename += str(dis)
            filename += '.txt'
            filename = dirname + '\\' + filename
            out = open(filename,'a')
            out.write(sub+'\n')
            out.write(message+'\n')
            allObj.write(sub+'\n'+message+'\n')
            out.close()
    cursor.close()
    con.close()
    allObj.close()
'''	
    cnt = 1 
    for d in dic:
        
        print filename
        out = open(filename,'w')
        brr = dic[d]
        out.write(brr)
    out.close()
'''    

def creatDic(results):
    sub = ''
    message = ''
    for ret in results:
        if ret[2] == 0 :
            sub = ret[7].decode('utf8')
        message = message + getMessage(ret[8].decode('utf8'))
    return sub,message
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
def _delete_dir_and_file(dirpath):
    try:
        if not os.path.isfile(dirpath):
            list = os.listdir(dirpath)
            for dir_or_file in list:mdl_logstore_standard_log
                _delete_dir_and_file(dirpath+'/'+dir_or_file)
            os.rmdir(dirpath)
        else:
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
        
        os.mkdir(dirname)
    except Exception,e:
        print "_init_ failed! err:%s\tdirname:%s"  % (e,dirname)
        sys.exit(1)
    getRecords(dirname)
if __name__ == "__main__":
    dirname = 'D:/forum nlp'
    _init_(dirname)

