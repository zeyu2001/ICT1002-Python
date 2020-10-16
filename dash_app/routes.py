# -*- coding: utf-8 -*-

from app import app, server, FILE_DIRECTORY
from flask import send_from_directory
from urllib.parse import quote as urlquote
from index import index_layout
from stats import stats_layout
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import base64
import os


def save_file(name, content):
    """Store a file on the Dash server."""
    with open(os.path.join(FILE_DIRECTORY, name), "wb") as fp:
        fp.write(content.encode('utf-8'))


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the file directory."""
    return send_from_directory(FILE_DIRECTORY, path, as_attachment=True)


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return location


heading = html.Header(
    html.H1(
        "Spam Classifier Dataset",
        style={
            "text-align": "center",
            "margin": "10px",
            "font-weight": "lighter",
            "font-size": "300%"
        },
        id='page-header'
    ),
)

toggle_language = html.Button(
    '中文',
    id='toggle-language',
)

upload = dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Your Own Datasets')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    multiple=True
)

search_bar = dcc.Input(
    id="search",
    type='text',
    placeholder="Search",
    style={
        "width": "100%",
        "margin": "10px",
        "height": "30px"
    }
)

dropdown = dcc.Dropdown(
    id='dropdown',
    options=[
        {'label': 'All', 'value': 'all'},
        {'label': 'Spam', 'value': 'spam'},
        {'label': 'Not Spam', 'value': 'ham'}
    ],
    value='all',
    style={
        "margin": "10px",
        "height": "30px"}
)

user_input = html.Div(
    [
        html.Div(
            search_bar,
            style={
                "width": '68%',
                "display": 'table-cell',
            },
        ),
        html.Div(
            dropdown,
            style={
                "width": '30%',
                "display": 'table-cell',
            },
        ),
    ],
    style={
        "width": '100%',
        "display": 'table',
        "margin": "10px"
    }
)

# Trick to share data between callbacks
intermediate_value = html.Div(
    id='intermediate-value', style={'display': 'none'})

# Dynamic app layout based on URL
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    heading,
    toggle_language,
    upload,
    user_input,
    intermediate_value,

    # The only part that changes
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    Displays the appropriate page layout based on the <pathname>.
    Dash dynamically updates the #page-content element to display the correct page. No browser refresh.

    Args:
        pathname (str): A string representing the URL path.

    Returns:
        A Dash HTML components object representing the layout of the specified URL path.
    """
    if pathname == '/stats':
        return stats_layout
    else:
        return index_layout
