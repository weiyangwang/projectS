import numpy as np
import csv
import plotly
import plotly.graph_objs as go
import math
from scipy import stats
import os

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
corr_plot_url = plotly.offline.plot(figf, filename='correlation2D', auto_open=False)
print(corr_plot_url)

#qns = np.array([[51,59]])
#qns = np.vstack([qns,[[i,72] for i in range(43,51)]])
#qns = np.vstack([qns,[[i,67] for i in range(51,63)]])
#qns = np.vstack([qns,[[i,68] for i in range(51,63)]])
#qns = np.vstack([qns,[[i,69] for i in range(51,63)]])
#qns = np.vstack([qns,[[i,70] for i in range(51,63)]])
qns = np.array([[i,71] for i in range(51,63)])
grid = (math.floor(qns.shape[0]/2),qns.shape[0]%2)
figarr = plotly.tools.make_subplots(rows=grid[0]+grid[1], cols=2, print_grid=True, horizontal_spacing= 0.1, vertical_spacing= 0.1, 
                                    shared_yaxes=False, shared_xaxes=False)

annotations = []
for i in range(0,qns.shape[0]):
    mask = ~np.isnan(dataf[:,qns[i,0]]) & ~np.isnan(dataf[:,qns[i,1]])
    slope, intercept, r_value, p_value, std_err = stats.linregress(dataf[mask,qns[i,0]],dataf[mask,qns[i,1]]*100/4)
    print(qns[i,0], qns[i,1], "stats.linregress (slope,r): ", slope,r_value)
    print(correlf.iat(qns[i,0], qns[i,1]))
    line = slope*dataf[mask,qns[i,0]]+intercept
    #A = np.vstack([data[:,qns[i,0]], np.ones(len(data[:,qns[i,0]]))]).T
    #m, c = np.linalg.lstsq(A, data[:,qns[i,1]])[0]
    #ypred = [m*ix+c for ix in data[:,qns[i,0]]]
    trace0 = go.Scatter(
        x=dataf[mask,qns[i,0]], y=line, mode='lines', name='OLS'+str(i)+' r='+str(round(r_value, 4))+' m='+str(round(slope, 4)),
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 3),
        showlegend = True
    )
    trace1 = go.Scatter(
        x=dataf[mask,qns[i,0]], y=dataf[mask,qns[i,1]]*100/4, mode='markers', name='Points'+str(i),
        marker=dict(color='rgb(102,0,0)', size=5, opacity=0.4),
        showlegend = True
    )
    trace2 = go.Histogram2dcontour(
        x=dataf[mask,qns[i,0]], y=dataf[mask,qns[i,1]]*100/4, name='density', ncontours=20,
        colorscale='Hot', reversescale=True, showscale=False,
        showlegend = True
    )
    trace3 = go.Histogram(
        x=dataf[mask,qns[i,0]], name= 'Q'+str(qns[i,0])+' density',
        marker=dict(color='rgb(102,0,0)'),
        yaxis='y2'
    )
    trace4 = go.Histogram(
        y=dataf[mask,qns[i,1]], name='Q'+str(qns[i,1])+' density', marker=dict(color='rgb(102,0,0)'),
        xaxis='x2'
    )
   
    figarr.append_trace(trace0, int((i/2)+1), (i%2)+1)
    figarr.append_trace(trace1, int((i/2)+1), (i%2)+1)
    figarr.append_trace(trace2, int((i/2)+1), (i%2)+1)   
    figarr['layout']['xaxis{}'.format(i+1)].update(title='Qn: '+reader.fieldnames[qns[i,0]])
    figarr['layout']['yaxis{}'.format(i+1)].update(title='Qn: '+reader.fieldnames[qns[i,1]])
   
figarr['layout'].update(height=500*(grid[0]+grid[1]), width=500*2, title='Correlations')
multi_plot_url = plotly.offline.plot(figarr, filename='multiplot', auto_open=False)
print(multi_plot_url)

html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Project Share: Correlations between survey questions</h1>

        <!-- *** Section 1 *** --->
        <h2>Section 1: Overall correlation between all each question pair</h2>
        <iframe width="1000" height="1000" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + corr_plot_url + '''?width=800&height=1000"></iframe>
        <p>Pearson product-moment correlation between each pair of questions. \
        The xy-plane are the question pairs while the z-axis is the strength of the correlation.</p>
        
        <!-- *** Section 2 *** --->
        <h2>Section 2: Scatter plots and correlations between interesting question pairs</h2>
        <iframe width="1000" height="3000" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + multi_plot_url + '''?width=1000&height=3000"></iframe>
        <p>Scatter and contour plots between each interesting question pair. \
        A ordinary least squares (OLS) fit is made to quantify the strength of the correlation by the gradient m.</p>
    </body>
</html>'''

print(multi_plot_url.replace('\\', '/')[7:])

f = open('report.html','w')
f.write(html_string)
f.close()