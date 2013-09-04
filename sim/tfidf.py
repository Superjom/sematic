# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division
import sys
sys.path.append('..')
from utils import *
from math import *

class TfIdf(object):
    '''
    自动建立dic
    '''
    def __init__(self, ph):
        self.ph = ph
        self.dic = {}
        # init
        self.gen_idf()

    def sim(self, qws, tws):
        sco_dic_q, sco_dic_t = [self.get_score(ws) \
                for ws in (qws, tws)]
        upper = sum([sco_dic_q[w] * sco_dic_t.get(w, 0.0) \
                    for w in sco_dic_q])
        down = sqrt(sum([sco_dic_q[w]**2 for w in sco_dic_q])) *\
                sqrt(sum([sco_dic_t[w]**2 for w in sco_dic_t])) 
        #print upper, down, upper/down
        return upper/down

    def get_score(self, ws):
        tf_dic = self.get_tf(ws)
        for k in tf_dic:
            tf_dic[k] *= self.idf(k)
        #print tf_dic
        return tf_dic

    def idf(self, w):
        return log( self.num_docs/self.dic[w] )

    def get_tf(self, ws):
        doc_dic = {}
        #num_words = len(ws)
        for w in ws:
            doc_dic[w] = doc_dic.get(w, 0) + 1
        """
        for k in doc_dic:
            doc_dic[k] /= num_words
        """
        return doc_dic

    def gen_idf(self):
        """
        create a dic
        """
        self.num_docs = 0
        with open(self.ph) as f:
            for line in f.readlines():
                self.num_docs += 1
                query, title = line.split('\t')
                qws = map(strip, query.split())
                tws = map(strip, title.split())
                for w in set(qws + tws):
                    self.dic[w] = self.dic.get(w, 0) + 1


class WordTfIdf(TfIdf):
    def __init__(self, ph, tph):
        TfIdf.__init__(self, ph)
        self.ph, self.tph = ph, tph

    def scan(self):
        self.sims = []
        with open(self.ph) as f:
            for line in f.readlines():
                query, title = line.split('\t')
                qws = map(strip, query.split())
                tws = map(strip, title.split())
                sim = self.sim(qws, tws)
                self.sims.append(sim)

    def tofile(self):
        with open(self.tph, 'w') as f:
            print "num of lines: ", len(self.sims)
            f.write(
                '\n'.join(map(str, self.sims)))

    def __call__(self):
        self.scan()
        self.tofile()

def trans_format(ph, label_ph, train_ph, test_ph):
    total_num_lines = get_num_lines(ph)
    print total_num_lines
    #assert total_num_lines == sum([label_ph, train_ph, test_ph])
    with open(ph) as f:
        for path in (label_ph, train_ph, test_ph):
            sims = []
            num_lines = get_num_lines(path)
            print "num of lines of ", num_lines
            for i in range(num_lines):
                line = f.readline().strip()
                #print line
                sim = float(line)
                sims.append(sim)
            toph = path + ".tfidf"
            with open(toph, 'w') as tf:
                tf.write(
                    '\n'.join( map(str, sims)))



if __name__ == '__main__':
    args = ArgsAction()
    args.add_action(2, "word_tf_idf", WordTfIdf, "cmd fph, tph")
    args.add_action(4, "trans_format", trans_format, "cmd ph, label_ph, train_ph, test_ph", is_class=False)

    args.start()
