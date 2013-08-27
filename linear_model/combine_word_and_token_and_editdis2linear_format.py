# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from trans_linear_model_format import LinearFormater, get_num_words
import sys
sys.path.append('..')

from utils import *

def wid2list(path):
    res = []
    with open(path) as f:
        for line in f.readlines():
            ls = map(strip, line.split())
            ls = map(int, ls)
            res.append(ls)
    return res

class CombinedModel(LinearFormater):
    def __init__(self):
        LinearFormater.__init__(self)

    def label_from_file(self, path):
        with open(path) as f:
            ws = f.read().split()
            ws = map(strip, ws)
            ws = map(int, ws)
            self.set_labels(ws)
    
    def label_to_test(self, path):
        num_lines = get_num_lines(path)
        print 'get num_lines:', num_lines
        labels = [1 for i in range(num_lines)]
        self.set_labels(labels)

    def add_data_from_file(self, path, _max):
        data = wid2list(path)
        self.add_lst(data, _max)

    def add_vector_from_file(self, path):
        with open(path) as f:
            c = f.read()
            ws = c.split()
            ws = map(strip, ws)
            ws = map(int, ws)
            self.add_vector(ws)

if __name__ == '__main__':
    args = sys.argv[1:]
    _type = args[0]

    c = CombinedModel()

    if _type == "train":
        _type, tpath, label_ph, wid1_dic, wid1, wid2_dic, wid2 , token1_dic, token1, token2_dic, token2, editw = \
            args_check(12, "cmd tpath, label_ph, wid1, wid2, token1, token2, editw")
        c.label_from_file(label_ph)
    else:
        _type, tpath, wid1_dic, wid1, wid2_dic, wid2 , token1_dic, token1, token2_dic, token2, editw = \
            args_check(11, "cmd tpath, label_ph, wid1, wid2, token1, token2, editw")
        c.label_to_test(wid1)

    #for dic_ph, ph in [(wid1_dic, wid1), (wid2_dic, wid2), (token1_dic, token1), (token2_dic, token2)]:
    for dic_ph, ph in [ (wid2_dic, wid2),  (token2_dic, token2)]:
        _max = get_num_words(dic_ph)
        c.add_data_from_file(ph, _max)
    #for ph in  (editw, editc):
    for ph in  (editw, ):
        c.add_vector_from_file(ph)

    c.tofile(tpath)
