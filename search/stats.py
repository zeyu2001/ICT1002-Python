import dash_html_components as html
import dash_core_components as dcc


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

bar_graph = dcc.Graph(id='bar-graph-stats')
pie = dcc.Graph(id='pie-stats')
line_graph = dcc.Graph(id='line-graph-stats')

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

date_picker = dcc.RangeSlider(
    id="date-slider",
    marks={date: "{}/10/2020".format(date) for date in range(1, 8)},
    updatemode="mouseup",
    allowCross=False,
    min=1,
    max=7,
    value=[3, 5]
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
        user_input,
        toolbar,
        heading_2,
        date_picker,
        bar_graph,
        pie,
        line_graph
    ],
    style={
        "font-family": 'Palatino, "Palatino Linotype", "Palatino LT STD"',
    }
)

