# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
import sys
sys.path.append('..')
from utils import *
from numpy import *
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
        down = sum([sqrt(sum([dic[w]^2 for w in dic])) \
                    for dic in (sco_dic_q, sco_dic_t)])
        return upper/down

    def get_score(self, ws):
        tf_dic = self.get_tf(ws)
        for k in tf_dic:
            tf_dic[k] *= self.idf(k)
        return tf_dic

    def idf(self, w):
        return log(self.dic[w] / self.num_docs)

    def get_tf(self, ws):
        doc_dic = {}
        num_words = len(ws)
        for w in ws:
            doc_dic[w] = doc_dic.get(w, 0) + 1
        for k in doc_dic:
            doc_dic[k] /= num_words

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
            f.write(
                ' '.join(self.sims))

    def __call__(self):
        self.scan()
        self.tofile()

if __name__ == '__main__':
    args = ArgsAction()
    args.add_action(2, "word_tf_idf", "cmd fph, tph")

    args.start()
