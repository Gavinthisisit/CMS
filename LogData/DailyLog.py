#coding=utf-8
import MySQLdb

def getDBConnect(username,passwd,database):
    
    con = MySQLdb.connect(host="localhost",user=username,passwd=passwd,db = database,charset='utf8')
    cursor = con.cursor()
    return cursor,con
    
def getResults(cursor, sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
    

def getLogData(results):
    log_dict  = {}
    for ret in results:
        uId = ret[12]
        arr = []
        brr = []
        if log_dict.has_key(uId) == False:
            id = ret[0]
            str_id = str(id)
            arr.append(str_id)
            event = ret[1]
            event.decode()
            str_event = str(event)
            arr.append(str_event)
            time = ret[17]
            str_time = str(time)
            arr.append(str_time)
            brr.append(arr)
        else:
            brr = log_dict[uId]
            id = ret[0]
            str_id = str(id)
            arr.append(str_id)
            event = ret[1]
            event.decode()
            str_event = str(event)
            arr.append(str_event)
            time = ret[17]
            str_time = str(time)
            arr.append(str_time)
            brr.append(arr)
        log_dict[uId] = brr
    return log_dict
    
def Print(outname,log_dict):
    out = open(outname,'w')
    for d in log_dict:
        brr = log_dict[d]
        out.write(str(d)+'\n')
        for b in brr:
            line = ''
            for a in b:
                line = line + a +' '
            line = line+'\n'
            out.write(line)
    out.close()
 
if __name__ == '__main__':
    dir = "D:/Dataprocess/LogData/"
    cursor,con = getDBConnect('root','','course')
    sql = 'select * from  `mdl_workshop`  where course=7;'
    results = getResults(cursor,sql)
    workshop_dict = {}
    for ret in results:
        workshop_id = ret[0]
        starttime = ret[23]
        endtime = ret[24]
        workshop_dict[workshop_id] = [starttime,endtime]
        sql = "select * from `mdl_logstore_standard_log` where timecreated>%s and timecreated<%s;" % (starttime,endtime)
        results = getResults(cursor,sql)
        log_dict = getLogData(results)
        filename = 'log_sqlOut_'+str(workshop_id)+'.txt'
        Print(dir+filename,log_dict)
    con.close()

