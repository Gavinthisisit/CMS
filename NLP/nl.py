#coding=utf-8

import sys,os
import jieba
import jieba.posseg as pseg
import jieba.analyse
#import NLP_discussion

reload(sys)
sys.setdefaultencoding( "utf-8" )




#斯坦福
'''
from nltk.tokenize.stanford_segmenter import StanfordSegmenter

segmenter = StanfordSegmenter(path_to_jar="stanford-segmenter-3.4.1.jar",
                              path_to_sihan_corpora_dict="./data",
                              path_to_model="./data/pku.gz",
                              path_to_dict="./data/dict-chris6.ser.gz")


sentence = u"这是斯坦福中文分词器测试"

outfile = open('outfile', 'w')

result = segmenter.segment(sentence)

outfile.write(result.encode('UTF-8'))

outfile.close()

'''
'''
seg_list = jieba.cut('我来到北京航空航天大学',cut_all=True)
print "Full Mode:","/".join(seg_list) #全模式

seg_list = jieba.cut('我来到北京航空航天大学',cut_all=False)
print "Default Mode:","/".join(seg_list)#精确模式

seg_list = jieba.cut('他来到了网易杭研大厦')#默认是精确模式
print ",".join(seg_list)

#seg_list = jieba.cut_for_search('小明毕业于中国开科学院计算所，后来在日本京都大学深造')#搜索引擎模式
#print ",".join(seg_list)
'''

def _get_emotion_dict(filename):
    em_dict = {}
    fd = open(filename,'r')
    for line in fd.readlines():
        fields = line.strip('\n').split('\t')
        key = fields[0].decode('utf8')
        if key not in em_dict:
            em_dict[key] = 1
    return em_dict
    


def _get_wordsflag_dic():
    words_flag_dic = {}
    dic_name = 'words_dic.txt'
    try:
        obj = open(dic_name,'r')
        for line in obj.readlines():
            fields = line.strip('\n').split()
            if fields[0] not in words_flag_dic:
                words_flag_dic[fields[0]] = fields[1].decode('utf8')
#                print '%s\t%s' % (fields[0],fields[1].decode('utf8').encode('gbk'))
        return words_flag_dic
    except Exception,e:
        print '_get_wordsflag_dic failed!,errmsg=%s' % (e)
        sys.exit(0)

def _get_top_words(sentence,topK):
    top_out_name = 'top_words.txt'
    outObj = open(top_out_name,'w')
    topWords = jieba.analyse.extract_tags(sentence,topK)
    for word in topWords:
        outline = word+'\n'
        outObj.write(outline)
    outObj.close()

    
def _get_content(filepath):
    obj = open(filepath,'r')
    sentence = ''
    for line in obj.readlines():
        fields = line.strip('\n').split('\t')
        if fields[0] != '':
            sentence += fields[0].decode('utf8')
    return sentence
    
def _flag_filter(flag):
    if flag == 'x' or flag == 'm' or flag == 'uj' or flag == 'd' or flag == 'f' or flag == 'r':
        return True
    else:
        return False
def _chs_content_filter(word):
    if word == '是' or word == '要' or word == '时' or word == '有' or word == '来':
        return False
    else:
        return True
def _segment_sentence(sentence,filename,positive_dict,negative_dict,outfile):
    if sentence == '':
        print 'There are nothing to deal with.'
        sys.exit(0)
    filter_list_flag = ['x','m','uj','f','r','d','a','c','p','ul','t','ad']
    flag_filter = set(filter_list_flag)
    
    
    eng_content_filter_list = ['nbsp','the','new','void','method','or','to','of','gc','orz']
    eng_content_filter = set(eng_content_filter_list)
    words_flag_dic = _get_wordsflag_dic()
    words = pseg.cut(sentence)

    outObj = open(outfile,'a')
