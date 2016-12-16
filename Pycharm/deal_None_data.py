# coding=utf-8


import os, sys


def getFileLines(filename):
    obj = open(filename, 'r')
    flines = obj.readlines()
    obj.close()
    return flines


def getFileData(filelines, grade_dict):
    min = 99999
    for line in filelines:
        fields = line.strip("\n").split('\t')
        author_id = fields[0]
        tester_id = fields[3]
        code_point = fields[1]
        test_point = fields[2]
        if author_id not in grade_dict:
            item = []
            if code_point != 'None':
                code_it = [code_point]
            else:
                code_it = []
            if test_point != 'None':
                test_it = [test_point]
            else:
                test_it = []
            item = [code_it, test_it]
        else:
            code_it = grade_dict[author_id][0]
            test_it = grade_dict[author_id][1]
            if code_point != 'None':
                code_it.append(code_point)
            if test_point != 'None':
                test_it.append(test_point)
            item = [code_it, test_it]
        grade_dict[author_id] = item
    return grade_dict


def creatDict(filedir):
    point_dict = {}
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
        point_dict = getFileData(flines, point_dict)
    return point_dict


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
            other_fields = fields[3:]

            new_line = '%s\t%s\t%s' % (fields[0], fields[1], fields[2])
            other_line = ''
            for f in other_fields:
                other_line = other_line + '\t%s' % (f)
            new_line = new_line + other_line + '\n'
            flines[i] = new_line
        obj = open(filename, 'w')
        obj.writelines(flines)
        obj.close()
    print 'Deal With None Data Done!'


if __name__ == '__main__':
    datadir = 'D:\Dataprocess\Home_Data'
    point_dict = creatDict(datadir)
    deal_None(point_dict,datadir)

