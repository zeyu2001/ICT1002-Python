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
    style={"display": "inline", "margin": "10px"}
)

button_export = html.Div(
    id='export-charts',
    style={"display": "inline", "margin": "10px"},
)

toolbar = html.Div(
    [matched_count, button_back, button_export],
    style={"margin": "10px"}
)

date_picker = dcc.RangeSlider(
    id="date-slider",
    marks={date: "{}/10/2020".format(date) for date in range(1, 7)},
    updatemode="mouseup",
    allowCross=False,
    min=1,
    max=6,
    value=[2, 5]
)

stats_layout = html.Div(
    [
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
