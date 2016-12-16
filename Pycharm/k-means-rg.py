# coding=utf-8
from numpy import *
import os,sys


def loadDataSet(fileName, prefileName):
    full_data_dict = {}
    current_data_dict = {}
    fr = open(prefileName,'r')  ##load current data
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = []
        id = curLine[0]
        for t in curLine[1:]:
            x = float(t)
            fltLine.append(x)
        full_data_dict[id] = fltLine
    fr.close()

    fr = open(fileName,'r')  ##load homework data before this time
    for line in fr.readlines()[1:]:
        curLine = line.strip().split('\t')
        fltLine = []
        id = curLine[0]
        for t in curLine[1:]:
            x = float(t)
            fltLine.append(x)
        if id not in full_data_dict:
            current_data_dict[id] = fltLine
            full_data_dict[id] = fltLine[:-3]
        else:
            current_data_dict[id] = full_data_dict[id] + fltLine
            full_data_dict[id] = full_data_dict[id] + fltLine[:-3]
    fr.close()

    return current_data_dict, full_data_dict

def loadConnection(preFileName):
    print 'load %s start...' % (preFileName)
    pre_dict = {}
    obj = open(preFileName,'r')
    flines = obj.readlines()
    for line in flines:
        fields = line.strip('\n').split('\t')
        uid = fields[0]
        pre_list = []
        if  len(fields) > 1:
            pre_test = fields[1].split('$$')
            for id in pre_test:
                pre_list.append(id)
        pre_dict[uid] = pre_list
    obj.close()
    print 'load %s end...' % (preFileName)
    return pre_dict

# 计算两个向量的距离，用的是欧几里得距离
def distEclud(vecA, vecB):
    sum = 0.0
    lenA = len(vecA)
    lenB = len(vecB)
    if lenA >= lenB:
        for i in range(len(vecB)):
            sum += power(vecA[i] - vecB[i], 2)
        while i < lenA-1:
            sum += 2
            i += 1
    else:
        for i in range(len(vecA)):
            sum += power(vecA[i] - vecB[i], 2)
        while i < lenB-1:
            sum += 2
            i += 1
    return sqrt(sum)

def adapt_Distribute(test_to_dict,test_from_dict,uid,calid,data_dict,pre_connection_dict):
    flag = True
    forbidden_id = ''
    while flag:
        dis_dict = {}
        for id in data_dict:
            if id == uid:
                continue
            try:
                dis = distEclud(data_dict[uid],data_dict[id])
            except Exception,e:
                print data_dict[uid], data_dict[id], uid, id
                sys.exit(1)
            dis_dict[id] = dis
        sort_dict = sorted(dis_dict.iteritems(), key=lambda asd: asd[1], reverse=False)
        for item in sort_dict:
            id = item[0]
            entropy = item[1]
            reserve_id = ''
            if  forbidden_id != id and test_to_dict[id] != uid and uid not in pre_connection_dict:
                reserve_id = test_from_dict[id][0]
                test_to_dict[uid] = [id, entropy]
                test_from_dict[id] = [uid, entropy]
                pre_connection_dict[uid] = [id]
                break
            elif forbidden_id != id and test_to_dict[id] != uid and id not in pre_connection_dict[uid]:
                reserve_id = test_from_dict[id][0]
                test_to_dict[uid] = [id, entropy]
                test_from_dict[id] = [uid, entropy]
                pre_connection_dict[uid].append(id)
                break
        uid = reserve_id
        forbidden_id = id
        entropy = distEclud(data_dict[uid],data_dict[calid])
        if uid not in pre_connection_dict:
            test_to_dict[uid] = [calid,entropy]
            test_from_dict[calid] = [uid, entropy]
            pre_connection_dict[uid] = [calid]
            flag = False
        elif  calid not in pre_connection_dict[uid]:
            test_to_dict[uid] = [calid, entropy]
            test_from_dict[calid] = [uid, entropy]
            pre_connection_dict[uid].append(calid)
            flag =False
    return test_to_dict,test_from_dict,pre_connection_dict

