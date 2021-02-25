import json

import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d

EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
TITLE = "LLDP Network Visualiser"

with open('data/net.json', 'r') as f:
    data = json.load(f)

app = dash.Dash(
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS,
    title=TITLE,
)
server = app.server

styles = {
    'json-output': {
        'overflow-y': 'scroll',
        'height': 'calc(25% - 25px)',
        'border': 'thin lightgrey solid'
    },
    'tab': {'height': 'calc(98vh - 115px)'}
}

app.layout = html.Div(className="container", children=[
    html.H1(
        children=TITLE,
        className="row",
        style={'textAlign': "center"}
    ),
    html.Button('Reset', id='bt-reset'),
    html.Div(className='row', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=data,
            layout={
                'name': 'breadthfirst',
            },
            style={
                'height': '750px',
                'width': '100%'
            },
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {'content': 'data(label)'}
                },
                # {
                #     'selector': 'edge',
                #     'style': {'content': 'data(value)'}
                # },
                {
                    'selector': '.dashed',
                    'style': {'line-style': 'dashed'}
                }
            ],
        )
    ]),
    dcc.Dropdown(
        id='dropdown-callbacks-1',
        value='grid',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in ['grid', 'random', 'circle', 'cose', 'concentric', 'breadthfirst']
        ]
    ),
    html.Div(className='row', children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='Tap Objects', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Node Object JSON:'),
                    html.Pre(
                        id='tap-node-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Object JSON:'),
                    html.Pre(
                        id='tap-edge-json-output',
                        style=styles['json-output']
                    )
                ])
            ]),
            dcc.Tab(label='Tap Data', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Node Data JSON:'),
                    html.Pre(
                        id='tap-node-data-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Data JSON:'),
                    html.Pre(
                        id='tap-edge-data-json-output',
                        style=styles['json-output']
                    )
                ])
            ]),

            dcc.Tab(label='Mouseover Data', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Node Data JSON:'),
                    html.Pre(
                        id='mouseover-node-data-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Data JSON:'),
                    html.Pre(
                        id='mouseover-edge-data-json-output',
                        style=styles['json-output']
                    )
                ])
            ]),
            dcc.Tab(label='Selected Data', children=[
                html.Div(style=styles['tab'], children=[
                    html.P('Node Data JSON:'),
                    html.Pre(
                        id='selected-node-data-json-output',
                        style=styles['json-output']
                    ),
                    html.P('Edge Data JSON:'),
                    html.Pre(
                        id='selected-edge-data-json-output',
                        style=styles['json-output']
                    )
                ])
            ])
        ]),
    ]),
    html.Div(id='placeholder')
])


@app.callback(Output('tap-node-json-output', 'children'),
              [Input('cytoscape', 'tapNode')])
def displayTapNode(data):
    return json.dumps(data, indent=2)


@app.callback(Output('tap-edge-json-output', 'children'),
              [Input('cytoscape', 'tapEdge')])
def displayTapEdge(data):
    return json.dumps(data, indent=2)


@app.callback(Output('tap-node-data-json-output', 'children'),
              [Input('cytoscape', 'tapNodeData')])
def displayTapNodeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('tap-edge-data-json-output', 'children'),
              [Input('cytoscape', 'tapEdgeData')])
def displayTapEdgeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('mouseover-node-data-json-output', 'children'),
              [Input('cytoscape', 'mouseoverNodeData')])
def displayMouseoverNodeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('mouseover-edge-data-json-output', 'children'),
              [Input('cytoscape', 'mouseoverEdgeData')])
def displayMouseoverEdgeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('selected-node-data-json-output', 'children'),
              [Input('cytoscape', 'selectedNodeData')])
def displaySelectedNodeData(data):
    return json.dumps(data, indent=2)


@app.callback(Output('selected-edge-data-json-output', 'children'),
              [Input('cytoscape', 'selectedEdgeData')])
def displaySelectedEdgeData(data):
    return json.dumps(data, indent=2)


@app.callback(
    [Output('cytoscape', 'zoom'),
     Output('cytoscape', 'elements')],
    [Input('bt-reset', 'n_clicks')]
)
def reset_layout(n_clicks):
    print(n_clicks, 'click')
    return [1, data]


@app.callback(Output('cytoscape', 'layout'),
              Input('dropdown-callbacks-1', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }


if __name__ == '__main__':
    app.run_server(debug=True)
