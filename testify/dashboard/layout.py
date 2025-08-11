
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def get_layout():
    """
    Generates the final, professional layout for the dashboard.
    - Adds dcc.Location to read URL parameters.
    - Adds dcc.Store for error messages.
    - Adds a div to display error messages.
    """
    return html.Div(className='dashboard-container', children=[
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='filtered-data-store'),
        dcc.Store(id='error-message-store'), # For error messages
        dcc.Download(id="download-dataframe-csv"),
        # ADD THIS LINE for automatic refresh every 5 seconds
        dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),
        # --- HEADER SECTION ---
        html.Div(className='header', children=[
            # Use assets folder for Dash static files
            html.Img(src='/assets/logo.png', alt="Logo", style={'height': '36px', 'width': 'auto', 'verticalAlign': 'middle'}),
            html.H1("Testify "),
            html.Div(className='header-icons', children=[  # html.I(className='fas fa-bell'),
                html.Div(className='profile-dropdown', children=[
                    html.I(className='fas fa-user-circle', id='profile-icon'),
                    html.Div(className='dropdown-menu', id='dropdown-menu', children=[
                        html.A('Profile', href='/profile'),
                        html.Hr(),
                        html.A('Logout', href='/logout'),
                    ], style={'display': 'none'})
                ])
            ])
        ]),

        html.Div(className='main-content', children=[
            html.Div(className='filters-sidebar', children=[
                html.H2("Filters"),
                html.Div(className='filter-group', children=[
                    html.Label("Product Type"),
                    dcc.Dropdown(id='product-dropdown', options=[], placeholder="Select products...", multi=True)
                ]),
                html.Div(className='filter-group', children=[
                    html.Label("Test Type"),
                    dcc.Dropdown(id='test-type-dropdown', options=[], placeholder="Select test types...", multi=True)
                ]),
                html.Div(className='filter-group', children=[
                    html.Label("Status"),
                    dcc.Dropdown(id='status-dropdown', options=[
                        {'label': 'Passed', 'value': 'Pass'},
                        {'label': 'Failed', 'value': 'Fail'},
                        {'label': 'Pending', 'value': 'Pending'}
                    ], placeholder="Select statuses...", multi=True)
                ]),
                html.Div(className='filter-group', children=[
                    html.Label("Date Range"),
                    dcc.DatePickerRange(id='date-picker-range', display_format='MM/DD/YYYY')
                ]),
                html.Button('Apply Filters', id='apply-filters-button', n_clicks=0)
            ]),

            html.Div(className='dashboard-content', id='dashboard-content-area', children=[
                html.Div(id='error-message-div'), # Div to display error messages
                html.Div(className='title-bar', children=[
                    html.H2("Dashboard"),
                    html.P("Analyze data with comprehensive filters and export options.")
                ]),

                dbc.Row([
                    dbc.Col(dbc.Card(id='kpi-total-tests', className='kpi-card')),
                    dbc.Col(dbc.Card(id='kpi-passed', className='kpi-card')),
                    dbc.Col(dbc.Card(id='kpi-failed', className='kpi-card')),
                    dbc.Col(dbc.Card(id='kpi-pending', className='kpi-card')),
                ]),

                dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='results-over-time-graph')), lg=12),
                ]),

                dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='stacked-bar-chart')), lg=7),
                    dbc.Col(dbc.Card(dcc.Graph(id='status-pie-chart')), lg=5),
                ]),

                dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='duration-box-plot')), lg=7),
                    dbc.Col(dbc.Card(dcc.Graph(id='duration-scatter-plot')), lg=5),
                ]),

                dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='tester-donut-chart')), lg=7),
                    dbc.Col(dbc.Card(dcc.Graph(id='coverage-area-chart')), lg=5),
                ]),

                dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='execution-heatmap')), width=12),
                ]),

                # --- THIS IS THE FIX FOR THE TABLE SCROLLING ---
                html.Div(className="table-wrapper", children=[
                    dash_table.DataTable(
                        id='detailed-test-table',
                        columns=[
                            {"name": "TEST NAME", "id": "test_id"}, {"name": "PRODUCT", "id": "product_name"},
                            {"name": "TYPE", "id": "test_type"}, {"name": "STATUS", "id": "status"},
                            {"name": "DURATION", "id": "duration_str"}, {"name": "DATE", "id": "execution_date_str"},
                        ],
                        style_cell={'backgroundColor': '#27293d', 'color': '#e0e0e0', 'border': 'none', 'textAlign': 'left'},
                        style_header={'backgroundColor': '#1a1c2c', 'fontWeight': 'bold'},
                    )
                ]),

                html.Div(className='dashboard-footer', children=[
                    html.P("Data Source: Manual | Live", className='footer-text'),
                    html.Div(className='footer-buttons', children=[
                        html.Button("Export as PDF", id="export-pdf-button"),
                        html.Button("Export as CSV", id="export-csv-button"),
                    ])
                ])
            ])
        ])
    ])
