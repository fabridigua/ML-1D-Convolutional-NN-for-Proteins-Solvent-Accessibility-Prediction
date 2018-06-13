
import numpy as np

class DataManager:
    def __init__(self,train="",test="", classes=2, solv_type=0):
        self.train_file = train
        self.test_file = test
        self.classes = classes
        self.solv_type = solv_type# 0 = relative, 1=  absolute solvent accessibility (index 33 or 34)
                
    
    def getDataset(self,limit=700):
        dataset = np.load('data/'+self.train_file)
        dataset = np.reshape(dataset,(dataset.shape[0],700,57))
        
        sec_data_indexes = range(30) # indici della struttura secondaria
        
        train_num = int(dataset.shape[0]*0.65)#indice fino al quale prendo il trainset
        v_idx = int(dataset.shape[0]*0.15)
        #totale: 80% train (di cui 15 validazione) e 20% test
        
        print("train proteins num: ",train_num+v_idx)
        print("di cui per la validazinìone: ",v_idx)
        print("totale: ",dataset.shape[0])
        
        trainset = dataset[:train_num,:,sec_data_indexes]
        if self.solv_type==0 :
                trainlabel = dataset[:train_num,:,33:34]
                vallabel = dataset[train_num:(train_num+v_idx),:,33:34]
                testlabel = dataset[(train_num+v_idx):,:,33:34]
        else:
            trainlabel = dataset[:train_num,:,34.35]
            vallabel = dataset[train_num:train_num+v_idx,:,34:35]
            testlabel = dataset[(train_num+v_idx):,:,34:35]
            
        valset = dataset[train_num:(train_num+v_idx),:,sec_data_indexes]
        trainset = np.concatenate((trainset, valset), axis=0)
        trainlabel = np.concatenate((trainlabel, vallabel), axis=0)
        
        testset = dataset[(train_num+v_idx):,:,sec_data_indexes]
        
        from keras.utils import to_categorical
        trainlabel = to_categorical(trainlabel,2)
        testlabel = to_categorical(testlabel,2)
        vallabel = to_categorical(vallabel,2)
        
        trainmask = dataset[:train_num,:,30]* -1 + 1
        valmask = dataset[train_num:(train_num+v_idx),:,30]* -1 + 1
        testmask = dataset[(train_num+v_idx):,:,30]* -1 + 1
        
        trainmask = trainmask[:,:limit]
        valmask = valmask[:,:limit]
        testmask = testmask[:,:limit]
        
        trainvalmask = np.concatenate((trainmask, valmask), axis=0)
        
        train_tmp = []
        train_lab_tmp = []
        val_tmp = []
        val_lab_tmp = []
        test_tmp = []
        test_lab_tmp = []
        
        for i in range(valset.shape[0]):
          p = valset[i,:limit,:]
          pl = vallabel[i,:limit,:]
          num_amino = int(sum(valmask[i]))
          if(num_amino<=limit):
            val_tmp.append(p)
            pl[num_amino:,:]=[0,0]
            val_lab_tmp.append(pl)
        
        for i in range(trainset.shape[0]):
          p = trainset[i,:limit,:]
          pl = trainlabel[i,:limit,:]
          num_amino = int(sum(trainvalmask[i]))
          if(num_amino<=limit):
            train_tmp.append(p)
            pl[num_amino:,:]=[0,0]
            train_lab_tmp.append(pl)
        
        for i in range(testset.shape[0]):
          p = testset[i,:limit,:]
          pl = testlabel[i,:limit,:]
          num_amino = int(sum(testmask[i]))
          if(num_amino<=limit):
            test_tmp.append(p)
            pl[num_amino:,:]=[0,0]
            test_lab_tmp.append(pl)
        
        trainset = np.array(train_tmp).astype(float)
        valset = np.array(val_tmp).astype(float)
        trainlabel = np.array(train_lab_tmp).astype(float)
        vallabel = np.array(val_lab_tmp).astype(float)
        testset = np.array(test_tmp).astype(float)
        testlabel = np.array(test_lab_tmp).astype(float)
        
        print("trainset.shape ",trainset.shape)
        print("testdata.shape ",testset.shape)
        print("valset.shape ",valset.shape)
        print("testlabel.shape ",testlabel.shape)
        print("trainlabel.shape ",trainlabel.shape)
        print("vallabel.shape ",vallabel.shape)

        
        return trainset, valset, trainlabel, vallabel,testset,testlabel
        
        