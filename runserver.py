# Insert into system path
import sys
sys.path.insert(0, './dash_app')
sys.path.insert(0, './classifier')

from app import app

if __name__ == '__main__':

    # Run server
    app.run_server(debug=False)
