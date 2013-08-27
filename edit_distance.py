#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Aug 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division
from utils import *
import sys

class EditDistance(object):
    def __init__(self, _type, fpath, tpath):
        self.fpath = fpath
        self.tpath = tpath
        self._type = _type

    def cal_dis(self):
        self.dis = []
        num_lines = get_num_lines(self.fpath)
        with open(self.fpath) as f:
            for id, line in enumerate(f.readlines()):
                if id % 150 == 0: print id/num_lines
                source, target = line.split('\t')
                if self._type == 'word':
                    source = source.split()
                    target = target.split()
                    source = map(int, source)
                    target = map(int, target)
                elif self._type == 'char':
                    source = source.strip()
                    target = target.strip()
                else:
                    print "error, type should be word/char"
                    sys.exit(-1)
                #print source, target
                try:
                    dis = minEditDistRe(0, source, target)
                except Exception, e:
                    print 'error: %d %s' % (id, e)
                    dis = 1000
                self.dis.append(dis)

    def tofile(self):
        c = '\n'.join(map(str, self.dis))
        with open(self.tpath, 'w') as f:
            f.write(c)

    def __call__(self):
        self.cal_dis()
        self.tofile()


if __name__ == "__main__":
    _type, fpath, tpath = args_check(3, "cmd [type] [fpath] [tpath]")
    w = EditDistance(_type, fpath, tpath)
    w()
