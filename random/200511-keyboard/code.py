from pydub import AudioSegment
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

nz = AudioSegment.from_file("./NiZ_Plum_66_typing.m4a")
mbp = AudioSegment.from_file("./MBP_13_2017_typing_cropped.m4a")
ab = AudioSegment.from_file("./AmazonBasics_typing_cropped.m4a")

def make_random_subset(audio, subset=0.2):
    max_length = len(nz)
    interval = subset * max_length
    start = np.random.randint(0, int(max_length) - int(interval))
    return start, interval

def bootstrap(audio, N=100, subset=0.2):
    rms = []
    for i in range(N):
        start, interval = make_random_subset(audio, subset=subset)
        rms.append(audio[start:start+interval].rms)
    return rms

nz_rms = bootstrap(nz)
ab_rms = bootstrap(ab)
mbp_rms = bootstrap(mbp)

df = pd.DataFrame({'NiZ Plum 66':nz_rms, 'AmazonBasics':ab_rms, 'MBP 13':mbp_rms}).unstack().reset_index()
df.columns = ['Keyboard', 'Trials', 'Loudness (RMS)']

fig = px.box(df, y='Loudness (RMS)', color='Keyboard', hover_data=['Keyboard'])
fig.update_layout(width=700, height=500)
fig.write_html('./bootstrap_loudness.html')

dft = pd.read_csv('./typing_test.csv')
fig = make_subplots(rows=1, cols=2, subplot_titles=("Words per min (WPM)", "Accuracy (%)"))
for i, c in zip(['NiZ Plum 66', 'AmazonBasics', 'MBP 13'], px.colors.qualitative.Plotly):
    for j in ['YSX', 'SS']:
        subject = dft.Keyboard.isin([i]) * dft.Subject.isin([j])
        fig.add_trace(go.Box(
            y=dft.loc[subject, 'WPM'],
            name=i + ' ('+j+')',
            boxpoints=False, # no data points
            marker_color=c,
        ), row=1, col=1)
        fig.add_trace(go.Box(
            y=dft.loc[subject, 'Accuracy (%)'],
            name=i + ' ('+j+')',
            boxpoints=False, # no data points
            marker_color=c,
            showlegend=False
        ), row=1, col=2)
fig.update_layout(width=700, height=500)
fig.write_html('./typing_test.html')

fig = make_subplots(rows=1, cols=2, subplot_titles=("YSX", "SS"),
        x_title='Words per min (WPM)', y_title='Accuracy (%)')
for i, c in zip(['NiZ Plum 66', 'AmazonBasics', 'MBP 13'], px.colors.qualitative.Plotly):
    ysx = dft.Keyboard.isin([i]) * dft.Subject.isin(['YSX'])
    ss = dft.Keyboard.isin([i]) * dft.Subject.isin(['SS'])
    fig.add_trace(go.Scatter(
        y=dft.loc[ysx, 'Accuracy (%)'],
        x=dft.loc[ysx, 'WPM'],
        mode='markers',
        marker=dict(size=10),
        name=i,
        marker_color=c,
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        y=dft.loc[ss, 'Accuracy (%)'],
        x=dft.loc[ss, 'WPM'],
        mode='markers',
        name=i,
        marker_color=c,
        marker=dict(size=10),
        showlegend=False
    ), row=1, col=2)
fig.update_layout(width=700, height=400)
fig.write_html('./typing_test_correlation.html')

