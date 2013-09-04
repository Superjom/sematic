# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division
import sys
import re
from string import *
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf8')
from utils import *

def str2list(ch):
    print ch
    print len(ch)
    ls = []
    for i in range(len(ch)):
        ls.append(ch)
    return ls

mat = re.compile(r'[A-Z]')
def alp2lower(ch):
    if mat.match(ch):
        return lower(ch)
    return ch

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

    def scan(self, as_char=False):
        self.sims = []
        with open(self.ph) as f:
            for i, line in enumerate(f.readlines()):
                #print 'i, line: ' , i, line
                line = line.decode('utf8')
                line = line.strip()
                line = line.replace(' ', '')
                print i
                try:
                    query, title = line.split('\t')
                except:
                    query = line
                    title = "wrong wrong"
                qs = map(alp2lower, list(query)) if as_char else query.split()
                ts = map(alp2lower, list(title)) if as_char else title.split()
                sim = self.sim(map(strip, qs), map(strip, ts))
                self.sims.append(sim)

    def tofile(self):
        with open(self.tph, 'w') as f:
            f.write(
                '\n'.join(map(str, self.sims)))

    def sim(self, ws1, ws2):
        query_set = set(ws1)
        title_set = set(ws2)
        #print 'query_set', query_set
        #print 'title_set', title_set
        query_and_title = query_set & title_set
        #print query_and_title
        #print query_set
        #print query_set, title_set
        return float(len(query_and_title)) / len(query_set)

class CharSubSeq(SubSeq):
    """
    以字为单位
    """
    def __init__(self, ph, tph):
        SubSeq.__init__(self, ph, tph)

    def __call__(self):
        self.scan(as_char=True)
        self.tofile()

UPPER = 0.95

def filter_sim_label(up_ph, sim_ph):
    """
    确保子句能够标注为1
    """
    with open(up_ph) as upf:
        lines = []
        with open(sim_ph) as sf:
            sims = map(float, sf.read().split())
            for i,line in enumerate(upf.readlines()):
                line = line.strip()
                label, query, url, title = line.split('\t')
                if sims[i] >= UPPER:
                    label = '1'
                new_line = '\t'.join([label, query, url, title])
                lines.append(new_line)

        with open(up_ph, 'w') as f:
            f.write('\n'.join(lines))


if __name__ == '__main__':
    args = ArgsAction()
    args.add_action(2, "subseq", SubSeq, "cmd fph, tph")
    args.add_action(2, "subseq_char", CharSubSeq, "cmd fph, tph")
    args.add_action(2, "filter_sim_label", filter_sim_label, "cmd up_ph, sim_ph", is_class=False)
    args.start()
