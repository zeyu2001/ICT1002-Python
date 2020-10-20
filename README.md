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