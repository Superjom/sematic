# -*- coding: utf-8 -*-
'''
Created on Jul 9, 2013

@author: Chunwei Yan @ pkusz
@mail:  yanchunwei@outlook.com
'''
import sys
sys.path.append('..')
from utils import *
from numpypy import *

# 稀疏维度
N_DEMEN = 10

def trans_lda_format(fpath, tpath):
    lines = []
    with open(fpath) as f:
        for line in f.readlines():
            s, t = map(strip, line.split('\t'))
            lines += [s, t]
    with open(tpath) as f:
        f.write(
           '\n'.join(lines) 
        )

def format_lda_result2_titles(fpath, tpath, from_no, to_no):
    """
    trans lda result to "0.1 0.1\t0.2 0.2"
    """
    from_no = 2 * from_no + 1
    to_no *= 2
    lines = []
    with open(fpath) as f:
        for no,line in enumerate(f.readlines()):
            no += 1
            if from_no <= no and  to_no >= no:
                lines.append(line.strip())
    num_lines = int(len(lines) / 2)
    new_lines = []
    sims = []
    for i in range(num_lines):
        i *= 2
        ls1 = lines[i].split()
        ls2 = lines[i+1].split()
        a1 = array(map(float, ls1))
        a2 = array(map(float, ls2))
        sim = sum(a1*a2) / ( 
                sqrt(sum(a1**2)) * sqrt(sum(a2**2)))
        sims.append(sim)
        
    _min = min(sims)
    _max = max(sims)

    for sim in sims:
        _list = sparse_value2list(sim, N_DEMEN, _min, _max)
        new_lines.append(
                ' '.join(map(str, _list)))

    with open(tpath, 'w') as f:
        f.write('\n'.join(new_lines))





from combine_word_and_token_and_editdis2linear_format import CombinedModel


if __name__ == '__main__':
    _type = sys.argv[1]
    if _type == 'trans_format':
        _type, fpath, tpath = args_check(3, "cmd fpath, tpath")
        trans_lda_format(fpath, tpath)

    elif _type == 'format_lda_res':
        _type, fpath, tpath, from_no, to_no= args_check(5, "cmd fpath, tpath")
        from_no, to_no = int(from_no), int(to_no)
        format_lda_result2_titles(fpath, tpath, from_no, to_no)
    # -----------------------------------------------------------
    elif _type == 'trans_linear_model':
        action = sys.argv[2]
        c = CombinedModel()
        if action == "train":
            _type, action, tpath, label_ph, lda_titles_ph, num_topics = \
                args_check(6, "cmd _type, action[train/test], tpath, label_ph, lda_titles_ph num_topics")
            c.label_from_file(label_ph)
        else:
            _type, action, tpath, lda_titles_ph, num_topics = \
                args_check(5, "cmd _type, action[train/test], tpath, lda_titles_ph num_topics")
            c.label_to_test(lda_titles_ph)

        #num_topics = int(num_topics)
        c.add_data_from_file(lda_titles_ph, N_DEMEN, need_count=False)
        #c.add_vector_from_file(lda_titles_ph)
        c.tofile(tpath)
    # -----------------------------------------------------------
