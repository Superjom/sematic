# -*- coding: utf-8 -*-
'''
Created on Jul 22, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division

from utils import args_check, Dic, strip

def gen_dic(fpath, tpath):
    print '.. dic: fpath>tpath', fpath, tpath
    with open(fpath) as f:
        c = f.read()
        ws = c.split()
        ws = map(strip, ws)
        dic = Dic()
        dic.from_list(ws)
        dic.tofile(tpath)

def gen_2gram_dic(fpath, tpath):
    print '.. dic: fpath>tpath', fpath, tpath
    with open(fpath) as f:
        c = f.read()
        ws = c.split()
        ws = map(strip, ws)
        two_grams = []
        for i in range(len(ws)-1):
            if i % 500 == 0:
                print 'status:', i / len(ws)
            word_pair = "%s-%s" % (ws[i], ws[i+1])
            two_grams.append(word_pair)

        dic = Dic()
        dic.from_list(two_grams)
        dic.tofile(tpath)

if __name__ == '__main__':
    ngram, fpath, tpath = args_check(3, "cmd [ngram] [fpath], [tpath]")
    if int(ngram) == 1:
        gen_dic(fpath, tpath)
    else:
        gen_2gram_dic(fpath, tpath)
