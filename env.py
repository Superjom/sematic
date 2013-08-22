#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Aug 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
from __future__ import division

import os
from utils import pjoin

PROJECT_PATH = os.path.dirname(__file__)
DATA_PATH = pjoin(PROJECT_PATH, 'data')

LABELED_DATA_PATH = pjoin(DATA_PATH, 'train4user_with_label.txt')

DB_PATH = pjoin(DATA_PATH, 'database.bdb')

# charater-wise 编辑距离
CHA_EDIT_DIS_PH = pjoin(DATA_PATH, 'cha_edit_dis.txt')
# word-wise 编辑距离
WORDID_EDIT_DIS_PH = pjoin(DATA_PATH, 'wordid_edit_dis.txt')

# 用于源title分词
SOURCE_TITLES_PH = pjoin(DATA_PATH, 'source_titles.txt')
TARGET_TITLES_PH = pjoin(DATA_PATH, 'target_titles.txt')
# word splited files
SPLITED_SOURCE_TITLES_PH = pjoin(DATA_PATH, 'source_titles.txt_split')
SPLITED_TARGET_TITLES_PH = pjoin(DATA_PATH, 'target_titles.txt_split')

WORD_ID_SOURCE_TARGET_PH = pjoin(DATA_PATH, 'word_id_source_target.txt')


DIC_PH = pjoin(DATA_PATH, 'dic.txt')

# berkely db
KEY_LABELED_DATA = 'labeled'


