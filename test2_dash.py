# 必要なライブラリをインポート
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# データの読み込みと前処理
nikkei = pd.read_csv('nikkei.csv', parse_dates=['datetime'])
nikkei = nikkei[nikkei['datetime'] >= '2011-01-04']
nikkei['Return'] = nikkei['close'].diff()

# 基本統計量の計算
mean_return = nikkei['Return'].mean()
std_return = nikkei['Return'].std()
count_data = len(nikkei)
start_date = nikkei['datetime'].min().strftime('%Y-%m-%d')
end_date = nikkei['datetime'].max().strftime('%Y-%m-%d')

# Dashアプリケーションの初期化
app = dash.Dash(__name__)

# Dashアプリケーションのレイアウト

app.layout = html.Div([
    # Left side statistics
    html.Div([
        html.H3('基本統計量'),
        html.P(f'平均: {mean_return:.2f}'),
        html.P(f'標準偏差: {std_return:.2f}'),
        html.P(f'データ点数: {count_data:.2f}'),
        html.P(f"Date Range: {start_date} to {end_date}")
    ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    # Right content
    html.Div([
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Time Series Plot', value='tab-1'),
            dcc.Tab(label='Histogram', value='tab-2'),
            dcc.Tab(label='Candlestick Chart', value='tab-3'),
            dcc.Tab(label='Scatter Plot', value='tab-4'),
        ]),
        html.Div(id='tabs-content')
    ], #style={'width': '58%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px'})
    style={'width': '60%', 'display': 'inline-block','vertical-align': 'top'})
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return dcc.Graph(
            figure={
                'data': [
                    go.Scatter(x=nikkei['datetime'], y=nikkei['close'], name='Close', line=dict(color='teal')),
                    go.Scatter(x=nikkei['datetime'], y=nikkei['open'], name='Open', line=dict(color='teal', dash='dash'))
                ],
                'layout': go.Layout(title='Nikkei 225 Open & Close Prices Over Time', xaxis=dict(title='Date'), yaxis=dict(title='Price'))
            }
        )
    elif tab == 'tab-2':
        return dcc.Graph(
            figure={
                'data': [go.Histogram(x=nikkei['Return'].dropna(), marker=dict(color='teal'))],
                'layout': go.Layout(title='Distribution of Nikkei 225 Returns', xaxis=dict(title='Return'), yaxis=dict(title='Frequency'))
            }
        )
    elif tab == 'tab-3':
        ohlc = nikkei.resample('D', on='datetime').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last'
        }).reset_index()
        return dcc.Graph(
            figure={
                'data': [go.Candlestick(x=ohlc['datetime'],
                                        open=ohlc['open'],
                                        high=ohlc['high'],
                                        low=ohlc['low'],
                                        close=ohlc['close'],
                                        increasing_line_color='teal',
                                        decreasing_line_color='teal')],
                'layout': go.Layout(title='Nikkei 225 Candlestick Chart', xaxis=dict(title='Date'), yaxis=dict(title='Price'))
            }
        )
    elif tab == 'tab-4':
        return dcc.Graph(
            figure={
                'data': [go.Scatter(x=nikkei['Return'], y=nikkei['volume'], mode='markers', marker=dict(color='teal'))],
                'layout': go.Layout(title='Scatter Plot of Returns vs. Volume', xaxis=dict(title='Return'), yaxis=dict(title='Volume'))
            }
        )

if __name__ == '__main__':
    app.run_server(debug=True)
