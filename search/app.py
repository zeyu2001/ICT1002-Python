import dash
from flask import Flask
import os
from urllib.parse import quote as urlquote

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)

UPLOAD_DIRECTORY = "tmp/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
