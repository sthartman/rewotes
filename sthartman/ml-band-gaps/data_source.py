# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 11:57:07 2022

@author: steve
"""
from json import dump, load
import os
from pandas import concat, read_csv, DataFrame
from pymatgen.core.structure import Structure

class Dataset:
    def __init__(self, frame, features, properties, name):
        self.features = features
        self.name = name
        self.properties = properties
        self.dat_frame = frame
                 
    def add_feature(self, feat_frame):
        #TODO: what if one of the new features already exists in the dataframe?
        self.dat_frame = concat([self.dat_frame, feat_frame], axis=1)
        self.features = self.features + list(feat_frame.columns)
        
    def to_json(self, fname):
        with open(fname, 'w') as f:
            store_dict = {'properties': self.properties}
            store_dict['name'] = self.name
            store_dict['features'] = self.features
            self.dat_frame['structure'] = [s.as_dict() 
                                           for s in self.dat_frame['structure']]
            store_dict['frame'] = self.dat_frame.to_dict()
            dump(store_dict, f)
    
    @classmethod
    def from_dirs(cls, direc_list, name):
        dat_frame = DataFrame()
        for direc in direc_list:
            direc_path = os.getcwd() + '\\' + direc + '\\'
            with open(direc_path + 'properties.csv','r') as f:
                direc_frame = read_csv(f)
                direc_frame['structure'] = [Structure.from_file(direc_path + n) 
                                             for n in direc_frame['filename']]
                dat_frame = concat([dat_frame, direc_frame], 
                                        axis=0, ignore_index=True)
            properties = list(dat_frame.columns)
            properties.remove('filename')
            features = []
            return cls(dat_frame, features, properties, name)
        
    
    @classmethod
    def from_json(cls, fname):
        with open(fname, 'r') as f:
            store_dict = load(f)
            name = store_dict['name']
            properties = store_dict['properties']
            features = store_dict['features']
            dat_frame = DataFrame.from_dict(store_dict['frame'])
            dat_frame['structure'] = [Structure.from_dict(d) 
                                           for d in dat_frame['structure']]
            return cls(dat_frame, features, properties, name)
