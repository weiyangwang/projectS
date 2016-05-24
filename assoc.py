import numpy as np
import csv, sys
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go

plotly.offline.init_notebook_mode() # run at the start of every notebook

import pandas as pd

filename = 'XD edit suvery input template.xlsx - Cleaned Data.csv'

reader = csv.reader(open(filename,'r',encoding="utf8"),delimiter=',')
data=np.array([line for line in reader])

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

data = [
    go.Surface(
        z=correl
    )
]
layout = go.Layout(
    title='Correlations between Qns',
    autosize=False,
    width=1000,
    height=1000,
    margin=dict(
        l=65,
        r=50,
        b=65,
        t=90
    )
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig)