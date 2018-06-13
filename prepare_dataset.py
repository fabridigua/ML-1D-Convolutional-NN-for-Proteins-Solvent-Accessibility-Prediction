#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 13:26:04 2018

@author: fabrizio

Script to generate train, validate and test set

Require a npy file with the dataset, see generate_sample for the sample generation
"""


    train_file = 'DATASET_NAME'
    data_saved = np.load(train_file+'.npy')
    #print('data saved shape: ',data_saved.shape)
    
    dbManager = DM(train=train_file)    
    X_train, X_valid, y_train, y_valid,testset,testlabel = dbManager.getDataset(limit=700)          
    
    # Now you can use for the classification
    # See the notebook 