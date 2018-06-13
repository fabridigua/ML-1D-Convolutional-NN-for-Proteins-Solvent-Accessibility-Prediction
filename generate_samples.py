#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 12:22:18 2018

@author: fabrizio

Generate Random Samples from DSSP extracted from PDB (CullPDB folder)
Output is a numpy file (.npy)

proteins_num is the wanted samples number
NOTE: the output samples can be less than proteins_num cause
      proteins are not selected if have less than 700 aminoacids
"""

import os
import numpy as np
import datetime
from PdbParser import PdbParser as PDB

proteins_num=8800 # output 7032 proteins

if not os.path.exists('data/generated'):
    os.makedirs('data/generated')
    
if not os.path.exists('data/cullpdb/pdbs'):
    print("You have to put pdb files in data/pdbs")

def generateSamples(num):
        # PDB => DSSP => SAMPLES
        pdbParser = PDB()
        pp=pdbParser.convertDSSPStoSamples(num)
        print('\n',np.array(pp).shape)
        file=datetime.datetime.now().strftime('%y.%m.%d_%H.%M')+'_dataset_'+str(num)+'_proteins'
    #    file = '18.04.08_17.51_dataset_5000_proteins'
        train_file = 'data/generated/'+file
        np.save(train_file,np.array(pp))
        return train_file
    
print(("-")*5,"Generating samples",("-")*5)

train_file = generateSamples(proteins_num)
data_saved = np.load(train_file+'.npy')
print('Data saved shape: ',data_saved.shape)