def distribute(data_dict,pre_connection_dict):
    print 'cal start...'
    test_to_dict = {}
    test_from_dict = {}
    data_size = len(data_dict)
    cnt = 0
    while len(test_to_dict) != data_size:
        print len(test_to_dict),data_size
        for uid in data_dict:
            if uid not in test_to_dict:
                dis_dict = {}
                for calid in data_dict:
                    if calid == uid:
                        continue
                    if calid not in test_from_dict:
                        try:
                            dis = distEclud(data_dict[uid], data_dict[calid])
                            print uid,calid
                        except Exception,e:
                            print data_dict[uid], data_dict[calid], uid, calid
                            sys.exit(1)
                        dis_dict[calid] = dis
                sort_dict = sorted(dis_dict.iteritems(), key=lambda asd: asd[1], reverse=False)
                flag = False
                for item in sort_dict:
                    id = item[0]
                    entropy = item[1]
                    if  uid not in pre_connection_dict:
                        test_to_dict[uid] = [id,entropy]
                        test_from_dict[id] = [uid,entropy]
                        pre_connection_dict[uid] = [id]
                        flag = True
                        break
                    elif id not in pre_connection_dict[uid]:
                        test_to_dict[uid] = [id, entropy]
                        test_from_dict[id] = [uid, entropy]
                        pre_connection_dict[uid].append(id)
                        flag = True
                        break
                if flag != True:
                    test_to_dict,test_from_dict,pre_connection_dict = adapt_Distribute(test_to_dict,test_from_dict,uid,id,data_dict,pre_connection_dict)
    print 'cal end...'
    return test_to_dict, test_from_dict,pre_connection_dict


# 随机生成初始的质心（ng的课说的初始方式是随机选K个点）
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(array(dataSet)[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))  # create mat to assign data points
    # to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):  # for each data point assign it to the closest centroid
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI;
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2
        print centroids
        for cent in range(k):  # recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]  # get all the point in this cluster
            centroids[cent, :] = mean(ptsInClust, axis=0)  # assign centroid to mean
    return centroids, clusterAssment


def show(dataSet, k, centroids, clusterAssment):
    from matplotlib import pyplot as plt
    numSamples, dim = dataSet.shape
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    for i in xrange(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)
    plt.show()


def PrintToFile(data, file):
    out = open(file, 'w')
    for id in data:
        line = '%s---%s\n' % (id, data[id])
        out.write(line)
    out.close()


def PrintPreFile(predata, prefile):
    out = open(prefile, 'w')
    for id in predata:
        datalist = predata[id]
        line = '%s' % (id)
        for d in datalist:
            line = line + '\t%s' % (d)
        out.write(line + '\n')
    out.close()

def PrintToPreConFile(pre_dict,pre_file):
    outObj = open(pre_file,'w')
    for id in pre_dict:
        pre_con = pre_dict[id]
        line = '%s\t' % (id)
        for pre_id in pre_con:
            line += '%s$$' % (pre_id)
        line = line.strip('$$')
        outObj.write(line+'\n')
    outObj.close()

def PrintToConnectionMapFile(dataFile, test, pre_MapFile):
    obj = open(dataFile,'r')
    data_dict = {}
    for line in obj.readlines()[1:]:
        fields = line.strip('\n').split('\t')
        id = fields[0]
        code_point = float(fields[1])
        test_point = float(fields[2])
        upload_level = float(fields[3])
        action_count = float(fields[4])
        time_count = float(fields[5])
        data_dict[id] = [code_point,test_point]
    obj.close()
    outObj = open(pre_MapFile,'w')
    for id in test:
        line = '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (id,data_dict[id][0],data_dict[id][1],upload_level,action_count,time_count,test[id][0])
        outObj.write(line+'\n')
    outObj.close()

def main():
    datadir = 'D:\Dataprocess\Home_Data\data'
    prefileName = 'D:\Dataprocess\Home_Data\pre_data_file.txt'
    preConnectionfile = 'D:\Dataprocess\Home_Data\pre_connection_file.txt'
    data_list = os.listdir(datadir)
    for file in data_list:
        fileName = datadir + '\\' + file
        print '%s start processing' % (fileName)
        current_data_dict,full_data_dict = loadDataSet(fileName, prefileName)
        pre_connection_dict = loadConnection(preConnectionfile)
        test_to, test_from, pre_connection_dict= distribute(current_data_dict,pre_connection_dict)
        fileNum = file.split('_')
        Tofile = 'D:\Dataprocess\Home_Data\\test_to\\test_to_%s.txt' % (fileNum[0])
        FromFile = 'D:\Dataprocess\Home_Data\\test_from\\test_from_%s.txt' % (fileNum[0])
        PrintToFile(test_to, Tofile)
        PrintToPreConFile(pre_connection_dict,preConnectionfile)
        pre_MapFile = 'D:\Dataprocess\Home_Data\\pre_map\\pre_map_%s.txt' % (fileNum[0])
        PrintToConnectionMapFile(fileName,test_to,pre_MapFile)
        PrintToFile(test_from, FromFile)
        PrintPreFile(full_data_dict, prefileName)
        print '%s end processing' % (fileName)


if __name__ == '__main__':
    main()