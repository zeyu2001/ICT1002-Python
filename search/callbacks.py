from app import app
from data import CATEGORIES
from bm_alg import boyer_moore_match
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


def get_data(query, category):

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
    [Input("search-index", "value"), Input("dropdown-index", "value")]
)
def search_data(query, category):
    data = get_data(query, category)
    return data, "{} items matched.".format(len(data))


@app.callback(
    [Output("graph-stats", "figure"), Output('matched-count-stats', 'children')],
    [Input("search-stats", "value"), Input("dropdown-stats", "value")]
)
def get_graph(query, category):
    data = get_data(query, category)
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
