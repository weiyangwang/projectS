import numpy as np
import csv
import plotly
import plotly.graph_objs as go

plotly.offline.init_notebook_mode() # run at the start of every notebook

import pandas as pd

filename = 'XD edit suvery input template.xlsx - Cleaned Data.csv'

reader = csv.DictReader(open(filename,'r',encoding="utf8"),delimiter=',')
dataf=np.array([[line[k] for k in reader.fieldnames] for line in reader])

try:
    for index, x in np.ndenumerate(dataf):
        if not x.isnumeric():
                dataf[index] = np.nan
except ValueError:
    print("ERROR!!!")

dataf = dataf.astype(float)

df = pd.DataFrame(dataf, columns=reader.fieldnames)
correlf = df.corr()
np.fill_diagonal(correlf.values, 0)

datacorrelf = [
    go.Surface(
        z=np.array(correlf)
    )
]
layoutcorrelf = go.Layout(
    title='Correlations between Qns',
    autosize=False,
    width=1000,
    height=1000,
    margin=dict(
        l=65,
        r=50,
        b=65,
        t=90
    ),
    xaxis = dict(
            ticktext = reader.fieldnames,
            tickvals = [i for i, val in enumerate(reader.fieldnames)],
            tickangle = 45,
            showticklabels = True
    ),
    yaxis = dict(
            ticktext = reader.fieldnames,
            tickvals = [i for i, val in enumerate(reader.fieldnames)],
            tickangle = 45,
            showticklabels = True
    )
)
figf = go.Figure(data=datacorrelf, layout=layoutcorrelf)
plotly.offline.plot(figf, filename='correlation2D.html')