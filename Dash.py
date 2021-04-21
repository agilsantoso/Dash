import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("Data_Harian_Kasus_per_Provinsi_COVID-19_Indonesia.csv")
df = df.drop("Unnamed: 7", axis=1)
df = df.drop("Unnamed: 8", axis=1)
df = df.drop('X, Y', axis=1)

map_df = gpd.read_file('idn_admbnda_adm1_bps_20200401.shp')
map_df = map_df.replace('Dki Jakarta','DKI Jakarta')

merged = map_df.set_index('ADM1_EN').join(df.set_index('Provinsi'))

variable = 'Kasus_Posi'
vmin = merged['Kasus_Posi'].min()
vmax = merged['Kasus_Posi'].max()

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
fig.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')
ax.margins(0)
ax.apply_aspect()
bbox = ax.get_window_extent().inverse_transformed(fig.transFigure)
w,h = fig.get_size_inches()
fig.set_size_inches(w*bbox.width, h*bbox.height)
merged.plot(column=variable, cmap='Reds', linewidth=0.3, ax=ax, edgecolor='0.8')
cbar = fig.colorbar(plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax)), orientation="vertical", aspect=40, shrink=0.5, pad=0.03)
cbar.ax.tick_params(labelsize=6)
ax.set_title('Persebaran Covid-19 tiap Provinsi di Indonesia', \
              fontdict={'fontsize': '12',
                        'fontweight' : '3'})
ax.annotate('Sumber: https://indonesia-covid-19.mathdro.id/api/',
           xy=(0.1, .1), xycoords='figure fraction',
           horizontalalignment='left', verticalalignment='bottom',
           fontsize=7, color='#555555')


app.layout = html.Div(children=[
    html.H1(children='Data Kasus Positif Covid-19 di Indonesia'),

    html.Div(children='''
        Data Kasus Positif Tiap Provinsi
    '''),
    
    dcc.Graph(
        id='example-graph',
        figure=fig)
])

app.run_server(debug=True)