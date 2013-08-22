#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Aug 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division
import os
import sys
sys.path.append('..')

from utils import args_check
import env

def split_word(fpath, tpath):
    data_dir = os.path.join("/home/chunwei/trunk", "tools/libTCWordSeg3.4.0/data")
    program = os.path.join(env.PROJECT_PATH,'TCWordSeg')
    cmd = ' '.join([
            program, data_dir,
            fpath, tpath,
            ])

    print os.popen(cmd)



if __name__ == "__main__":
    ppath, wpath = args_check(2, "cmd [paragraph_path] [words_path]")

    split_word(ppath, wpath)
    #remove_stop_words(wpath)
