from app import app
from index import index_layout
from stats import stats_layout
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# To share data between pages
data_store = dcc.Store(id='data-store')

# Dynamic app layout based on URL
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    data_store
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/stats':
        return stats_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_layout
