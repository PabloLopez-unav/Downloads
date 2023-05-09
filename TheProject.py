import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import plotly.express as px
import serial    
import re         
import time       
 
X_s1=deque(maxlen=10)
X_s2=deque(maxlen=10)
X_s3=deque(maxlen=10)
X_s4=deque(maxlen=10)
X_s1_list = deque(maxlen=10)
X_s2_list = deque(maxlen=10)
X_s3_list = deque(maxlen=10)
X_s4_list = deque(maxlen=10)


ser = serial.Serial() 
ser.port = 'COM3'      
ser.baudrate = 9600    


ser.open()

if ser.isOpen():
        print("Port " + ser.port + " opened successfully")

serial_read_state = True
def serialRead(ser): 
    global serial_read_state
    if (serial_read_state==True):  
        serial_read_state=False
        message = ser.readline() 
        print(message)
        data_string = message.decode("utf-8") 
        print(data_string)
        data = re.findall('S1=([\d\.]+),S2=([\d\.]+),S3=([\d\.]+),S4=([\d\.]+)', data_string) 
        data = [list(map(float, tup)) for tup in data]
        print(data) 
        serial_read_state=True
    else:
        time.sleep(0.1)
        data=serialRead(ser)
    return data 

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#f8f9fa",
        "fontFamily": "Helvetica",
        "height": "100vh",
        "padding": "1rem",
        "color": "#343a40",
    },
    children=[
        
        html.Div(
            style={"textAlign": "center", "marginBottom": "2rem"},
            children=[
                html.H1(
                    "Smart Light System",
                    style={"fontSize": "3rem", "marginBottom": "0.5rem"},
                ),
                html.P("Control your light expenses with ease!"),
            ],
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "center"},
            children=[
                html.Div(
                    style={"marginRight": "2rem"},
                    children=[
                        html.H2("Floor number 1"),
                        dcc.Graph(
                            id="live-graph",
                            animate=True,
                            style={"height": "250px", "width": "600px", "marginBottom": "1rem"},
                        ),
                        dcc.Interval(
                            id="graph-update",
                            interval=2000,  
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.H2("Floor number 2"),
                        dcc.Graph(
                            id="live-graph2",
                            animate=True,
                            style={"height": "250px", "width": "600px", "marginBottom": "1rem"},
                        ),
                        dcc.Interval(
                            id="graph-update2",
                            interval=2000,  
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "center"},
            children=[
                html.Div(
                    style={"marginRight": "2rem"},
                    children=[
                        html.H2("Floor number 3"),
                        dcc.Graph(
                            id="live-graph3",
                            animate=True,
                            style={"height": "250px","width": "600px", "marginBottom": "1rem"},
                        ),
                        dcc.Interval(
                            id="graph-update3",
                            interval=2000, 
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.H2("Floor number 4"),
                        dcc.Graph(
                            id="live-graph4",
                            animate=True,
                            style={"height": "250px", "width": "600px", "marginBottom": "1rem"},
                        ),
                        dcc.Interval(
                            id="graph-update4",
                            interval=2000, 
                        ),
                    ],
                ),
            ],
        ),

        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "marginBottom": "2rem",
            },
            children=[
                html.Div(
                    children=[
                        html.H2("Expenses before SLS"),
                        html.H3("140 €/hour"),
                    ]
                ),
                html.Div(
                    children=[
                        html.H2("Real Time Cost with SLS"),
                        html.H3(id="live-text"),
                        dcc.Interval(
                            id="interval-component",
                            interval=2000, 
                            n_intervals=0
        ),
    
    ])
        
    ])
])



@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter1(input_data):
    if len(X_s1) == 0:
        X_s1.append(1)
    else:
        X_s1.append(X_s1[-1] + 1)
    xa = serialRead(ser)
    LED1 = xa[0][0]
    X_s1_list.append(LED1)
    data = go.Scatter(
        x=list(X_s1),
        y=list(X_s1_list),
        name='Scatter',
        mode='lines+markers'
    )
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X_s1), len(X_s1_list)]),  
                                                yaxis=dict(range=[0 ,1.5]),
                                                xaxis_title='Time since switch on',
                                                yaxis_title='Light it or not')}


@app.callback(
    Output('live-graph2', 'figure'),
    [Input('graph-update2', 'n_intervals')]
)
def update_graph_scatter2(input_data):
    if len(X_s2) == 0:
        X_s2.append(1)
    else:
        X_s2.append(X_s2[-1] + 1)
    xx = serialRead(ser)
    LED2 = xx[0][1]
    X_s2_list.append(LED2)
    data = go.Scatter(
        x=list(X_s2),
        y=list(X_s2_list),
        name='Scatter',
        mode='lines+markers'
    )
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X_s2),max(X_s2)]),  
                                                yaxis=dict(range=[0 ,1.5]),
                                                xaxis_title='Time since switch on',
                                                yaxis_title='Light it or not')} 


@app.callback(
    Output('live-graph3', 'figure'),
    [Input('graph-update3', 'n_intervals')]
)
def update_graph_scatter3(input_data):
    if len(X_s3) == 0:
        X_s3.append(1)
    else:
        X_s3.append(X_s3[-1] + 1)
    xe = serialRead(ser)
    LED3 = xe[0][2]
    X_s3_list.append(LED3)
    data = go.Scatter(
        x=list(X_s3),
        y=list(X_s3_list),
        name='Scatter',
        mode='lines+markers'
    )
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X_s3),max(X_s3)]),   # x-> time step range
                                                yaxis=dict(range=[0 ,1.5]),
                                                xaxis_title='Time since switch on',
                                                yaxis_title='Light it or not')} # y-> temp range


@app.callback(
    Output('live-graph4', 'figure'),
    [Input('graph-update4', 'n_intervals')]
)
def update_graph_scatter4(input_data):
    if len(X_s4) == 0:
        X_s4.append(1)
    else:
        X_s4.append(X_s4[-1] + 1)
    xo = serialRead(ser)
    LED4 = xo[0][3]
    X_s4_list.append(LED4)
    data = go.Scatter(
        x=list(X_s4),
        y=list(X_s4_list),
        name='Scatter',
        mode='lines+markers'
    )
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X_s4),max(X_s4)]),   
                                                yaxis=dict(range=[0 ,1.5]),
                                                xaxis_title='Time since switch on',
                                                yaxis_title='Light it or not')} 


@app.callback(
    dash.dependencies.Output('live-text', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_text(input_data):
    euro = serialRead(ser)
    vok = euro[0][0] + euro[0][1] + euro[0][2] + euro[0][3]
    vok2 = vok*35
    vok3 = str(vok2) + " €/hour"
    print(vok3)
    return vok3
    

if __name__ == '__main__':
    app.run_server(port=8044, debug=False) 