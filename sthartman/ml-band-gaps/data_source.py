# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 11:57:07 2022

@author: steve
"""
import os
from pandas import concat, read_csv, DataFrame
from pymatgen.core.structure import Structure

class Dataset:
    def __init__(self, direc_list):
        self.dat_frame = DataFrame()
        for direc in direc_list:
            direc_path = os.getcwd() + '\\' + direc + '\\'
            self.read_dir(direc_path)
        self.properties = list(self.dat_frame.columns)
        self.properties.remove('filename')
        self.features = []
                 
    def read_dir(self, direc_path):
        with open(direc_path + 'properties.csv','r') as f:
            direc_frame = read_csv(f)
            direc_frame['structure'] = [Structure.from_file(direc_path + n) 
                                         for n in direc_frame['filename']]
            self.dat_frame = concat([self.dat_frame,direc_frame], 
                                    axis=0, ignore_index=True)
    
    def add_features(self, feat_list):
        pass
        
if __name__ == "__main__":
    dataset_1 = Dataset(['mp_sample_data'])
#    dataset_2 = Dataset(['mp_sample_data', 'mp_sample_data_2'])
#    print(dataset_2)