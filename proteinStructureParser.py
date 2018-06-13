#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 19:48:03 2018

@author: fabrizio

OLD: it is only a parser of dataset metadata
"""
import numpy as np
import random as rd

file='cullpdb+profile_6133_filtered.npy'
dataset = np.load('data/'+file)

print(('-'*10)+'dataset: '+file+('-'*10))
print('shape: ',dataset.shape)

print('reshaping...')

primary_letters = ['A', 'C', 'E', 'D', 'G', 'F', 'I', 'H', 'K', 'M', 'L', 'N', 'Q', 'P', 'S', 'R', 'T', 'W', 'V', 'Y', 'X','NoSeq']
secondary_letters = ['L', 'B', 'E', 'G', 'I', 'H', 'S', 'T','NoSeq']

dataset = np.reshape(dataset,(dataset.shape[0],700,57))
print('shape: ',dataset.shape)
rand =rd.randint(0,dataset.shape[0]-1)
print('Protein number ',rand) 
example = dataset[rand,:,:]
print('shape ',example.shape)

print('Example ',rand)
protein = dataset[rand,:,:]
print('shape of protein ',protein.shape)

for i in range (700):
    amino = protein[i,:]
    primary_structure = amino[:22]
    letter = primary_letters[primary_structure.tolist().index(1)]
    #print('primary structure: ',primary_structure,' => ',letter)
    if(amino[32]==1):
        print(i,')',amino[32],'<----------------- C')
        print('next letter => ',primary_letters[protein[(i+1),:][:22].tolist().index(1)])
        break
    #print(i,')',amino[32])
    print(i,')  relative and absolute solvent accessibility ',amino[33:35])











