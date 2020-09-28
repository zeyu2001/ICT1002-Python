from app import app
from app import server
from bm_alg import boyer_moore_match
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

DATASET = "emails_updated.csv"

# Parse dataset into pandas dataframe
df = pd.read_csv(DATASET, encoding="ISO-8859-1",
                 converters={i: str for i in range(0, 100)})
df = df[['Spam', 'Label', 'Relevance', 'Text']]
DATA = df.to_dict('records')
DATA_SPAM = [item for item in DATA if item['Spam'] == '1']
DATA_HAM = [item for item in DATA if item['Spam'] == '0']

CATEGORIES = {
    'all': DATA,
    'spam': DATA_SPAM,
    'ham': DATA_HAM
}

# Convert to verbose data, 1 --> Spam, 0 --> Not Spam
for row in DATA:
    row['Spam'] = 'Spam' if row['Spam'] == '1' else 'Not Spam'
columns = [{"name": i, "id": i} for i in df.columns]

PIXEL_FOR_CHAR = 5


def create_conditional_style(df):
    style = []
    for col in df.columns[:-1]:
        name_length = len(col)
        pixel = 50 + round(name_length * PIXEL_FOR_CHAR)
        pixel = str(pixel) + "px"
        style.append({'if': {'column_id': col}, 'minWidth': pixel})

    return style


# Dash layout
heading = html.Header(
    html.H1(
        "Spam Classifier Dataset",
        style={
            "text-align": "center",
            "margin": "10px",
            "font-weight": "lighter",
            "font-size": "300%"
        }
    )
)

search_bar = dcc.Input(
    id="search",
    type='text',
    placeholder="Search",
    style={
        "width": "100%",
        "margin": "10px",
        "height": "30px"
    }
)

table = dt.DataTable(
    fixed_columns={'headers': True, 'data': 3},
    style_table={'minWidth': '100%'},
    style_data_conditional=create_conditional_style(df),
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
    style={
        "margin": "10px",
        "height": "30px"}
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


matched_count = html.P(
    id='matched-count',
    style={"margin": "10px", "display": "inline"}
)


button_view_statistics = dcc.Link(
    html.Button('View Statistics'), href="/stats",
    style={"display": "inline"}
)

toolbar = html.Div(
    [matched_count, button_view_statistics],
    style={"margin": "10px"}
)

# To share data between pages
data_store = dcc.Store(id='data-store')

# Dynamic app layout based on URL
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    data_store
])

# Layout of index page
index_layout = html.Div(
    [
        heading,
        user_input,
        toolbar,
        html.Div(loading_wrapper_table),
    ],
    style={
        "font-family": 'Palatino, "Palatino Linotype", "Palatino LT STD"',
    }
)

# Layout of stats page
heading_2 = html.Header(
    html.H2(
        "Top 10 Email Categories (From Matched Items)",
        style={
            "text-align": "center",
            "margin": "10px",
            "font-weight": "lighter",
        }
    )
)

graph = dcc.Graph(id='graph')

matched_count_stats = html.P(
    id='matched-count-stats',
    style={"margin": "10px", "display": "inline"}
)

button_back = dcc.Link(
    html.Button('Back'), href="/",
    style={"display": "inline"}
)

toolbar_stats = html.Div(
    [matched_count_stats, button_back],
    style={"margin": "10px"}
)

search_bar_stats = dcc.Input(
    id="search-stats",
    type='text',
    placeholder="Search",
    style={
        "width": "100%",
        "margin": "10px",
        "height": "30px"
    }
)

dropdown_stats = dcc.Dropdown(
    id='dropdown-stats',
    options=[
        {'label': 'All', 'value': 'all'},
        {'label': 'Spam', 'value': 'spam'},
        {'label': 'Not Spam', 'value': 'ham'}
    ],
    value='all',
    style={
        "margin": "10px",
        "height": "30px"}
)

user_input_stats = html.Div(
    [
        html.Div(
            search_bar_stats,
            style={
                "width": '68%',
                "display": 'table-cell',
            },
        ),
        html.Div(
            dropdown_stats,
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

stats_layout = html.Div(
    [
        heading,
        user_input_stats,
        toolbar_stats,
        heading_2,
        graph
    ],
    style={
        "font-family": 'Palatino, "Palatino Linotype", "Palatino LT STD"',
    }
)

# Dash callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/stats':
        return stats_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_layout


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
        return result, "{} items matched.".format(len(result))

    # No query in the beginning
    else:
        return data, "{} items matched.".format(len(data))


@app.callback(
    [Output("table", "data"), Output('matched-count', 'children')],
    [Input("search", "value"), Input("dropdown", "value")]
)
def search_data(query, category):
    return get_data(query, category)


@app.callback(
    [Output("graph", "figure"), Output('matched-count-stats', 'children')],
    [Input("search-stats", "value"), Input("dropdown-stats", "value")]
)
def get_graph(query, category):
    data, matched = get_data(query, category)
    result = {}
    for row in data:
        label = row['Label'].split('>')[0]
        if not label == 'Uncategorized':
            result.setdefault(label, 0)
            result[label] += 1

    sorted_data = sorted(list(result.items()), key=lambda x: x[1], reverse=True)[:10]
    result = {
        'Label': [item[0] for item in sorted_data],
        'Count': [item[1] for item in sorted_data]
    }
    
    fig = px.bar(pd.DataFrame(result), x='Label', y='Count',
                 hover_data=['Label', 'Count'], color='Count',
                 labels={'Label': 'Email Content Categories'}, height=400)
    return fig, matched


if __name__ == '__main__':
    app.run_server(debug=True)
