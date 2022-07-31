# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:38:57 2022

@author: steve
"""
import csv
from mp_api import MPRester
import os

if __name__ == "__main__":
    with MPRester(api_key="5Lcv7aW3A4tCxFzUZYDrT3egCiavfrgM") as mpr:
        dir_name = os.getcwd() + '\\mp_sample_data\\'
        data = mpr.summary.search(energy_above_hull=(0,0), 
                                  num_elements=(1,1),
                                  fields=['structure', 'composition',
                                          'symmetry', 'band_gap',
                                          'total_magnetization_normalized_vol'])
        with open(dir_name + 'properties.csv', 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['filename', 'band_gap',
                                 'total_magnetization_normalized_vol'])
            for mat in data:
                symm = mat.symmetry.symbol.replace('/', '~')
                fname = str(mat.composition) + '_' + symm + '.vasp'
                mat.structure.to(fmt='POSCAR', filename=dir_name + fname)
                csv_writer.writerow([fname, mat.band_gap,
                                     mat.total_magnetization_normalized_vol])