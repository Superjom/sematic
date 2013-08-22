#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Aug 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division
import env
from utils import bdb_open, tojson, \
        fromjson, strip, Dic, args_check,\
        get_num_lines

class LabeledDataSet(object):
    def __init__(self):
        self.labeled_data_ph = env.LABELED_DATA_PATH
        self.db = bdb_open(env.DB_PATH)
        self.num_lines = get_num_lines(env.LABELED_DATA_PATH)

    def load_labeled_data(self):
        """
        load labeled data to a list
        """
        self.labeled_records = []
        with open(self.labeled_data_ph) as f:
            for line in f.readlines():
                label, source, url, target  = line.split()
                target = target.strip()
                self.labeled_records.append(
                    [label, source, url, target] ) 

    def iter_labeled_data(self):
        with open(self.labeled_data_ph) as f:
            for line in f.readlines():
                line = line.decode('gbk', 'ignore')
                label, source, url, target  = line.split('\t')
                target = target.strip()
                yield ( {'label':label, 
                            'source':source, 'url':url, 'target':target})


    def todb(self):
        """
        save list to database
        """
        print '.. save labeled data to database'
        for id, data in enumerate(self.iter_labeled_data()):
            print id
            self.db['%s-%d' % (env.KEY_LABELED_DATA, id)] = tojson(data)
        print '.. end database'

    def get(self, id):
        """
        get from database
        """
        key = '%s-%d' % (env.KEY_LABELED_DATA, id)
        return fromjson(self.db[key])

def record2db():
    """
    将记录加入到数据库中
    """
    l = LabeledDataSet()
    l.todb()


def gen_source_title_file(field=None, path=None):
    """
    用于分词
    源title 
    文件每行一个记录
    """
    l = LabeledDataSet()
    sources = []
    for data in l.iter_labeled_data():
        if field is None:
            sources.append(data['source'])
        else:
            sources.append(data[field])

    if path is None:
        path = env.SOURCE_TITLES_PH

    with open(path, 'w') as f:
        c = '\n'.join(sources)
        c = c.encode('gbk', 'ignore')
        f.write(c)


def gen_target_title_file():
    """
    用于分词
    源title 
    文件每行一个记录
    """
    gen_source_title_file('target', env.TARGET_TITLES_PH)

def gen_word_dic():
    """
    在word-wise 的字典
    source 和 target
    """
    def gen_dic(path):
        words = []
        with open(path) as f:
            for line in f.readlines():
                words += map(strip, line.split())
        words = map(strip, words)
        return list(set(words))

    dic = Dic()
    dic.from_list(
        gen_dic(env.SPLITED_SOURCE_TITLES_PH) +
        gen_dic(env.SPLITED_TARGET_TITLES_PH))
    encode = ('gbk', 'utf8')
    dic.tofile(env.DIC_PH, encode=encode)

def gen_word_id_titles():
    """
    生成一个只包含source\ttarget wordid 
    的文件
    """
    dic = Dic()
    dic.fromfile(env.DIC_PH)
    num_rcds = get_num_lines(env.SOURCE_TITLES_PH)
    print 'num of rcds:', num_rcds
    records = []
    with open(env.SPLITED_SOURCE_TITLES_PH) as sf:
        with open(env.SPLITED_TARGET_TITLES_PH) as tf:
            for i in range(num_rcds):
                source = sf.readline().decode('gbk','ignore').encode('utf8')
                target = tf.readline().decode('gbk','ignore').encode('utf8')
                source = source.strip().split()
                target = target.strip().split()
                s_rcds = [dic.get(w) for w in source]
                t_rcds = [dic.get(w) for w in target]
                #print s_rcds, t_rcds
                records.append(
                    ' '.join(map(str, s_rcds)) + '\t' +
                    ' '.join(map(str, t_rcds))
                )
                with open(env.WORD_ID_SOURCE_TARGET_PH, 'w') as f:
                    f.write('\n'.join(records))


if __name__ == "__main__":
    args = args_check(1, "cmd [action]")
    #record2db()
    actions = {
            'record2db' : record2db,
            'gen_target_title_file': gen_target_title_file,
            'gen_source_title_file': gen_source_title_file,
            'gen_word_dic': gen_word_dic,
            'gen_word_id_titles': gen_word_id_titles,
    }
    action = args[0]
    actions[action]()
