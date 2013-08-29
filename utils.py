#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Aug 21, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division
import os
import sys
from math import floor


pjoin = os.path.join

def get_num_lines(path):
    shell = os.popen('cat %s | wc -l' % path).read()
    num = int(shell) + 1
    return num

def sparse_value2list(v, n, _min, _max):
    #print _min, _max, v
    step = (_max-_min) / n
    #print step
    v -= _min
    nn = int(v/step) - 1
    #print nn
    _list = [0 for i in range(n)]
    _list[nn] = 1
    return _list

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        """
        if len(self.memo) > 50000:
            raise Exception, "out of range"
        """
        num_of_iter = args[0]
        if num_of_iter == 0:
            self.memo = {}
        key = str(args)
        if not key in self.memo:
            self.memo[key] = self.f(*args)
        return self.memo[key]
memoized = Memoize

def substCost(x, y):
    if x == y: return 0
    else: return 2

@memoized
def minEditDistR(target, source):
    i = len(target)
    j = len(source)
    if i == 0: return j
    elif j==0: return i

    return min(
            minEditDistR(target[:i-1], source) + 1,
            minEditDistR(target, source[:j-1])+1,
            minEditDistR(target[:i-1], source[:j-1]) + substCost(source[j-1], target[i-1]))


@memoized
def minEditDistRe(num_iter, target, source):
    if num_iter > 5000:
        raise Exception, "out of iter_num"
    i = len(target)
    j = len(source)
    if i == 0: return j
    elif j==0: return i

    return min(
            minEditDistRe(num_iter+1, target[:i-1], source) + 1,
            minEditDistRe(num_iter+1, target, source[:j-1])+1,
            minEditDistRe(num_iter+1, target[:i-1], source[:j-1]) + substCost(source[j-1], target[i-1]))

#import bsddb
def bdb_open(path):
    db = bsddb.btopen(path, 'c')
    return db

import json
tojson = json.dumps
fromjson = json.loads


def args_check(num_args, usage_intro):
    argv = sys.argv
    if len(argv[1:]) != num_args:
        print "=" * 50
        print "     usage: %s" % usage_intro
        print "=" * 50
        sys.exit(-1)
    return argv[1:]

class ArgsAction(object):
    def __init__(self):
        self.actiion = {}

    def add_action(self, num_args, _type, action, info="", is_class=True):
        self.action[_type] = (num_args, action, info, is_class)

    def start(self):
        _type = sys.argv[0]
        if _type not in self.action:
            print "Error: Unknown action"
        else:
            num_args, action, is_class, info = self.action[_type]
            args = args_check(num_args+1, info)
            if is_class:
                c = action(*args[1:])
                c()
            else:
                action(*args[1:])


class Dic(object):
    def from_list(self, _list):
        self.dic = list(set(_list))

    def get(self, word):
        return self.dic[word]

    def tofile(self, path, encode=None):
        """
        encode = (fencode, tencode)
        """
        with open(path, 'w') as f:
            c = ' '.join(self.dic)
            if encode is not None:
                c = c.decode(encode[0], 'ignore').encode(encode[1], 'ignore')
            f.write(c)

    def fromfile(self, path):
        self.dic = {}
        with open(path) as f:
            c = f.read()
            _list = c.split()
            for i, w in enumerate(_list):
                self.dic[w] = i

strip = lambda x: x.strip()



if __name__ == "__main__":
    print sparse_value2list(2.5, 6, 0, 6)


