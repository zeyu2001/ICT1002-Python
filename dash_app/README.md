# Usage

Install requirements first: `pip install -r requirements.txt`

For development and debugging only.

```
$ python3 runserver.py
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```
After running `runserver.py`, navigate to localhost to view the application.

# Project Structure
*Still needs some cleaning up!*
```
search/
|____emails.csv
|____top_words.py
|____requirements.txt
|____index.py
|____README.md
|____runserver.py
|____stats.py
|____callbacks.py
|____bm_alg.py
|____app.py
|____emails_updated.csv
|____data.py
|____routes.py
```
- `app.py`: Defines the Dash application. 
- `runserver.py`: Runs the application defined above. Integrates all routes and callbacks for the Dash application.
- `routes.py`: Specifies the routes (URLs) of the application. The application is multi-paged, but the browser does not need to refresh. The content is dynamically updated here :)
- `index.py`: Layout for / (homepage)
- `stats.py`: Layout for /stats
- `callbacks.py`: Defines callback functions for the Dash app. This is how the application is able to dynamically update its content (tables, graphs, etc.) based on the user input (search bar, dropdown, etc.)
- `data.py`: Extracts data from the dataset using pandas, exports data using pandas also
- `bm_alg.py`: The search algorithm. Time complexity is O(m+n) if pattern does not appear in the text, O(mn) if pattern does appear in the text

# Todo
- Write tests! Recommend using doctest.
- Write docstrings! Recommend using Google docstring format.
- Define external CSS (right now it is inline, defined in the Python script)
- Add other functions, like top words, etc. `top_words.py` already created but not used yet.
