import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np

# Sample data
np.random.seed(42)
data = np.random.randn(100)

# Create a sample histogram
fig = px.histogram(data, nbins=20, title='サンプルグラフ')

# Statistics
mean = np.mean(data)
std = np.std(data)
median = np.median(data)
min_val = np.min(data)
max_val = np.max(data)

app = dash.Dash(__name__)

app.layout = html.Div([
    # Left side statistics
    html.Div([
        html.H3('基本統計量'),
        html.P(f'平均: {mean:.2f}'),
        html.P(f'標準偏差: {std:.2f}'),
        html.P(f'中央値: {median:.2f}'),
        html.P(f'最小値: {min_val:.2f}'),
        html.P(f'最大値: {max_val:.2f}')
    ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    # Right side graph
    html.Div([
        dcc.Graph(figure=fig)
    ], style={'width': '58%', 'display': 'inline-block'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
