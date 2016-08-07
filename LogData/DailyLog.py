#coding=utf-8
import MySQLdb

con = MySQLdb.connect(host="localhost",user='root',passwd='12345678',db = 'moodle',charset='utf8')
cursor = con.cursor()

sql = "select * from mdl_logstore_standard_log"
cursor.execute(sql)

results = cursor.fetchall()
filename = 'log_sqlOut.txt'
dic  = {}
for ret in results:
	uId = ret[12]
	arr = []
	brr = []
	if dic.has_key(uId) == False:
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
		brr = dic[uId]
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
	dic[uId] = brr
out = open(filename,'w')

for d in dic:
	brr = dic[d]
	for b in brr:
		line = ''
		for a in b:
			line = line + a +' '
		line = line+'\n'
		out.write(line)
con.close()


