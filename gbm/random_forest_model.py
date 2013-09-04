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
from sklearn.ensemble import RandomForestClassifier as rfc

class DataSet(object):
    def __init__(self):
        self.data = []
        self.labels = []

    def add_vector(self, _list):
        if not self.data:
            for d in _list:
                self.data.append([d])
        else:
            assert len(_list) == len(self.data), "%d != %d" % (len(_list), len(self.data))
            for i, d in enumerate(_list):
                self.data[i].append(d)

    def add_vector_from_file(self, ph):
        with open(ph) as f:
            c = f.read()
            datas = map(float, c.split())
            self.add_vector(datas)

    def set_labels(self, _list):
        self.labels = _list

    def label_from_file(self, path, data_map=None):
        """
        data_map: dic for label to data
        """
        with open(path) as f:
            c = f.read()
            _list = map(strip, c.split())
            if data_map:
                self.labels = map(lambda x: data_map[x], _list)
            else:
                self.labels = map(int, _list)

class RFModel(object):
    """
    use random forest to classify the features
    """
    def __init__(self, train_dataset, predict_dataset, toph=None):
        self.clf = rfc(n_estimators=300)
        self.train_dataset = train_dataset
        self.predict_dataset = predict_dataset
        self.toph = toph
        assert len(self.train_dataset.labels) == len(self.train_dataset.data)

    def train(self):
        self.clf.fit(self.train_dataset.data, self.train_dataset.labels)

    def predict(self):
        self.pred_labels = self.clf.predict(self.predict_dataset.data)
        return self.pred_labels

    def tofile(self):
        assert self.toph is not None
        with open(self.toph, 'w') as f:
            f.write(
                '\n'.join(map(str, self.pred_labels)))

def train2file(*vec_phs):
    """
    args:
        label_ph, toph, vec paths of train and test
    vec_phs:
        paths of vectors  and will be splited to 2 parts
    """
    print 'args: ', vec_phs
    vec_phs = vec_phs[0]
    label_ph = vec_phs[0]
    toph = vec_phs[1]
    vec_phs = vec_phs[2:]
    print 'vec_phs:', vec_phs
    length = len(vec_phs)
    part_length = int(length/2)
    train_vec_phs, test_vec_phs = vec_phs[:part_length], vec_phs[part_length:]
    # build dataset
    datasets = []
    for phs in (train_vec_phs, test_vec_phs):
        dataset = DataSet()
        datasets.append(dataset)
        for ph in phs:
            dataset.add_vector_from_file(ph)
    train_dataset, test_dataset = datasets
    # set labels
    train_dataset.label_from_file(label_ph)

    model = RFModel(train_dataset, test_dataset, toph)
    model.train()
    model.predict()
    model.tofile()




if __name__ == '__main__':
    # add subsentence sim, tfidf sim
    args = sys.argv[1:]
    print "args: ", args
    train2file(args)

