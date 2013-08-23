# -*- coding: utf-8 -*-
'''
Created on Jul 23, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
import sys
sys.path.append('..')
from utils import Dic, strip, args_check

class Replacer(object):
    def __init__(self, dic_path, fpath, tpath):
        self.dic_path = dic_path
        self.fpath = fpath
        self.tpath = tpath
        self._init()

    def __call__(self):
        self.trans()
        self.tofile()

    def _init(self):
        # load dic
        self.dic = Dic()
        self.dic.fromfile(self.dic_path)

    def trans(self):
        self.lines = []
        with open(self.fpath) as f:
            for line in f.readlines():
                s, t = map(strip, line.split('\t'))
                ss = [self.dic.dic.get(w, '') for w in s.split()]
                ts = [self.dic.dic.get(w, '') for w in t.split()]
                c = ' '.join(map(str, ss)) \
                    + '\t' +\
                    ' '.join(map(str, ts))
                self.lines.append(c)

    def tofile(self):
        with open(self.tpath, 'w') as f:
            content = '\n'.join(self.lines)
            f.write(content)

if __name__ == "__main__":
    dic_path, fpath, tpath = args_check(3, "cmd [dic_path], [fpath], [tpath]")
    t = Replacer(dic_path, fpath, tpath)
    t()
