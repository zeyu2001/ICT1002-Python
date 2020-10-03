import dash_html_components as html
import dash_core_components as dcc


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

graph = dcc.Graph(id='graph-stats')

matched_count = html.P(
    id='matched-count-stats',
    style={"margin": "10px", "display": "inline"}
)

button_back = dcc.Link(
    html.Button('Back'), href="/",
    style={"display": "inline"}
)

toolbar = html.Div(
    [matched_count, button_back],
    style={"margin": "10px"}
)

search_bar = dcc.Input(
    id="search-stats",
    type='text',
    placeholder="Search",
    style={
        "width": "100%",
        "margin": "10px",
        "height": "30px"
    }
)

dropdown = dcc.Dropdown(
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

stats_layout = html.Div(
    [
        heading,
        user_input,
        toolbar,
        heading_2,
        graph
    ],
    style={
        "font-family": 'Palatino, "Palatino Linotype", "Palatino LT STD"',
    }
)
