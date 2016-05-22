#!/usr/bin/python

import numpy as np
import csv, sys
import matplotlib.pyplot as plt

filename = 'XD edit suvery input template.xlsx - Cleaned Data.csv'

reader = csv.reader(open(filename,'r',encoding="utf8"),delimiter=',')
data=np.array([line for line in reader])

#print data[2049,151]
np.set_printoptions(threshold=np.nan)

#data[data=='#N/A'] = 0
#data[data=='NA'] = 0
#data[data==''] = 0

try:
    for index, x in np.ndenumerate(data):
        if not x.isnumeric():
                data[index] = 0
except ValueError:
    print("ERROR!!!")

data = data.astype(float)
    
correl = np.array([[np.corrcoef(data[:,i],data[:,j])[0,1] for i in range(len(data[0]))] for j in range(len(data[0]))])
correl = np.around(correl, decimals=2)
correl[np.isnan(correl)] = 0
for index, x in np.ndenumerate(correl):
    if index[0]==index[1]:
        correl[index] = 0

heatmap = plt.pcolor(correl,vmin=0,vmax=1)
plt.colorbar(heatmap)
plt.show()