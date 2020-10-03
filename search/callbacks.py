import base64
import datetime
import io
import json

from app import app
from data import parse_data, DATASET
from bm_alg import boyer_moore_match
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Initialize data for initial layout
df, DATA, CATEGORIES, COLUMNS = parse_data(DATASET)

def get_data(query, category, json_data):

    if json_data:
        categories = json.loads(json_data)
        data = categories[category]
    else:
        data = CATEGORIES[category]

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
    [Input("search-index", "value"), Input("dropdown-index", "value"), Input("intermediate-value", "children")]
)
def search_data(query, category, json_data):
    data = get_data(query, category, json_data)
    return data, "{} items matched.".format(len(data))


@app.callback(
    [Output("graph-stats", "figure"), Output('matched-count-stats', 'children')],
    [Input("search-stats", "value"), Input("dropdown-stats", "value"), Input("intermediate-value", "children")]
)
def get_graph(query, category, json_data):
    data = get_data(query, category, json_data)
    result = {}
    for row in data:
        label = row['Label'].split('>')[0]
        if not label == 'Uncategorized':
            result.setdefault(label, 0)
            result[label] += 1

    sorted_data = sorted(list(result.items()),
                         key=lambda x: x[1], reverse=True)[:10]
    result = {
        'Label': [item[0] for item in sorted_data],
        'Count': [item[1] for item in sorted_data]
    }

    fig = px.bar(pd.DataFrame(result), x='Label', y='Count',
                 hover_data=['Label', 'Count'], color='Count',
                 labels={'Label': 'Email Content Categories'}, height=400)
    return fig, "{} items matched.".format(len(data))


def parse_contents(contents, filename, date):

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df, data, categories, columns = parse_data(io.StringIO(decoded.decode("ISO-8859-1")))

    except Exception as e:
        print(e)
        return False

    return df, data, categories, columns


@app.callback(Output('intermediate-value', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        results = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        categories = results[0][2]
        for result in results[1:]:
            categories['all'] += result[2]['all']
            categories['ham'] += result[2]['ham']
            categories['spam'] += result[2]['spam']
            
        return json.dumps(categories)