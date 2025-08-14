import json
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ctx, dcc, html, State
from .home import get_sidebar

def layout():
    # banner
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://cdn.rcsb.org/news/2020/zoom_6lu7_crystal.jpg', alt='OPC UA Dashboard', className="banner-image"),
                html.Div([
                    html.H2("OPC UA Communication Dashboard"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    # Main Tabs (full width)
    main_tabs = dbc.Tabs([
        # Server Connection Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Server Connection", className="card-title"),
                            dbc.Input(id='server-name', placeholder="Server name", className="mb-3"),
                            dbc.Input(id='endpoint-url', placeholder="Endpoint URL (e.g., opc.tcp://localhost:4840)", className="mb-3"),
                            dbc.Row([
                                dbc.Col(dbc.Input(id='username', placeholder="Username", className="mb-3"), width=6),
                                dbc.Col(dbc.Input(id='password', type="password", placeholder="Password", className="mb-3"), width=6),
                            ]),
                            dbc.Button(
                                "Connect",
                                id='connect-server',
                                color="primary",
                                className="w-100 mb-3",
                                size="lg"
                            ),
                            html.Div(id='connection-status'),
                            dcc.Store(id='connection-store', data={'connected': False})
                        ])
                    ])
                ], width=8, className="mx-auto")
            ], className="mt-4")
        ], label="Server Connection", tab_id="tab-server"),
        
        # Client Connection Tab (initially disabled)
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("OPC UA Client", className="card-title"),
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Terminal"),
                                    html.Div(id='terminal-output', className="terminal-window bg-dark text-light p-3 mb-3", style={'height': '300px', 'overflowY': 'auto'}),
                                    dbc.InputGroup([
                                        dbc.Input(id='terminal-input', placeholder="Enter OPC UA command..."),
                                        dbc.Button("Send", id='send-command', color="primary"),
                                    ]),
                                ], md=6),
                                
                                dbc.Col([
                                    html.H5("Node Browser"),
                                    html.Div(id='node-browser', className="node-browser-window bg-light p-3", style={'height': '300px', 'overflowY': 'auto'}),
                                ], md=6)
                            ])
                        ])
                    ])
                ], width=12)
            ])
        ], label="Client Connection", tab_id="tab-client", disabled=True, className="disabled-tab"),
        
        # Video Configuration Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Video Configuration", className="card-title"),
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Camera Controls"),
                                    dbc.Label("Pitch", className="mt-2"),
                                    dcc.Slider(id='camera-pitch', min=-90, max=90, value=0, step=1, marks=None, tooltip={"placement": "bottom"}),
                                    dbc.Label("Yaw", className="mt-3"),
                                    dcc.Slider(id='camera-yaw', min=-180, max=180, value=0, step=1, marks=None, tooltip={"placement": "bottom"}),
                                ], md=4),
                                
                                dbc.Col([
                                    html.H5("Video Sources"),
                                    dbc.Tabs([
                                        dbc.Tab([
                                            dbc.Input(id='video-url', placeholder="RTSP/HTTP video URL", className="mb-3"),
                                            dbc.Button("Connect to Stream", id='connect-stream', color="primary", className="w-100"),
                                        ], label="Network Stream"),
                                        
                                        dbc.Tab([
                                            dcc.Upload(
                                                id='upload-video',
                                                children=html.Div([
                                                    'Drag and drop video file or ',
                                                    html.A('select file')
                                                ]),
                                                className="upload-box p-5 text-center",
                                                style={'border': '2px dashed #ccc', 'borderRadius': '5px'}
                                            ),
                                        ], label="File Upload")
                                    ]),
                                    html.Div(id='video-preview-container', className="mt-3")
                                ], md=8)
                            ])
                        ])
                    ])
                ], width=12)
            ])
        ], label="Video Configuration", tab_id="tab-video"),
        
        # Subscribed Nodes Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Node Subscriptions", className="card-title"),
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Subscribe to Nodes"),
                                    dbc.InputGroup([
                                        dbc.Input(id='node-id', placeholder="Node ID (e.g., ns=3;i=1001)"),
                                        dbc.Button("Subscribe", id='subscribe-node', color="primary"),
                                    ], className="mb-3"),
                                    
                                    dbc.Input(id='level-node', placeholder="Level Node ID", className="mb-2"),
                                    dbc.Input(id='confidence-node', placeholder="Confidence Node ID", className="mb-2"),
                                    dbc.Input(id='setpoint-node', placeholder="Setpoint Node ID", className="mb-2"),
                                    dbc.Input(id='switch-node', placeholder="Switch Node ID", className="mb-2"),
                                    dbc.Button("Subscribe All", id='subscribe-nodes', color="primary", className="w-100 mb-3"),
                                    
                                    html.Div(id='subscription-status'),
                                    html.Div(id='subscription-errors', className="text-danger")
                                ], md=4),
                                
                                dbc.Col([
                                    html.H5("Current Subscriptions"),
                                    html.Div(id='subscriptions-table-container', style={'height': '300px', 'overflowY': 'auto'}),
                                    dbc.Table(id='subscriptions-table', bordered=True, hover=True, responsive=True)
                                ], md=4),
                                
                                dbc.Col([
                                    html.H5("Node Value Visualization"),
                                    dcc.Graph(
                                        id='node-graph',
                                        config={'displayModeBar': True},
                                        style={'height': '400px'}
                                    ),
                                    dcc.Interval(
                                        id='graph-update-interval',
                                        interval=1*1000,  # in milliseconds
                                        n_intervals=0
                                    )
                                ], md=4)
                            ])
                        ])
                    ])
                ], width=12)
            ])
        ], label="Subscribed Nodes", tab_id="tab-nodes")
    ], id="main-tabs", active_tab="tab-server", className="mb-4")

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(main_tabs, fluid=True)
        ], className='content')
    ]

    return layout

