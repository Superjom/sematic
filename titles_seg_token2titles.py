# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from utils import *

def get_token(word):
    ws = word.split('/')
    if len(ws) == 2:
        return ws[1]
    else:
        return ''


def one_gram(fpath, tpath):
    lines = []
    with open(fpath) as f:
        for line in f.readlines():
            s, t = line.split('\t')
            ss = map(strip, s.split())
            ts = map(strip, t.split())
            s_tokens = [get_token(w) for w in ss]
            t_tokens = [get_token(w) for w in ts]
            lines.append(
                ' '.join(s_tokens) + '\t' +\
                ' '.join(t_tokens)
                )
    with open(tpath, 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    fpath, tpath = args_check(2, "cmd [fpath] [tpath]")
    one_gram(fpath, tpath)
