
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import glob
import re


# In[2]:

target = np.load('G:/Phase2Data/target/target_1980_2010.npy')
label = pd.DataFrame(target).astype(float)


# In[ ]:

pathName = 'G:/Phase2Data/*.npy'
def getDataFrames(pathName):
    for npyFile in glob.glob(pathName):
        pathSplit = re.split('data_D_1980_2010_|.npy',npyFile)
        data = np.load(pathName)
        for i in range(6,10):
            path = 'G:\Phase2Parts\\' + pathSplit[1] + 'day'+ str(i+1) + '.csv'
            dataPart = data[i:11300+i:]
            np.savetxt(path, dataPart.astype(np.float), delimiter=",")
        


# In[3]:




# In[6]:

def SAOLA(data,label):
    dfList = pd.DataFrame()
    for csvFile in glob.glob(data):
        print csvFile
        df = pd.read_csv(csvFile,header=None)
        
        for i in df:
            corrC = df.iloc[:,i].corr(label.iloc[:,0])
            zTrans = np.arctanh(corrC)
            zScore = zTrans*np.sqrt(11300 - 3)
            if zScore < 1.96:
                continue
            else:
                df3 = df.iloc[:,i]
                if dfList.empty:
                    dfList =pd.concat([dfList, df3], axis=1,ignore_index = True)
                else:
                    df3, dfList = correlationF(df3,dfList)
    return dfList


# In[7]:

def correlationF(df3,dfList):
    label = pd.DataFrame(target)
    i = 0
    while i < len(dfList.columns):
        corr_yc = dfList.iloc[:,i].corr(label.iloc[:,0])
        xTrans_yc=np.arctanh(corr_yc)
        Zy_c= xTrans_yc*np.sqrt(11300-3)
        
        corr_fc = df3.corr(label.iloc[:,0])
        xTrans_fc=np.arctanh(corr_fc)
        Zf_c= xTrans_fc*np.sqrt(11300-3)
       
        corr_fy = dfList.iloc[:,i].corr(df3)
        xTrans_fy=np.arctanh(corr_fy)
        Zf_y= xTrans_fy*np.sqrt(11300-3)

        if Zy_c > Zf_c and Zf_y >=Zf_c:
            return df3,dfList
        if Zf_c > Zy_c and Zf_y >=Zy_c:
            dfList = dfList.drop(dfList.columns[i], axis=1)
            i=0
        else:
            i= i+1
    dfList =pd.concat([dfList, df3], axis=1,ignore_index=True)
    return df3,dfList        
        
    


# In[8]:

dfList = pd.DataFrame()
data = "G:/Phase2Parts/*.csv"
dfList = correlationC(data,label)


# In[9]:




# In[ ]:

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
plt.figure(figsize=(12,6))

map = Basemap(projection='robin',lon_0=360)

map.drawcoastlines()

x, y = map([280,80],[2.5,27.5])

map.scatter(x, y,color = 'r',marker = '+',s = 100) 
plt.show()
plt.clf()

