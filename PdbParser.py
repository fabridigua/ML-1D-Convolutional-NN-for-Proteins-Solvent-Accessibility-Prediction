#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 12:05:56 2018

@author: fabrizio
"""

import os
import os.path
import numpy as np
import sys
from prody import execDSSP
from Amino import Amino as aminoacido
from Protein import Protein as proteina
from DSSPData import DSSPData as DSSP
from keras.utils import to_categorical

class PdbParser:
    def __init__(self):
        #default folders with pdbs and (saved) DSSPs:
        self.pdbdir='data/cullpdb/pdbs/' 
        self.dsspdir='data/cullpdb/dssp/'    
        if not os.path.exists(self.dsspdir):
            os.makedirs(self.dsspdir)
        
    def convertSomePDBtoDSSP(self,quantity):
        #converts a given number of pdb to DSSP
        for root, dirs, files in os.walk(self.pdbdir):  
            for filename in files:
                quantity-=1
                if(quantity<0):
                    break
                print(quantity,' )',filename,' converted to dssp')
                # here uses from prody import execDSSP
                execDSSP(self.pdbdir+filename,outputdir=self.dsspdir)
            break
        
    def convertiSinglePDBtoDSSP(self,file): # con estensione
        if(os.path.isfile(self.pdbdir+file)):
            execDSSP(self.pdbdir+file,outputdir=self.dsspdir)
        else:
            print("File "+self.pdbdir+file+" not found..\n")

    def getDSSPInfo(self,file):
        # for debug
        if(os.path.isfile(self.dsspdir+file)):
            print('-'*7,'DSSP ',file,'-'*7)
            dsspData = DSSP()
            dsspData.parseDSSP(self.dsspdir+file)
            dsspACC = np.array(dsspData.getACC())
            print('ACC: ',dsspACC)
            print(dsspACC.shape)
            getAAs = np.array(dsspData.getAAs())
            print('ACC: ',getAAs)
            print(getAAs.shape)
            if(dsspACC.shape[0]>700):
                return 0
            else:
                return 1
        else:
            print('dssp not found..searching in pdbs folder')
            self.convertiSinglePDBtoDSSP(file.replace('dssp','pdb'))
            if(os.path.isfile(self.dsspdir+file)):
                self.getDSSPInfo(file)
            else:
                print('file not found: ',file)
        
    def getAllDSSPInfo(self,c=8000):
        count=0
        for root, dirs, files in os.walk(self.dsspdir):
            for filename in files:
                #count += self.getDSSPInfo(filename)
                dssps = self.extractSSfromDSSP(filename)
                print([x[1] for x in dssps])
                count +=1
                if(count>=c):
                    break
            break
        print('count: ',count)
        
    def convertDSSPtoSample(self,file):
        if(os.path.isfile(self.dsspdir+file)):
            #print('-'*7,'CONVERTING DSSP ',file,' TO SAMPLE','-'*7)
            primaryArray=['A', 'C', 'E', 'D', 'G', 'F', 'I', 'H', 'K', 'M', 'L', 'N', 'Q', 'P', 'S', 'R', 'T', 'W', 'V', 'Y', 'X']
            secondaryArray=['L', 'B', 'E', 'G', 'I', 'H', 'S', 'T']
            dssp = self.extractSSfromDSSP(file)
            dsspData = DSSP()
            dsspData.parseDSSP(self.dsspdir+file)
            dsspPrimary = np.array(dsspData.getAAs())
            dsspSecondary = np.array([x[1] for x in dssp])
            dsspSecondary[:] = [x if x != ' ' else 'L' for x in dsspSecondary]
            dsspACC = np.array(dsspData.getACC())
#            print('ACC: ',dsspACC)
#            print(dsspACC.shape)
            acc_max=float(max(dsspACC))
            if(dsspACC.shape[0]>700):
                return 0
            else:#fa la conversione solo se ci sono <=700 aminoacidi
                am_num=len([x for x in dsspPrimary if x in primaryArray])
                j=0
                p = proteina()
                aminos=[]
                num_to_add=0
                for i in range(700):
                    a = aminoacido()
                    no_add = False
                    if i<len(dsspPrimary):
                        if(dsspPrimary[i] in primaryArray):
                            #print(j,'/',len(dsspSecondary),': ',(dsspSecondary[j]),' -> ',secondaryArray.index((dsspSecondary[j])),' --> ',np.array(to_categorical(secondaryArray.index((dsspSecondary[j])),9)))
                            a.updateFeatures(residues=np.array(to_categorical(primaryArray.index((dsspPrimary[i])),22)))
                            a.updateFeatures(secondary=np.array(to_categorical(secondaryArray.index((dsspSecondary[j])),9)))
                            if(i==0): a.updateFeatures(terminals=np.array([1,0])) 
                            elif(i==(am_num-1)): a.updateFeatures(terminals=np.array([0,1]))
                            else: a.updateFeatures(terminals=np.array([0,0]))
                            j+=1
                            acc = float(dsspACC[i])
                            acc_ass= 1 if acc>15 else 0
                            acc_rel= 1 if (acc/acc_max)>0.15 else 0
                            a.updateFeatures(accs=np.array([acc_rel,acc_ass]))
                            a.updateFeatures(sequence=np.array([0]*22))    
                        else:
                            num_to_add+=1
                            no_add = True
                    else:
                        a.updateFeatures(residues=np.array(to_categorical(21,22)))
                        a.updateFeatures(secondary=np.array(to_categorical(8,9)))
                        a.updateFeatures(terminals=np.array([0,0]))
                        a.updateFeatures(accs=[0,0])
                        a.updateFeatures(sequence=np.array(to_categorical(21,22)))
                    if no_add is False: aminos.append(a)
                for k in range(num_to_add):
                    a = aminoacido()
                    a.updateFeatures(residues=np.array(to_categorical(21,22)))
                    a.updateFeatures(secondary=np.array(to_categorical(8,9)))
                    a.updateFeatures(terminals=np.array([0,0]))
                    a.updateFeatures(accs=[0,0])
                    a.updateFeatures(sequence=np.array(to_categorical(21,22)))
                    aminos.append(a)
                p.setAminos(aminos)
                #print(np.array(p.toArray()).shape)
                return p
        else:
            #print('\nDSSP not found..searching in pdbs folder: '+file)
            self.convertiSinglePDBtoDSSP(file)
            #print("\nself.dsspdir+file: "+self.dsspdir+file.replace('pdb','dssp'))
            if(os.path.isfile(self.dsspdir+file.replace('pdb','dssp'))):
                #print("\n --> found self.dsspdir+file: "+self.dsspdir+file.replace('pdb','dssp'))
                p = self.convertDSSPtoSample(file.replace('pdb','dssp'))
                return p
            else:
                print('Error, file not found: ',file)
                return 0
            
    def convertDSSPStoSamples(self,c=8000):
        count=0
        proteins = []
        for root, dirs, files in os.walk(self.pdbdir):
            for filename in files:
                protein = self.convertDSSPtoSample(filename)
                if(protein!=0): proteins.append(protein.toArray())
                #time.sleep(1)
                sys.stdout.write("\rConverting DSSP: %d%%" % (count*100/c))
                sys.stdout.flush()
                count +=1
                if(count>=c):
                    break
            break
        return proteins
            
    def extractSSfromDSSP(self,in_dssp, path=True):
        if path:
            with open(self.dsspdir+in_dssp, 'r') as inf:
                dssp_out = inf.read()
        else:
            dssp_out = in_dssp[:]
        dssp_residues = []
        go = False
        for line in dssp_out.splitlines():
            if go:
                try:
                    res_num = int(line[5:10].strip())
                    chain = line[10:12].strip()
                    residue = line[13]
                    ss_type = line[16]
                    phi = float(line[103:109].strip())
                    psi = float(line[109:116].strip())
                    dssp_residues.append([res_num, ss_type, chain,
                                          residue, phi, psi])
                except ValueError:
                    pass
            else:
                if line[2] == '#':
                    go = True
                pass
        return dssp_residues

            