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


class SubSeq(object):
    '''
    检测query 是否是 title 的子句
    简单的基于二元词的匹配
    '''
    def __init__(self, ph, tph):
        self.ph = ph
        self.tph = tph

    def __call__(self):
        self.scan()
        self.tofile()

    def scan(self):
        self.sims = []
        with open(self.ph) as f:
            for line in f.readlines():
                query, title = line.split('\t')
                sim = self.sim(map(strip, query.split()), map(strip, title.split()))
                self.sims.append(sim)

    def tofile(self):
        with open(self.tph) as f:
            f.write('\t'.join(self.sims))

    def sim(self, ws1, ws2):
        query_set = set(ws1)
        title_set = set(ws2)
        query_and_title = query_set and title_set
        return len(query_and_title) / (query_set + title_set)


if __name__ == '__main__':
    args = ArgsAction()
    args.add_action(2, "sumseq", "cmd fph, tph")
    args.start()
