from __future__ import annotations

import json
import sys
from logging import getLogger
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output

logger = getLogger(__name__)


EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
TITLE = "LLDP Network Visualiser"


def load_json():
    json_data = []
    try:
        with open('data/node.json', 'r') as f:
            node_data = json.load(f)

        with open('data/edge.json', 'r') as f:
            edge_data = json.load(f)
        json_data.extend(node_data)
        json_data.extend(edge_data)
    except OSError as e:
        logger.error(str(e))
        sys.exit(1)
    else:
        return json_data


data = load_json()
cyto.load_extra_layouts()

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
    html.Div(className='row', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=data,
            layout={
                'name': 'cola',
                'directed': True,
                'padding': 10
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
    html.Button('Reset', id='bt-reset'),
    dcc.Dropdown(
        id='dropdown-callbacks-1',
        value='grid',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in [
                'grid',
                'breadthfirst',
                'cose-bilkent',
                'cola',
                'euler',
                'spread',
                'dagre',
                'klay',
            ]
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
