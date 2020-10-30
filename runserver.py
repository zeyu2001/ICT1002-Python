# Insert into system path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/dash_app')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/classifier')

import argparse
from app import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--d', '--debug', help="Turn on debug mode", action="store_true")
    args = parser.parse_args()

    debug = args.d
    # Run server
    app.run_server(debug=debug)