# Callbacks
@dash.callback(
    Output('connection-status', 'children'),
    Output('connection-store', 'data'),
    Output('tab-client', 'disabled'),
    Output('main-tabs', 'active_tab'),
    Input('connect-server', 'n_clicks'),
    State('server-name', 'value'),
    State('endpoint-url', 'value'),
    State('username', 'value'),
    State('password', 'value'),
    prevent_initial_call=True
)
def connect_to_server(n_clicks, name, url, username, password):
    if not url:
        return dbc.Alert("Endpoint URL is required", color="danger"), dash.no_update, True, dash.no_update
    
    try:
        # Simulate connection - replace with actual OPC UA client code
        connection_status = {
            'connected': True,
            'server_name': name or "Unnamed Server",
            'endpoint': url,
            'timestamp': dash.callback_context.timestamp
        }
        
        status = dbc.Alert(
            [
                html.I(className="bi bi-check-circle-fill me-2"),
                f"Connected to {name or 'server'} at {url}"
            ],
            color="success",
            className="d-flex align-items-center"
        )
        
        # Enable client tab and switch to it
        return status, connection_status, False, "tab-client"
    
    except Exception as e:
        return dbc.Alert(f"Connection failed: {str(e)}", color="danger"), {'connected': False}, True, dash.no_update

@dash.callback(
    Output('subscription-status', 'children'),
    Output('subscriptions-table', 'children'),
    Input('subscribe-node', 'n_clicks'),
    Input('subscribe-nodes', 'n_clicks'),
    State('node-id', 'value'),
    State('level-node', 'value'),
    State('confidence-node', 'value'),
    State('setpoint-node', 'value'),
    State('switch-node', 'value'),
    State('connection-store', 'data'),
    prevent_initial_call=True
)
def manage_subscriptions(node_click, nodes_click, node_id, level, confidence, setpoint, switch, connection):
    ctx = dash.callback_context
    if not connection.get('connected'):
        return dbc.Alert("Not connected to server", color="danger"), dash.no_update
    
    if not ctx.triggered:
        return dash.no_update, dash.no_update
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == 'subscribe-node' and node_id:
        # Single node subscription
        new_row = dbc.Tr([
            dbc.Td(node_id),
            dbc.Td("Subscribed"),
            dbc.Td("--"),
            dbc.Td(dbc.Button("Unsubscribe", color="danger", size="sm"))
        ])
        
        # Update table - in a real app, you'd maintain state properly
        return dbc.Alert(f"Subscribed to node {node_id}", color="success"), new_row
    
    elif triggered_id == 'subscribe-nodes':
        # Multi-node subscription
        nodes = []
        if level: nodes.append(("Level", level))
        if confidence: nodes.append(("Confidence", confidence))
        if setpoint: nodes.append(("Setpoint", setpoint))
        if switch: nodes.append(("Switch", switch))
        
        if not nodes:
            return dbc.Alert("No nodes specified", color="warning"), dash.no_update
        
        rows = []
        for node_type, node_id in nodes:
            rows.append(dbc.Tr([
                dbc.Td(node_id),
                dbc.Td(node_type),
                dbc.Td("Subscribed"),
                dbc.Td("--"),
                dbc.Td(dbc.Button("Unsubscribe", color="danger", size="sm"))
            ]))
        
        table = dbc.Table(
            [html.Thead(html.Tr([html.Th("Node ID"), html.Th("Type"), html.Th("Status"), html.Th("Value"), html.Th("Action")]))] + rows,
            bordered=True, hover=True, responsive=True
        )
        
        return dbc.Alert(f"Subscribed to {len(nodes)} nodes", color="success"), table
    
    return dash.no_update, dash.no_update

@dash.callback(
    Output('node-graph', 'figure'),
    Input('graph-update-interval', 'n_intervals'),
    State('subscriptions-table', 'children'),
    State('connection-store', 'data')
)
def update_graph(n_intervals, subscriptions, connection):
    if not connection.get('connected'):
        return dash.no_update
    
    # In a real app, you would get actual node values here
    import plotly.graph_objects as go
    from random import random
    
    fig = go.Figure()
    
    # Simulate some data
    if subscriptions and isinstance(subscriptions, list) and len(subscriptions) > 1:
        for row in subscriptions[1:]:  # Skip header
            node_id = row.props['children'][0].props['children']
            fig.add_trace(go.Scatter(
                x=list(range(10)),
                y=[random() * 100 for _ in range(10)],
                name=node_id,
                mode='lines+markers'
            ))
    
    fig.update_layout(
        margin={'l': 40, 'r': 10, 't': 30, 'b': 30},
        showlegend=True,
        uirevision='constant'  # Preserves UI state during updates
    )
    
    return fig