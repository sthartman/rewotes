# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 18:36:49 2022

@author: steve
"""

from copy import deepcopy
from data_source import Dataset
from matminer.featurizers.composition.composite import Meredig
from matminer.featurizers.structure import BagofBonds
from matminer.featurizers.structure.composite import JarvisCFID
from matminer.featurizers.structure.matrix import CoulombMatrix
from matminer.featurizers.structure.misc import StructureComposition
from multiprocess import Pool
from numpy import array_split, shape
from pandas import DataFrame

def featurize_row_structures(dataset, featurizer, indices, name):
    df = DataFrame([featurizer.featurize(s) for s in dataset.dat_frame['structure']])
    df = df[df.columns[indices]]
    df.columns = [name + str(i) for i in indices]
    return df
    

if __name__ == "__main__":
    dataset_1 = Dataset.from_dirs(['mp_sample_data'], 'single_element_stable')
#    dataset_1 = Dataset.from_json('dataset_1.json')
#    mere_featurizer = StructureComposition(featurizer=Meredig())
#    mere_frame = featurize_row_structures(dataset_1, mere_featurizer,
#                                          range(103,120), 'meredig_')
#    dataset_1.add_feature(mere_frame)
    
#    cmat_featurizer = CoulombMatrix(flatten=False)
#    cmat_featurizer.fit(dataset_1.dat_frame['structure'])
#    bofb_featurizer = BagofBonds(cmat_featurizer)
#    bofb_featurizer.fit(dataset_1.dat_frame['structure'])
#    bofb_frame = DataFrame([bofb_featurizer.featurize(s) 
#                            for s in dataset_1.dat_frame['structure']])

    def proxy(chunk, ftzr):        
        return [ftzr.featurize(s) for s in chunk]

    n_cpu = 6
    chunks = array_split(dataset_1.dat_frame['structure'][0:6], n_cpu, axis=0)
    cf = JarvisCFID(use_adf=False, use_chg=False, use_ddf=False,
                    use_cell=False, use_rdf=False, use_nn=False)
    with Pool(n_cpu) as pool:
        data = pool.starmap(proxy, [(chunk, deepcopy(cf)) for chunk in chunks])
        cfid_frame = DataFrame([row[0][:] for row in data],
                               columns=cf.feature_labels())
        dataset_1.add_feature(cfid_frame)
        dataset_1.to_json('dataset_1.json')
