# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
import sys
sys.path.append('..')
from utils import strip, args_check

def gen2gram(ws):
    ws = map(strip, ws)
    two_grams = []
    for i in range(len(ws)-1):
        word_pair = "%s-%s" % (ws[i], ws[i+1])
        two_grams.append(word_pair)
    return two_grams

def parse(fpath, tpath):
    lines = []
    with open(fpath) as f:
        for line in f.readlines():
            s, t = line.split('\t')
            ss = gen2gram(s.split())
            ts = gen2gram(t.split())
            line = ' '.join(ss) \
                    + '\t' +\
                    ' '.join(ts)
            lines.append(line)

    with open(tpath, 'w') as f:
        f.write(
            '\n'.join(lines))

if __name__ == '__main__':
    fpath, tpath = args_check(2, "")
    parse(fpath, tpath)
