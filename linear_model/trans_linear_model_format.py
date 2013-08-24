# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
import sys
sys.path.append("..")

COMPILER = "pypy"

from utils import strip, args_check, get_num_lines


class LinearFormater(object):
    def __init__(self):
        self.lst = []
        self.maxs = []

    def set_labels(self, a):
        for label in a:
            lst = [label]
            self.lst.append(lst)

    def add_lst(self, lst, need_count=True):
        """
        list of list
        [
            [id, id, id],
            [id, id, id],
        ]
        parameters:
            count=True/False, count times it occurs
        """
        _max = -1
        for id, line in enumerate(lst):
            #print line
            #print id
            if not line: 
                continue
            _max = max(_max, max(line))
            if need_count:
                count = self.get_list_with_count(line)
            else:
                count = self.get_list(line)
            #datas[id] = count
            self.lst[id].append(count)
        self.maxs.append(_max)

    def tofile(self, path):
        lines = []
        for id, li in enumerate(self.lst):
            label = "+1" if li[0]==1 else "-1"
            line = [label]
            for i,data in enumerate(li[1:]):
                _max = 0 if i==0 else self.maxs[-1]
                keyvalues = data.items()
                keyvalues = sorted(keyvalues, key=lambda x:x[0])
                for key,value in keyvalues:
                    key += _max+1
                    line.append(
                        "%d:%d" % (key, value))
            line = ' '.join(line)
            lines.append(line)

        with open(self.tpath, 'w') as f:
            f.write("\n".join(lines))

    """
    def test2file(self, path):
        lines = []
        for id, li in enumerate(self.lst):
            line = []
            for i,data in enumerate(li):
                _max = -1 if i==0 else self.maxs[-1]
                keyvalues = data.items()
                keyvalues = sorted(keyvalues, key=lambda x:x[0])
                for key,value in keyvalues:
                    key += _max+1
                    line.append(
                        "%d:%d" % (key, value))
            line = ' '.join(line)
            lines.append(line)
        with open(self.tpath, 'w') as f:
            f.write("\n".join(lines))
    """
    
    def get_list_with_count(self, lst):
        ids = list(set(lst))
        ids.sort()
        count = {}
        for id in ids: count[id] = 0

        for id in lst:
            count[id] = count.get(id, 0) + 1
        return count

    def get_list(self, lst):
        ids = list(set(lst))
        ids.sort()
        count = {}
        for id in ids:
            count[id] = 1
        return count


class WordLinear(LinearFormater):
    """
    input a title wid file
    """
    def __init__(self, label_path, fpath, tpath):
        LinearFormater.__init__(self)
        self.label_path = label_path
        self.fpath = fpath
        self.tpath = tpath

    def __call__(self, is_train=True):
        if is_train:
            self.scan()
            self.tofile(self.tpath)
        else:
            self.test_scan()
            self.tofile(self.tpath)

    def scan(self):
        with open(self.label_path) as f:
            ws = f.read().split()
            ws = map(strip, ws)
            ws = map(int, ws)
            self.set_labels(ws)

        with open(self.fpath) as f:
            datas = []
            for line in f.readlines():
                ws = line.split()
                ws = map(strip, ws)
                ws = map(int, ws)
                datas.append(ws)
            self.add_lst(datas)

    def test_scan(self):
        num_lines = get_num_lines(self.fpath)
        #self.lst = [ [] for i in range(num_lines)]
        labels = [1 for i in range(num_lines)]
        self.set_labels(labels)
        with open(self.fpath) as f:
            datas = []
            for line in f.readlines():
                ws = line.split()
                ws = map(strip, ws)
                ws = map(int, ws)
                datas.append(ws)
            self.add_lst(datas)



if __name__ == '__main__':
    args = sys.argv[1:]
    _type = args[0]

    if _type == "word":
        _type, label_path, fpath, tpath = args_check(4, "cmd [label_path] [fpath] [tpath]")
        w = WordLinear(label_path, fpath, tpath)
        w()
    elif _type == "test":
        _type, fpath, tpath = args_check(3, "cmd [label_path] [fpath] [tpath]")
        w = WordLinear(None, fpath, tpath)
        w(False)
