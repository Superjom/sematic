# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division

import sys
sys.path.append('..')
from utils import *

from linear_model.combine_word_and_token_and_editdis2linear_format import CombinedModel

class Vector(CombinedModel):
    def __init__(self, _type,  vec_ph, tph, label_ph):
        self.label_ph, self.vec_ph, self.tph = \
                label_ph, vec_ph, tph
        self._type = _type
        CombinedModel.__init__(self)

    def __call__(self):
        if self._type == 'train':
            self.label_from_file(self.label_ph)
        else:
            self.label_to_test(self.vec_ph)
        self.add_vector_from_file(self.vec_ph)
        self.tofile(self.tph, True)


if __name__ == '__main__':
    args = ArgsAction()
    args.add_action(4, "vector", Vector, "cmd _type:train/test, vec_ph, tph, ?label_ph")
    args.start()

