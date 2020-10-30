"""
Layout for '/' (homepage)
"""

from data import parse_data, DATASET
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd

# Initialize data for initial layout
df, DATA, CATEGORIES, COLUMNS = parse_data(DATASET)

PIXEL_FOR_CHAR = 5


def create_conditional_style(df):
    style = []
    for col in df.columns[:-1]:
        name_length = len(col)
        pixel = 50 + round(name_length * PIXEL_FOR_CHAR)
        pixel = str(pixel) + "px"
        style.append({'if': {'column_id': col}, 'minWidth': pixel})

    return style


table = dt.DataTable(
    fixed_columns={'headers': True, 'data': 4},
    style_table={'minWidth': '100%'},
    style_data_conditional=create_conditional_style(df),
    style_cell={
        'textAlign': 'left',
        'minWidth': '100%',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
    id='table-index',
    columns=COLUMNS,
    data=DATA,
    sort_action="native"
)

loading_wrapper_table = dcc.Loading(
    id="loading-index",
    type="circle",
    children=[table]
)

matched_count = html.P(
    id='matched-count-index',
    style={"margin": "10px", "display": "inline"}
)

button_view_statistics = dcc.Link(
    html.Button('View Statistics'), href="/stats",
    style={"display": "inline", "margin": "10px"}
)

button_export = html.Div(
    id='export-data',
    style={"display": "inline", "margin": "10px"},
)

toolbar = html.Div(
    [matched_count, button_view_statistics, button_export],
    style={"margin": "10px"}
)

index_layout = html.Div(
    [
        toolbar,
        html.Div(loading_wrapper_table),
    ],
    style={
        "font-family": 'Palatino, "Palatino Linotype", "Palatino LT STD"',
    }
)
