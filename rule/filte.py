# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append('..')
from utils import *
'''
'''
class Remover(object):
    def __init__(self, fpath, tpath):
        self.fpath, self.tpath = fpath, tpath

    def scan(self):
        self.lines = []
        with open(self.fpath) as f:
            for line in f.readlines():
                line = line.strip()
                q, t = line.split('\t')
                q = self.rem(q)
                t = self.rem(t)
                self.lines.append("\t".join([q,t]))

    def lines_scan(self, lines):
        self.lines = []
        for line in lines:
            try:
                q, t = line.split('\t')
            except:
                print line
                sys.exit(-1)
            q = self.rem(q)
            t = self.rem(t)
            self.lines.append("\t".join([q,t]))

    def get_content(self):
        return '\n'.join(self.lines)

    def tofile(self):
        with open(self.tpath, 'w') as f:
            f.write(
                self.get_content()
            )

# -------------------------------------------------------------
# -------------------------------------------------------------

class PuncRem(Remover):
    puncs = u"~ ! @ : # $ % ^ & * ( ) , . \" ' ? < >   ！ ￥ … …  ： 、 （ ） ： ‘ “ ？ 《 》 ， 。".split()
    # for cn del all taged as punc 
    def __init__(self, fpath, tpath):
        Remover.__init__(self, fpath, tpath)
        print '.. PuncRem'

    def get_lines(self):
        return self.lines

    def rem(self, line):
        #print self.puncs
        new_line = line
        for p in self.puncs:
            new_line = new_line.replace(p, u' ')
        # for Bug: enpty string
        if not new_line.strip():
            return line
        return new_line


class SegTagRem(Remover):
    rm_tokens = "ryv ry udel d p y vshi".split()

    def __init__(self, fpath, tpath):
        Remover.__init__(self, fpath, tpath)
        print '.. SegTagRem'

    def rem(self, line):
        ws = line.split()
        not_in = lambda x: not get_type(x) in self.rm_tokens 
        ws = filter(not_in, ws)
        return ' '.join(ws)

    def get_cmp(self):
        """
        get lines with no tag
        """
        def rm_tag(line):
            q,t = line.split('\t')
            qs, ts = q.split(), t.split()
            qs, ts = map(get_word, qs), map(get_word, ts)
            return '\t'.join([''.join(qs), ''.join(ts)])
        return map(rm_tag, self.lines)


class Alpha2Large(Remover):
    alphas = list("abcdefghijklmnopqrstuvwxyz")

    def __init__(self, fpath, tpath):
        Remover.__init__(self, fpath, tpath)
        print '.. Alpha2Large'
        self.alpha_dic = {}
        for a in self.alphas:
            self.alpha_dic[a] = a.upper()

    def rem(self, line):
        for k,v in self.alpha_dic.items():
            line = line.replace(k, v)
        return line

# -------------- -----------------------------
dict ={u'零':0, u'一':1, u'二':2, u'三':3, u'四':4, u'五':5, u'六':6, u'七':7, u'八':8, u'九':9, u'十':10, u'百':100, u'千':1000, u'万':10000,
       u'０':0, u'１':1, u'２':2, u'３':3, u'４':4, u'５':5, u'６':6, u'７':7, u'８':8, u'９':9,
            u'壹':1, u'贰':2, u'叁':3, u'肆':4, u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9, u'拾':10, u'佰':100, u'仟':1000, u'萬':10000, u'亿':100000000}

def getResultForDigit(a, encoding="utf-8"):
    if isinstance(a, str):
        a = a.decode(encoding)
    count = 0
    result = 0
    tmp = 0
    Billion = 0
    while count < len(a):
        tmpChr = a[count]
        #print tmpChr
        tmpNum = dict.get(tmpChr, None)
        #如果等于1亿
        if tmpNum == 100000000:
            result = result + tmp
            result = result * tmpNum
            #获得亿以上的数量，将其保存在中间变量Billion中并清空result
            Billion = Billion * 100000000 + result
            result = 0
            tmp = 0
        #如果等于1万
        elif tmpNum == 10000:
            result = result + tmp
            result = result * tmpNum
            tmp = 0
        #如果等于十或者百，千
        elif tmpNum >= 10:
            if tmp == 0:
                tmp = 1
            result = result + tmpNum * tmp
            tmp = 0
        #如果是个位数
        elif tmpNum is not None:
            tmp = tmp * 10 + tmpNum
        count += 1
    result = result + tmp
    result = result + Billion
    return result


class Ch2No(Remover):
    """
    token content
    """
    def __init__(self, fpath, tpath):
        Remover.__init__(self, fpath, tpath)

    def rem(self, line):
        ws = line.split()
        ws = map(strip, ws)
        pass

if __name__ == '__main__':
    fph, tph = args_check(2, "cmd fph tph")

    s = SegTagRem(fph, "")
    s.scan()
    lines = s.get_cmp()
    
    p = PuncRem("", "")
    p.lines_scan(lines)
    #p = PuncRem(fph, "")
    #p.scan()
    lines = p.lines

    a = Alpha2Large("" , tph)
    a.lines_scan(lines)
    a.tofile()
