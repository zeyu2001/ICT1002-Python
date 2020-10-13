import base64
import datetime
import io
import json

from app import app
from data import parse_data, DATASET, export_data
from bm_alg import boyer_moore_match
from dash.dependencies import Input, Output, State

import dash
import plotly.express as px
import pandas as pd

# Initialize data for initial layout
df, DATA, CATEGORIES, COLUMNS = parse_data(DATASET)


def parse_json(json_data, category):
    """
    Parses the <json_data> from intermediate value.

    Args:
        json_data (str): A string of data to process in JSON format.
        category (str): The category ('all' / 'spam' / 'ham') to extract data from.

    Returns:
        (status_code, data), where status_code = 0 if there is no error, 1 otherwise.
    """
    if json_data:
        loaded_data = json.loads(json_data)
        categories = loaded_data['categories']
        error = loaded_data['error']

        if error:
            return (1, error)

        data = categories[category]

    else:
        data = CATEGORIES[category]

    return (0, data)


def get_data(query, data):
    """
    Queries <data> for the specified <query>.

    Args:
        query (str): A user query.
        data (list): A list of data to query.

    Returns:
        A list of data that satisfies the <query>.
    """
    # Use B-M algorithm to find relevant matches
    if query:
        result = []
        for row in data:
            text = row['Text']
            match = boyer_moore_match(text, query)
            if match != -1:
                result.append(row)
        return result

    # No query in the beginning
    else:
        return data


@app.callback(
    [Output("table-index", "data"), Output('matched-count-index', 'children')],
    [Input("search-index", "value"), Input("dropdown-index", "value"),
     Input("intermediate-value", "children")]
)
def search_data(query, category, intermediate_value):
    """
    Searches <intermediate_value> based on user-specified <query> and <category>.

    Args:
        query (str): A search query.
        category (str): A category ('all' / 'spam' / 'ham').
        intermediate_value (str): A string of data to process in JSON format.

    Returns:
        A list of matching data, and a string in the format "<length of data> items matched".
    """
    status_code, data = parse_json(intermediate_value, category)

    if status_code == 1:
        # Display empty table, and show the error message
        return [], data

    data = get_data(query, data)
    return data, "{} items matched.".format(len(data))


@app.callback(
    [Output("bar-graph-stats", "figure"),
     Output("pie-stats", "figure"),
     Output("line-graph-stats", "figure"),
     Output('matched-count-stats', 'children')],
    [Input("search-stats", "value"), Input("dropdown-stats", "value"),
     Input("intermediate-value", "children"), Input("date-slider", "value")]
)
def get_graph(query, category, intermediate_value, date_range):
    """
    Generates the following visualizations
    - bar graph of email categories
    - pie chart of email categories
    - line graph of frequency of received emails
    as Plotly graph objects.

    Args:
        query (str): A search query.
        category (str): A category ('all' / 'spam' / 'ham').
        intermediate_value (str): A string of data to process in JSON format.
        date_range (list): A date range, [start_date, end_date].

    Returns:
        A bar graph, pie chart, line graph, and a string in the format "<length of data> items matched".
    """
    status_code, data = parse_json(intermediate_value, category)

    if status_code == 1:
        # Display empty figure, and show the error message
        empty_fig = {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "No matching data found",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            }
        }
        return empty_fig, data

    data = get_data(query, data)
    categories_result = {}
    date_result = {}
    start_date, end_date = date_range[0], date_range[1]

    for row in data:
        date = row["Datetime"].split()[0]

        if int(date[-1]) in range(start_date, end_date):
            label = row['Label'].split('>')[0]

            if not label == 'Uncategorized':
                categories_result.setdefault(label, 0)
                categories_result[label] += 1

            date_result.setdefault(date, 0)
            date_result[date] += 1

    categories_sorted_data = sorted(list(categories_result.items()),
                                    key=lambda x: x[1], reverse=True)[:10]
    date_sorted_data = sorted(list(date_result.items()),
                              key=lambda x: x[0])

    categories_result = {
        'Label': [item[0] for item in categories_sorted_data],
        'Count': [item[1] for item in categories_sorted_data]
    }
    date_result = {
        'Dates': [item[0] for item in date_sorted_data],
        'Count': [item[1] for item in date_sorted_data]
    }

    bar_graph = px.bar(pd.DataFrame(categories_result), x='Label', y='Count',
                       hover_data=['Label', 'Count'], color='Count',
                       labels={'Label': 'Email Content Categories'}, height=400)

    pie = px.pie(pd.DataFrame(categories_result), values='Count', names='Label',
                 labels={'Label': "Email Content Categories", 'Count': "Number Of Emails"})

    line_graph = px.line(pd.DataFrame(date_result), x="Dates", y="Count",
                         title="Number of Emails sent on Each Day")

    return bar_graph, pie, line_graph, "{} items matched.".format(len(data))


def parse_contents(contents, filename, date):
    """
    Parses user-submitted dataset.

    Args:
        contents (str): A contents string generated from the user-uploaded file.
        filename (str): The filename of the user-uploaded file.
        date (str): The date of the user-uploaded file.
    
    Returns:
        Processed data in the form of Python data structures.
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df, data, categories, columns = parse_data(
            io.StringIO(decoded.decode("ISO-8859-1")))
    else:
        raise ValueError("Only CSV format supported.")

    return df, data, categories, columns


@app.callback(Output('intermediate-value', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    """
    Updates the hidden #intermediate-value element based on the user-uploaded data.
    If user uploads multiple files, combines the data from each file, and returns the aggregated data.

    Args:
        list_of_contents (list): A list of user-uploaded file contents.
        list_of_names (list): A list of user-uploaded file names.
        list_of_dates (list): A list of user-uploaded file dates.

    Returns:
        A string with data in JSON format.
    """
    if list_of_contents is not None:
        try:
            results = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]

        except Exception as e:
            print(e)
            error_msg = ("There was a problem processing your files. Please ensure the correct format is used." +
                         " Only CSV files with the headings: ['Datetime', 'Spam', 'Label', 'Relevance', 'Text']" +
                         " are supported at the moment.")
            categories = None

        else:
            categories = results[0][2]
            for result in results[1:]:
                categories['all'] += result[2]['all']
                categories['ham'] += result[2]['ham']
                categories['spam'] += result[2]['spam']
            error_msg = None

        return json.dumps({'categories': categories, 'error': error_msg})

# @app.callback(
#     Output("exportData", 'href'),
#     [Input("exportBtn", "n_clicks"),
#     Input("table-index", "data")])
# def export(n_clicks, data):

#     ctx = dash.callback_context
#     if ctx.triggered:
#         export_data(data_dict=data)
#         return 'C:/Program Files (x86)/SpamDetector/export.csv'

