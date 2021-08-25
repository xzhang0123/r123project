# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Time": list(range(6)),
    "Amount": [4, 1, 2, 2, 4, 5],
    # "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    "City": 1
})

fig = px.line(df, x="Time", y="Amount",title='Data')
# fig = px.line(df, x="Time", y="Amount", color="City",title='Data')
fig.update_layout(title_text='Data', title_x=0.5)

app.layout = html.Div(
children=[
html.Div([
    html.H1(children='R123 Intensity to Membrane Potential', style={'textAlign': 'center'}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Upload Data: Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '90%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Br(),
    # html.Div([    dcc.Graph(
    #         id='example-graph',
    #         figure=fig
    #     )]),
]),
html.Div(id='output-data-upload'),
html.Div([
        html.Div([
            # html.H3('Column 1', style={'textAlign': 'center'}),
            dcc.Graph(id='g1', figure=fig)
        ], className="six columns"),

        html.Div([
            # html.H3('Column 2', style={'textAlign': 'center'}),
            dcc.Graph(id='g2', figure=fig)
        ], className="six columns"),
    ], className="row")
    # html.Div(id='output-data-upload'),
])


def parse_contents(contents, filename, date):
    print(filename)
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            #df = pd.read_excel(io.BytesIO(decoded),header=[1],sheet_name=0,sep='\t',skiprows=1)
            df = pd.read_excel(io.BytesIO(decoded),sheet_name=0)
            #df = pd.read_excel(contents,sheet_name=0,sep='\t')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')],
              [State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)
