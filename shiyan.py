import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# 初始化 Dash 应用
app = dash.Dash(__name__)

# 示例数据生成函数
def generate_data():
    timestamps = pd.date_range(start='2024-06-01 00:00:00', periods=100, freq='min')
    values = np.random.randn(100).cumsum()
    return pd.DataFrame({'timestamp': timestamps, 'value': values})

# 初始数据
df = generate_data()

# Dash 应用布局
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0) # 每秒更新一次
])

# 回调函数更新图表
@app.callback(Output('live-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    new_data = generate_data() # 模拟获取新数据
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=new_data['timestamp'], y=new_data['value'], mode='lines+markers'))
    fig.update_layout(title='Real-time Data Visualization', xaxis_title='Time', yaxis_title='Value')
    return fig

if __name__ == '__main__':
    app.run(debug=True)