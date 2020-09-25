from app import app
from app import server
from bm_alg import boyer_moore_match
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import Input, Output
import pandas as pd

DATASET = "emails.csv"

# Parse dataset into pandas dataframe
df = pd.read_csv(DATASET)
df = df[df.columns.tolist()[::-1]]
DATA = df.to_dict('records')
DATA_SPAM = [item for item in DATA if item['spam']]
DATA_HAM = [item for item in DATA if not item['spam']]

CATEGORIES = {
    'all': DATA,
    'spam': DATA_SPAM,
    'ham': DATA_HAM
}

# Convert to verbose data, 1 --> Spam, 0 --> Not Spam
for row in DATA:
    row['spam'] = 'Spam' if row['spam'] else 'Not Spam'
columns = [{"name": i, "id": i} for i in df.columns]

# Dash layout
heading = html.Header(
    html.H1(
        "Spam Classifier Dataset",
        style={
            "text-align": "center", 
            "margin": "10px"
        }
    )
)

search_bar = dcc.Input(
    id="search",
    type='text',
    placeholder="Search",
    style={
        "width": "100%", 
        "margin": "10px"
    }
)

table = dt.DataTable(
    fixed_columns={'headers': True, 'data': 1},
    style_table={'minWidth': '100%'},
    style_cell={
        'textAlign': 'left',
        'minWidth': '100%',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
    id='table',
    columns=columns,
    data=DATA
)

loading_wrapper_table = dcc.Loading(
    id="loading-1",
    type="circle",
    children=[table]
)

dropdown = dcc.Dropdown(
    id='dropdown',
    options=[
        {'label': 'All', 'value': 'all'},
        {'label': 'Spam', 'value': 'spam'},
        {'label': 'Not Spam', 'value': 'ham'}
    ],
    value='all',
    style={"margin": "10px"}
)

user_input = html.Div(
    [
        html.Div(
            search_bar,
            style={
                "width": '68%',
                "display": 'table-cell',
            },
        ),
        html.Div(
            dropdown,
            style={
                "width": '30%',
                "display": 'table-cell',
            },
        ),
    ],
    style={
        "width": '100%',
        "display": 'table',
        "margin": "10px"
    }
)

app.layout = html.Div(
    [
        heading,
        user_input,
        html.Div(loading_wrapper_table),
    ],
    style={
        "font-family": "Helvetica Neue"
    }
)

# Dash callbacks
@app.callback(
    Output("table", "data"),
    [Input("search", "value")], Input("dropdown", "value")
)
def search_data(query, category):
    data = CATEGORIES[category]
    # Use B-M algorithm to find relevant matches
    if query:
        result = []
        for row in data:
            text = row['text']
            match = boyer_moore_match(text, query)
            if match != -1:
                result.append(row)
        return result

    # No query in the beginning
    else:
        return data


if __name__ == '__main__':
    app.run_server(debug=True)
