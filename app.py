from __future__ import annotations

import json
import sys
from logging import getLogger
from textwrap import dedent as d

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output
from modules.load_data import LoadingData
from modules.data_type import LOAD_DATA, STYLES

logger = getLogger(__name__)


EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
BOOTSTRAP_STYLESHEETS = [dbc.themes.BOOTSTRAP]
TITLE = "LLDP Network Visualiser"

loadingdata = LoadingData()
styles: STYLES = loadingdata.loading_styles()
data: LOAD_DATA = loadingdata.loading_data()

"""
print("Loading node data.")
with open('data/node.json', 'r') as f:
    node_data = json.load(f)
    data.extend(node_data)

print("Loading edge data.")
with open('data/edge.json', 'r') as f:
    edge_data = json.load(f)
    data.extend(edge_data)

print("Loading style settings.")
with open('style/styles.json', 'r') as f:
    styles = json.load(f)
"""

cyto.load_extra_layouts()
app = dash.Dash(
    __name__,
    external_stylesheets=BOOTSTRAP_STYLESHEETS,
    title=TITLE,
)

tab_tapnode_content = dbc.Card(
    dbc.CardBody(
        [
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
        ]
    ),
    className="mt-3",
)

tab_mouseover_content = dbc.Card(
    dbc.CardBody(
        [
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
        ]
    ),
    className="mt-3",
)

tab_tap_object = dbc.Card(
    dbc.CardBody(
        [
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
        ]
    ),
    className="mt-3",
)

tab_selected_data = dbc.Card(
    dbc.CardBody(
        [
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
        ]
    ),
    className="mt-3",
)

app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(html.H1(TITLE, id='title'), style=styles['title']),
        ],
        className="h-30"
    ),
    dbc.Row(
        [
            dbc.Col(dbc.Button("Reset Layout", id='layout-reset', outline=True, color="dark")),
            dbc.Col(dcc.Dropdown(
                id='dropdown-callbacks-1',
                value='cose-bilkent',
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
                ]),
            ),
        ],
        className="h-30",
    ),
    dbc.Row(
        [
            dbc.Col(cyto.Cytoscape(
                id='cytoscape',
                elements=data,
                layout={
                    'name': 'cola',
                    'directed': True,
                    'padding': 10
                },
                style={
                    'height': '750px',
                    'width': '100%',
                },
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {'content': 'data(label)'}
                    },
                    {
                        'selector': 'edge',
                        'style': {'content': 'data(value)'}
                    },
                    {
                        'selector': '.dashed',
                        'style': {'line-style': 'dashed'}
                    }
                ]),
                width=9,
            ),
            dbc.Col(
                dbc.Tabs(
                    [
                        dbc.Tab(tab_tapnode_content, label="Tap Data"),
                        dbc.Tab(tab_mouseover_content, label="Mouseover Data"),
                        dbc.Tab(tab_tap_object, label="Tap Object Data"),
                        dbc.Tab(tab_selected_data, label="Selected Data"),
                    ],
                    id="tabs",
                ),
                # html.Div(id='placeholder'),
                width=3,
                style={"background-color": "lightyellow"},
            ),
        ],
        style={"height": "100%", "background-color": "lightgray"},
    ),
], style={"background-color": "white"},
)


@ app.callback(Output('tap-node-json-output', 'children'),
               [Input('cytoscape', 'tapNode')])
def displayTapNode(data):
    return json.dumps(data, indent=2)


@ app.callback(Output('tap-edge-json-output', 'children'),
               [Input('cytoscape', 'tapEdge')])
def displayTapEdge(data):
    return json.dumps(data, indent=2)


@ app.callback(Output('tap-node-data-json-output', 'children'),
               [Input('cytoscape', 'tapNodeData')])
def displayTapNodeData(data):
    return json.dumps(data, indent=2)


@ app.callback(Output('tap-edge-data-json-output', 'children'),
               [Input('cytoscape', 'tapEdgeData')])
def displayTapEdgeData(data):
    return json.dumps(data, indent=2)


@ app.callback(Output('mouseover-node-data-json-output', 'children'),
               [Input('cytoscape', 'mouseoverNodeData')])
def displayMouseoverNodeData(data):
    return json.dumps(data, indent=2)


@ app.callback(Output('mouseover-edge-data-json-output', 'children'),
               [Input('cytoscape', 'mouseoverEdgeData')])
def displayMouseoverEdgeData(data):
    return json.dumps(data, indent=2)


@ app.callback(Output('selected-node-data-json-output', 'children'),
               [Input('cytoscape', 'selectedNodeData')])
def displaySelectedNodeData(data):
    return json.dumps(data, indent=2)


@ app.callback(Output('selected-edge-data-json-output', 'children'),
               [Input('cytoscape', 'selectedEdgeData')])
def displaySelectedEdgeData(data):
    return json.dumps(data, indent=2)


@ app.callback(
    [Output('cytoscape', 'zoom'),
     Output('cytoscape', 'elements')],
    [Input('layout-reset', 'n_clicks')]
)
def reset_layout(n_clicks):
    print(n_clicks, 'click')
    return [1, data]


@ app.callback(Output('cytoscape', 'layout'),
               Input('dropdown-callbacks-1', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
