from app import app
from app import server
import routes
import callbacks

if __name__ == '__main__':
    app.run_server(debug=True)