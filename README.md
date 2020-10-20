# Usage

## Running in a Development Environment

Install requirements first: `pip install -r requirements.txt`

To run the Dash server:

```
$ python3 runserver.py
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
```

After running `runserver.py`, navigate to localhost to view the application.

## Debug Mode

By default, debug mode is turned off. 
To run the Dash server with debug mode turned on, use the `--d` or `--debug` option.

```
$ python3 runserver.py --d
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```

Running on debug mode will turn on [Dash DevTools](https://dash.plotly.com/devtools), giving you access to tools like callback graphs, hot reloading, in-app error reporting, etc. 

Use this for debugging and development purposes.

## Deploying to a Production Environment

In a development environment, the Dash app can be easily accessed by running `runserver.py` and navigating to localhost. In a production environment, the Dash app must be deployed to a server. 

Dash is written on top of Flask. Hence, deploying a Dash app is exactly the same as deploying a Flask app. Refer to Flask's [Deployment Guide](https://flask.palletsprojects.com/en/1.1.x/deploying/) for more details.

Note the following:
>While lightweight and easy to use, Flask’s built-in server is not suitable for production as it doesn’t scale well. 
>

A WSGI server should be used instead. Simple-to-use, affordable solutions include [PythonAnywhere](https://www.pythonanywhere.com/) and [Heroku](https://www.heroku.com/).

# Project Structure

```
.
├── LICENSE
├── README.md
├── classifier
│   ├── data
│   │   ├── x_test.npy
│   │   ├── x_train.npy
│   │   ├── y_test.npy
│   │   └── y_train.npy
│   ├── emails.csv
│   ├── exec.py
│   ├── main.py
│   ├── metrics
│   │   └── 20200925163152_plot.png
│   ├── models
│   │   └── 20200925163152_spam_classifier.h5
│   ├── predict_input.py
│   └── process_data.py
├── dash_app
│   ├── app.py
│   ├── bm_alg.py
│   ├── callbacks.py
│   ├── data.py
│   ├── emails.csv
│   ├── index.py
│   ├── predict.py
│   ├── routes.py
│   ├── stats.py
│   └── temp
│       └── app_files
│           ├── output.csv
│           └── stats_output.html
├── requirements.txt
└── runserver.py
```

## Classifier

- `process_data.py`: Processes data from the dataset, removing irrelevant data in the spam text including punctuation, stop words, hyperlinks, etc. and representing the data as a feature matrix that allows the model architecture to effectively extract relationships between the sequence data and resulting label.
- `exec.py`: Trains and saves the classifier model. 
- `predict_input.py`: Integration with the Dash Web GUI. Given a user input, predict whether the email is spam.

## Dash App

- `app.py`: Defines the Dash application. 
- `runserver.py`: Runs the application defined above. Integrates all routes and callbacks for the Dash application.
- `routes.py`: Specifies the routes (URLs) of the application. The application is multi-paged, but the browser does not need to refresh. The content is dynamically updated here. Also defines the functions and request handlers to serve local files, allowing the user to download exported results.
- `index.py`: Layout for '/' (homepage)
- `stats.py`: Layout for '/stats'
- `predict.py`: Layout for '/predict'
- `callbacks.py`: Defines callback functions for the Dash app. This is how the application is able to dynamically update its content (tables, graphs, etc.) based on the user input (search bar, dropdown, etc.).
- `data.py`: Extracts data from the dataset / exports data from the dataset using pandas.
- `bm_alg.py`: The search algorithm. We use the Boyer-Moore algorithm. The precomputation time complexity is O(m+k), where k is the size of the alphabet. The time complexity for the searching phase is O(n). 