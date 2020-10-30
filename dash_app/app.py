"""
Defines the Dash application.
"""

import dash
from flask import Flask
import os
from urllib.parse import quote as urlquote

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)

FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/temp/app_files"

if not os.path.exists(FILE_DIRECTORY):
    os.makedirs(FILE_DIRECTORY)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(server=server, title='Spam or Ham', external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

# Initialize, routes, layouts and callbacks
import routes
import callbacks
