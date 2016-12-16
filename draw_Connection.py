'''
creat the connection on the map

'''



# coding=utf-8


import os, sys

def getFileLines(filename):
    obj = open(filename, 'r')
    flines = obj.readlines()
    obj.close()
    return flines


def getInputDict(filelines):
    input_dict = {}
    for line in filelines:
        fields = line.strip("\n").split('\t')
        author_id = fields[0]
        tester_id = fields[3]
        code_point = fields[1]
        test_point = fields[2]
        pos = [code_point,test_point]
        input_dict[author_id] = [pos,tester_id]
    return input_dict


def creatConnectionList(input_dict):
    con_set = set()
    connection_list = []
    for stu in input_dict:
        if stu in con_set:
            continue
        pos = input_dict[stu][0]
        next_stu = input_dict[stu][1]
        connection_list.append(pos)
        con_set.add(stu)
        while next_stu not in con_set:
            stu = next_stu
            pos = input_dict[stu][0]
            next_stu = input_dict[stu][1]
            connection_list.append(pos)
            con_set.add(stu)
    return connection_list

def WriteFile(point_dict, filename):
    outObj = open(filename, 'w')
    for t in point_dict:
        record = point_dict[t]
        #        if record[0] == 'None':
        #            continue
        line = "%s\t%s\t%s\t%s" % (t, record[0], record[1], record[2])
        outObj.write(line + '\n')


def getEven(code_point_list, test_point_list):
    retval = 0.0
    cnt = 0
    for val in code_point_list:
        retval = retval + float(val)
        cnt = cnt + 1
    if cnt != 0:
        retval = retval / cnt
    return int(retval)


def deal_None(point_dict, filedir):
    if not os.path.exists(filedir):
        print "Error! FileDir not exists!!!"
        exit(0)
    if not os.path.isdir(filedir):
        print "Error! %s is not a dir!!!" % (filedir)
        exit(0)
    filelist = os.listdir(filedir)
    for file in filelist:
        filename = filedir + '\\' + file
        obj = open(filename, 'r')
        flines = obj.readlines()
        obj.close()
        flen = len(flines)
        for i in range(flen):
            line = flines[i]
            fields = line.strip('\n').split('\t')
            coder = fields[0]
            code_point = fields[1]
            test_point = fields[2]
            tester = fields[3]
            if code_point == 'None':
                code_point = getEven(point_dict[coder][0], point_dict[tester][1])
            else:
                code_point = int(float(code_point))
            if test_point == 'None':
                test_point = getEven(point_dict[coder][0], point_dict[tester][1])
            else:
                test_point = 0 - int(float(test_point))
            fields[1] = code_point
            fields[2] = test_point
            new_line = '%s\t%s\t%s\t%s\n' % (fields[0], fields[1], fields[2], fields[3])
            flines[i] = new_line
        obj = open(filename, 'w')
        obj.writelines(flines)
        obj.close()
    print 'Deal With None Data Done!'

def creatPosMap(filedir):
    if not os.path.exists(filedir):
        print "Error! FileDir not exists!!!"
        exit(0)
    if not os.path.isdir(filedir):
        print "Error! %s is not a dir!!!" % (filedir)
        exit(0)
    filelist = os.listdir(filedir)
    for file in filelist:
        filename = filedir + '\\' + file
        flines = getFileLines(filename)
        input_dict = getInputDict(flines)
        con_list = creatConnectionList(input_dict)
        con_tuple = creatDATA(con_list)
        draw_Mat(con_tuple)
    
def creatDATA(connection_list):
    connect_tuple = ()
    for pos in connection_list:
        x = int(pos[0])
        y = int (pos[1])
        tmp = (x,y)
        connect_tuple = connect_tuple + tmp
    return connect_tuple
def draw_Mat(DATA):
    import matplotlib.pyplot as plt

    # dash_style =
    #     direction, length, (text)rotation, dashrotation, push
    # (The parameters are varied to show their effects,
    # not for visual appeal).
    dash_style = (
        (0, 20, -15, 30, 10),
        (1, 30, 0, 15, 10),
        (0, 40, 15, 15, 10),
        (1, 20, 30, 60, 10),
        )

    fig, ax = plt.subplots()

    (x, y) = zip(*DATA)
    ax.plot(x, y, marker='o')
    for i in range(len(DATA)):
        (x, y) = DATA[i]
    ax.set_xlim((-10.0, 10.0))
    ax.set_ylim((0.0, 10.0))
    plt.show()
    
if __name__ == '__main__':
    datadir = 'D:\Dataprocess\pre_MapDataOp'
    creatPosMap(datadir)
