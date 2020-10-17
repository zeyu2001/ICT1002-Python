import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd

PIXEL_FOR_CHAR = 5


def create_conditional_style(df):
    style = []
    for col in df.columns[:-1]:
        name_length = len(col)
        pixel = 50 + round(name_length * PIXEL_FOR_CHAR)
        pixel = str(pixel) + "px"
        style.append({'if': {'column_id': col}, 'minWidth': pixel})

    return style


heading_2 = html.Header(
    html.H2(
        "Classify Emails (Spam or Ham)",
        style={
            "text-align": "center",
            "margin": "10px",
            "font-weight": "lighter",
        }
    )
)

para = html.P(
    "Welcome to the spam classifier! Enter the email you wish to classify below:",
    style={"margin": "10px", "font-weight": "lighter",}
)

heading_3_1 = html.H2(
    "Email",
    style={
        "text-align": "left",
        "margin": "10px",
        "font-weight": "lighter",
    }
)

heading_3_2 = html.H2(
    "Prediction History",
    style={
        "text-align": "left",
        "margin": "10px",
        "font-weight": "lighter",
    }
)

input_text = dcc.Textarea(
    id="predict-input",
    placeholder="Copy and Paste Email Here...",
    style={
        "width": "100%",
        "margin": "10px",
        "height": "300px"
    }
)

button_back = dcc.Link(
    html.Button('Back'), href="/",
    style={"margin": "10px"}
)

input = html.Div(
    [input_text, button_back],
    style={"margin": "10px"}
)

df = pd.DataFrame({'Spam': [], 'Text': []})

output = dt.DataTable(
    fixed_columns={'headers': True, 'data': 1},
    style_data_conditional=create_conditional_style(df),
    style_table={'minWidth': '100%'},
    style_cell={
        'textAlign': 'left',
        'minWidth': '100%',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
    id='predict-output',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    sort_action="native"
)

loading_wrapper_output = dcc.Loading(
    id="loading-index",
    type="circle",
    children=[output]
)

predict_layout = html.Div(
    [
        heading_2,
        heading_3_1,
        para,
        input,
        heading_3_2,
        loading_wrapper_output,
    ],
    style={
        "font-family": 'Palatino, "Palatino Linotype", "Palatino LT STD"',
    }
)