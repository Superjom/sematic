#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Aug 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division
import env
from utils import bdb_open, tojson, fromjson, minEditDistR, args_check
from dataset import LabeledDataSet

class ChaEditDistance(object):
    def __init__(self):
        self.lab_dataset = LabeledDataSet()

    def __call__(self):
        self.cal_dis()
        self.tofile()

    def cal_dis(self):
        print '.. cal_dis'
        self.dis = []
        for id in range(self.lab_dataset.num_lines):
            print id
            rcd = self.lab_dataset.get(id)
            try:
                dis = minEditDistR(rcd['source'], rcd['target'])
            except Exception, e:
                print 'error: %d %s' % (id, e)
                dis = 1000
            self.dis.append(dis)

    def tofile(self):
        c = '\n'.join(map(str, self.dis))
        with open(env.CHA_EDIT_DIS_PH, 'w') as f:
            f.write(c)

class WordEditDistance(object):
    def __init__(self):
        self.path = env.WORD_ID_SOURCE_TARGET_PH

    def cal_dis(self):
        self.dis = []
        with open(self.path) as f:
            for id, line in enumerate(f.readlines()):
                print id
                source, target = line.split('\t')
                source = source.split()
                target = target.split()
                source = map(int, source)
                target = map(int, target)
                print source, target
                try:
                    dis = minEditDistR(source, target)
                except Exception, e:
                    print 'error: %d %s' % (id, e)
                    dis = 1000
                self.dis.append(dis)

    def tofile(self):
        c = '\n'.join(map(str, self.dis))
        with open(env.WORDID_EDIT_DIS_PH, 'w') as f:
            f.write(c)

    def __call__(self):
        self.cal_dis()
        self.tofile()


if __name__ == "__main__":
    args = args_check(1, "cmd [type]")
    _type = args[0]
    types = {
        'c': ChaEditDistance(),
        'w': WordEditDistance(),
    }
    t = types[_type]
    print t
    t()

