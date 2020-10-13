from app import app, server, UPLOAD_DIRECTORY
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
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(content.encode('utf-8'))


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


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
        }
    )
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

# Trick to share data between callbacks
intermediate_value = html.Div(
    id='intermediate-value', style={'display': 'none'})

# Dynamic app layout based on URL
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    heading,
    upload,
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
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_layout
