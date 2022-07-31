# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 18:36:49 2022

@author: steve
"""

from data_source import Dataset
from matminer.featurizers.composition.composite import Meredig
from matminer.featurizers.structure import BagofBonds
from matminer.featurizers.structure.misc import StructureComposition
from pandas import concat, DataFrame

def featurize_row_structures(dataset, featurizer, indices, name):
    df = DataFrame([featurizer.featurize(s) for s in dataset.dat_frame['structure']])
    df = df[df.columns[indices]]
    df.columns = [name + str(i) for i in indices]
    return df
    

if __name__ == "__main__":
    dataset_1 = Dataset(['mp_sample_data'])
    mere_featurizer = StructureComposition(featurizer=Meredig())
    mere_frame = featurize_row_structures(dataset_1, mere_featurizer,
                                          range(103,120), 'meredig_')
    dataset_1.dat_frame = concat([dataset_1.dat_frame, mere_frame], axis=1)