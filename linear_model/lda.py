# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
import sys
sys.path.append('..')
from utils import *

def trans_lda_format(fpath, tpath):
    lines = []
    with open(fpath) as f:
        for line in f.readlines():
            s, t = map(strip, line.split('\t'))
            lines += [s, t]
    with open(tpath) as f:
        f.write(
           '\n'.join(lines) 
        )


if __name__ == '__main__':
    _type = sys.argv[1]
    if _type == 'trans_format':
        _type, fpath, tpath = args_check(3, "cmd fpath, tpath")
        trans_lda_format(fpath, tpath)

