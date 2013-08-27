# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
import sys
from utils import get_num_lines, args_check

class Gen(object):
    formats = {
        '1':1,
        '-1':0,
    }

    def __init__(self, fph, test_ph, tph):
        """
        fph : file created by liblinear
        test_ph: testData
        """
        self.fph, self.test_ph, self.tph = \
                fph, test_ph, tph

    def __call__(self):
        self.trans()
        self.tofile()

    def trans(self):
        num_lines = get_num_lines(self.test_ph)
        self.lines = []
        with open(self.fph) as resf:
            with open(self.test_ph) as testf:
                for i in range(num_lines):
                    #print i
                    res = resf.readline()
                    tes = testf.readline()
                    label = self.formats.get(res.strip())
                    if label is None:
                        break
                    #print 'label:', label
                    line = "%d\t%s" % (label, tes.strip())
                    self.lines.append(line)

    def tofile(self):
        with open(self.tph, 'w')  as f:
            f.write('\n'.join(self.lines))



if __name__ == "__main__":
    fph, test_ph, tph = args_check(3, "")
    g = Gen(fph, test_ph, tph)
    g()
