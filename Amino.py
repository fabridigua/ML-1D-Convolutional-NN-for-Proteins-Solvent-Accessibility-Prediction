import numpy as np

class Amino:
    def __init__(self, features=[]):
        self.residues = features[:22]
        self.secondary_structure = features[22:31]
        self.terminals = features[31:33]
        self.accessibility = features[33:35]
        self.sequence_profile = features[35:]

    def isFirst(self):
        return self.terminals[0]==1

    def isLast(self):
        return self.terminals[1]==1
    
    def getResidueLetter(self):
        primary_letters = ['A', 'C', 'E', 'D', 'G', 'F', 'I', 'H', 'K', 'M', 'L', 'N', 'Q', 'P', 'S', 'R', 'T', 'W', 'V', 'Y', 'X','NoSeq']
        return primary_letters[self.residues.tolist().index(1)]
    
    def getSecondaryLetter(self):
        secondary_letters = ['L', 'B', 'E', 'G', 'I', 'H', 'S', 'T','NoSeq']
        return secondary_letters[self.secondary_structure.tolist().index(1)]
    
    def updateFeatures(self,residues=[],secondary=[],terminals=[],accs=[],sequence=[]):
        if(residues!=[]): self.residues = residues
        if(secondary!=[]): self.secondary_structure = secondary
        if(terminals!=[]): self.terminals = terminals
        if(accs!=[]): self.accessibility = accs
        if(sequence!=[]): self.sequence_profile = sequence
        
    def toArray(self):
        a = np.concatenate((self.residues,self.secondary_structure,self.terminals,self.accessibility,self.sequence_profile))
        return a