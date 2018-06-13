import numpy as np
from Amino import Amino as amino

class Protein:
    def __init__(self, data=[]):
        self.aminos = self.parseAminos(data) if data!=[] else []
        self.aminos_numb = self.getAminoNum() if data!=[] else 0

    def parseAminos(self,data):
        amins = []
        for a in range(700):
            ami = amino(data[a,:])
            amins.append(ami)
        return amins

    def getAminoNum(self):
        count=0
        for i in range(700): 
            if(self.aminos[i].isLast()):
                count = i+1
                break
        return count # max 700 

    def printPrimaryStructure(self,with_letters=False):
        if(with_letters):
            print('with_letters') #TODO
        else:
            for am in self.aminos:
                print(self.aminos.index(am),') ',am.residues,' -> ',am.accessibility)
        
        
    def setAminos(self,aminos):#aminos è un array di Amino
        self.aminos = aminos
        self.aminos_numb = self.getAminoNum()
        
    def addAmino(self,amino):
        if(len(self.aminos)<=0):
            self.aminos=[]
        self.aminos.append(amino)
        
    def toArray(self):
        return np.array([aa.toArray() for aa in self.aminos])
        
        