#    for t in title_words:
#        if t.flag in words_flag_dic:
#            if t.flag not in flag_filter:
#                if t.flag == 'eng':
#                    t.word = t.word.lower()
#                if t.word not in eng_content_filter:
#                    outline = '%s\t%s\t%s\t%s' % (t.word,t.flag,words_flag_dic[t.flag],1)
#            
#                    topObj.write(outline+'\n')
#                    outObj.write(outline+'\n')
#        else:
#            print 'Waring: Flag missed!!\t\'%s\'\t\'%s\'' % (t.word,t.flag)
    for w in words:
        if w.word in positive_dict:
            line = 'Positive emotion detected! word:%s file:%s' % (w.word,filename);
            outObj.write(line+'\n')
        elif w.word in negative_dict:
            line = 'Negative emotion detected! word:%s file:%s' % (w.word,filename);
            outObj.write(line+'\n')
    outObj.close()
#    _filter_sort(words,topfile,outfilename)
'''   
    for w in words:
        if w.flag in words_flag_dic:
            if _flag_filter(w.flag):
                continue;
            outline = '%s\t%s\t%s'  % (w.word,w.flag,words_flag_dic[w.flag])
            outObj.write(outline+'\n')
        else:
            print 'Waring: Flag missed!!\t\'%s\'\t\'%s\'' % (w.word,w.flag)
            waringObj.write(w.word+'\t'+w.flag+'\n')
'''
#    waringObj.close()
    
    

def _filter_sort(words,topfile,outFile):
    filter_list_flag = ['x','m','uj','f','r','d','a','c','p','ul','t','ad','u','nr']
    flag_filter = set(filter_list_flag)
    eng_content_filter_list = ['nbsp','the','new','void','method','or','to','of','gc','orz','on']
    eng_content_filter = set(eng_content_filter_list)
    word_dic = {}
    flag_dic = {}
    outObj = open(outFile,'a')
    words_flag_dic = _get_wordsflag_dic()
    try:
        for w in words:
            if w.flag not in flag_filter:                #根据我们的过滤列表过滤掉一些无意义的词汇
                if w.flag == 'eng':
                    w.word = w.word.lower()
                if w.word not in eng_content_filter and _chs_content_filter(w.word):
                    if w.word in word_dic:
                        word_dic[w.word] += 1           #生成单词出现频数的字典，key词，value是频数，以此来排序
                    else:
                        word_dic[w.word] = 1
                        flag_dic[w.word] = w.flag           #附加单词的词性
            if w.flag in words_flag_dic:            #将分词结果存入文件，以便后面观察效果
                if _flag_filter(w.flag):
                    continue;
                outline = '%s\t%s\t%s'  % (w.word,w.flag,words_flag_dic[w.flag])
                outObj.write(outline+'\n')
            else:
                print 'Waring: Flag missed!!\t\'%s\'\t\'%s\'' % (w.word,w.flag)

        sort_dic = sorted(word_dic.iteritems(), key=lambda asd:asd[1], reverse = True )    #dict排序
        topObj = open(topfile,'a')
        for list in sort_dic:
            outline = '%s\t%s\t%s\t%s' % (list[0],flag_dic[list[0]],words_flag_dic[flag_dic[list[0]]],list[1])
            topObj.write(outline+'\n')
        topObj.close()
    except Exception,e:
        print 'There are some error during generate sorted_dic,err:%s' % (e)
if __name__ == '__main__':
    t = '12'
    emotion_out_file = 'G:\CMS\NLP\emotion_out_%s.txt' % (t)
    positive_dict = _get_emotion_dict('G:\\CMS\\NLP\\ntusd-positive.txt')
    negative_dict = _get_emotion_dict('G:/CMS/NLP/ntusd-negative.txt')
    dirname = 'D:\Dataprocess\Complain\Complain\\%s' % (t)
    filelist = os.listdir(dirname)
    sentence = ''
    for file in filelist:
        filename = dirname + '\\' + file
        print filename
        sentence = _get_content(filename)
        _segment_sentence(sentence,filename,positive_dict,negative_dict,emotion_out_file)
#    _get_top_words(sentence,20)

