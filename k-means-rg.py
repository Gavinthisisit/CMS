#coding=utf-8
from numpy import *

def loadDataSet(fileName,prefilename):
    data_dict = {}
    fr = open(prefileName)                    ##load homework data before this time
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = []
        for t in curLine[1:]:
            x = float(t)
            fltLine.append(x)
        data_dict[curLine[0]] = fltLine
    fr = open(fileName)                       ##load current data
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = []
        for t in curLine[1:]:
            x = float(t)
            fltLine.append(x)
        if curLine[0] not in data_dict:
            data_dict[curLine[0]] = fltLine
        else:
            for f in fltLine:
                data_dict[curLine[0]].append(f)
    return data_dict
    
#计算两个向量的距离，用的是欧几里得距离
def distEclud(vecA, vecB):
    sum = 0.0
    for i in range(len(vecA)):
        sum += power(vecA[i] - vecB[i],2)
    return sqrt(sum)

def cal_dis(data_dict):
    print type(data_dict)
    test_to_dict = {}
    test_from_dict = {}
    data_size = len(data_dict)
    while len(test_to_dict) != data_size:
        for uid in data_dict:
            if uid not in test_to_dict:
                dis_dict = {}
                for calid in data_dict:
                    if calid not in test_from_dict:
                        dis = distEclud(data_dict[uid],data_dict[calid])
                        dis_dict[calid] = dis
                sort_dict = sorted(dis_dict.iteritems(),key=lambda asd:asd[1],reverse=True)
                for id in sort_dict:
                    if (uid not in test_from_dict) or (id != test_from_dict[uid]):
                        test_to_dict[uid] = id
                        test_from_dict[id] = uid
                        break
                    else:
                        continue
    return test_to_dict,test_from_dict



#随机生成初始的质心（ng的课说的初始方式是随机选K个点）    
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(array(dataSet)[:,j]) - minJ)
        centroids[:,j] = minJ + rangeJ * random.rand(k,1)
    return centroids
    
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))#create mat to assign data points 
                                      #to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: 
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print centroids
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean 
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
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)  
    plt.show()

def PrintToFile(data,file):
    out = open(file,'w')
    for id in data:
        line = '%s---%s\n' % (id,data[id])
        out.write(line)
    out.close()
def PrintPreFile(predata,prefile):
    out = open(prefile,'w')
    for id in predata:
        datalist = predata[id]
        line = '%s' % (id)
        for d in datalist[:-3]:
            line = line + '\t%s' % (d)
        out.write(line+'\n')
    out.close()
def main():
    datadir = 'D:\Dataprocess\Home_Data\data'
    prefileName = 'D:\Dataprocess\Home_Data\pre_data_file.txt'
    data_list = os.listdir(datadir)
    for file in data_list:
        fileName = datadir + '\\' + file
        data_dict = loadDataSet(fileName,prefileName)
        test_to,test_from = cal_dis(data_dict)
        fileNum = file.split('_')
        Tofile = 'D:\Dataprocess\Home_Data\test_to\test_to_%s.txt' % (fileNum[0])
        FromFile = 'D:\Dataprocess\Home_Data\test_to\test_from_%s.txt' % (fileNum[0])
        PrintToFile(test_to,Tofile)
        PrintToFile(test_from,FromFile)
        printPreFile(data_dict,prefileName)
    
    
if __name__ == '__main__':
    main()