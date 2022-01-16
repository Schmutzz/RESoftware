import dash
import html as html
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table as dt
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_dual_listbox import DualList
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from matplotlib import colors as mcolors
import main

print('Programmstart')



colors = mcolors.CSS4_COLORS
names = list(colors)
for i in names:
    if 'light' in i or 'white' in i:
        names.remove(i)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server

df = pd.read_csv('data/GruenEnergie_2019_ausbau.csv', sep=';', decimal=',', encoding='latin1')
df['Datum'] = pd.to_datetime(df['Datum'])

# ----------------------------------------------------------------------------------------------------------------------

df['Erzeugung_Gesamt_true_with_gaps'] = df['Erzeugung_Gesamt'].values
df['Erzeugung_Gesamt_false_with_gaps'] = df['Erzeugung_Gesamt'].values

df.loc[df['EE>100%'] == False, 'Erzeugung_Gesamt_true_with_gaps'] = 'NaN'
df.loc[df['EE>100%'] == True, 'Erzeugung_Gesamt_false_with_gaps'] = 'NaN'

# ----------------------------------------------------------------------------------------------------------------------

df['Erzeugung_Percentage_true_with_gaps'] = df['EE_Anteil'].values
df['Erzeugung_Percentage_false_with_gaps'] = df['EE_Anteil'].values

df.loc[df['EE>100%'] == False, 'Erzeugung_Percentage_true_with_gaps'] = 'NaN'
df.loc[df['EE>100%'] == True, 'Erzeugung_Percentage_false_with_gaps'] = 'NaN'

# ----------------------------------------------------------------------------------------------------------------------

conv = df['Diff_EE_zu_Verb'].loc[df['Diff_EE_zu_Verb'] < 0].sum()
conv *= -1
df_sum = pd.DataFrame()
df_sum['Energiemenge'] = [df['Verbrauch_Gesamt'].sum() - conv, df['Erzeugung_PV'].sum(), conv]
df_sum['Art'] = ['Wind', 'Solar', 'Konventionell']

# ----------------------------------------------------------------------------------------------------------------------

wea_modelle = pd.read_excel('data/WEA-Typen.xlsx')['Modell'].tolist()
wea_modelle = list(set(wea_modelle))
wea_modelle.pop(0)
wea_modelle.remove('v')

# ----------------------------------------------------------------------------------------------------------------------

areas_vor_df = pd.read_csv('data/test_func.csv', sep=';', decimal=',', encoding='utf-8',
                           usecols=['ID', 'Latitude', 'Longitude', 'Wetter-ID_Vor', 'haVor'])
areas_vor_df = areas_vor_df[areas_vor_df['Wetter-ID_Vor'] != 0]
areas_vor_df = areas_vor_df.sort_values(by=['Wetter-ID_Vor'])
areas_vor_df['Wetter-ID_Vor'] = areas_vor_df['Wetter-ID_Vor'].map(str)
areas_vor_df['haVor'] = areas_vor_df['haVor'].map(float)

# ----------------------------------------------------------------------------------------------------------------------

areas_pot_df = pd.read_csv('data/test_func.csv', sep=';', decimal=',', encoding='utf-8',
                           usecols=['ID', 'Latitude', 'Longitude', 'Wetter-ID_Pot', 'haPot'])
areas_pot_df = areas_pot_df[areas_pot_df['Wetter-ID_Pot'] != 0]
areas_pot_df = areas_pot_df.sort_values(by=['Wetter-ID_Pot'])
areas_pot_df['Wetter-ID_Pot'] = areas_pot_df['Wetter-ID_Pot'].map(str)
areas_pot_df['haPot'] = areas_pot_df['haPot'].map(float)

color_map = {}
for index, i in enumerate(areas_pot_df['Wetter-ID_Pot'].unique()):
    color_map[i] = names[index]

table_df = pd.read_csv('data/table.csv', sep=';', decimal=',', encoding='utf-8')

'''def drawEE_percentage(coloring):
    return px.line(df, x="Datum", y='EE_Anteil', color=coloring,
                   title='Ratio Renewable Energy to Consumption').update_layout(
        template='plotly_dark', title_x=0.5).add_hline(y=1).update_traces(showlegend=True)'''


def drawEE_percentage():
    fig = go.Figure()

    '''fig.add_trace(go.Scatter(x=df['Datum'], y=df['Verbrauch_Gesamt'], marker=dict(color='blue', opacity=0.7),
                             name="Verbrauch"))'''
    fig.add_trace(
        go.Scatter(x=df['Datum'], y=df['Erzeugung_Percentage_true_with_gaps'], marker=dict(color='green'),
                   name="EE>100%"))
    fig.add_trace(
        go.Scatter(x=df['Datum'], y=df['Erzeugung_Percentage_false_with_gaps'], marker=dict(color='red'),
                   name="EE<100%"))
    fig.update_layout(template='plotly_dark', title='Hourly Data: Ratio Renewable Energy to Consumption', title_x=0.5)
    fig.add_hline(y=1)

    return fig


def drawEE_absolute():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Datum'], y=df['Erzeugung_Gesamt_true_with_gaps'], marker=dict(color='green'),
                   name="EE>100%"))
    fig.add_trace(
        go.Scatter(x=df['Datum'], y=df['Erzeugung_Gesamt_false_with_gaps'], marker=dict(color='red'),
                   name="EE<100%"))
    fig.add_trace(go.Scatter(x=df['Datum'], y=df['Verbrauch_Gesamt'], marker=dict(color='blue', opacity=0.2),
                             name="Verbrauch"))
    fig.update_layout(template='plotly_dark', title='Hourly Data: Absolute Values', title_x=0.5)

    return fig


def drawEE_absolute_line():
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Datum'], y=df['Verbrauch_Gesamt'], mode='lines', line={'color': 'blue', 'width': 2},
                             name="Verbrauch"))
    fig.add_trace(
        go.Scatter(x=df['Datum'], y=df['Erzeugung_Gesamt_true_with_gaps'], marker=dict(color='lime', opacity=0.7),
                   name="EE>100%",
                   fill='tonexty'))
    fig.add_trace(go.Scatter(x=df['Datum'], y=df['Erzeugung_Gesamt_false_with_gaps'], mode='lines',
                             line={'dash': 'dash', 'color': 'red'}, name="EE<100%"))
    fig.update_layout(template='plotly_dark')

    '''return px.scatter(df, x="Datum", y='Verbrauch_Gesamt').update_layout(
        template='plotly_dark').update_traces(showlegend=True)'''

    return fig


def draw_pie():
    return px.pie(df_sum, 'Art', 'Energiemenge', title='Used Energy').update_layout(
        template='plotly_dark', title_x=0.5)


def draw_vor():
    return px.scatter_mapbox(areas_vor_df, lat='Latitude', lon='Longitude', title='Simulated expansion',
                             color='Wetter-ID_Vor',
                             color_discrete_map={}, size='haVor', size_max=12,
                             zoom=6.3, center={'lat': 54.2, 'lon': 9.8}).update_layout(
        mapbox_style="open-street-map",
        template='plotly_dark', title_x=0.5)


def draw_pot():
    return px.scatter_mapbox(areas_pot_df, lat='Latitude', lon='Longitude', title='Simulated expansion',
                             color='Wetter-ID_Pot',
                             color_discrete_map={}, size='haPot', size_max=12,
                             zoom=6.3, center={'lat': 54.2, 'lon': 9.8}).update_layout(
        mapbox_style="open-street-map",
        template='plotly_dark', title_x=0.5)


# ----------------------------------------------------------------------------------------------------------------------
# general settings


example_switch = html.Div([
    dbc.RadioItems(
        id="example_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}
        ],
        value='Yes'
    ),
], className="radio-group")

scenario_dropdown = html.Div([
    dcc.Dropdown(
        id='scenario_dropdown',
        options=[
            {'label': 'Scenario 1', 'value': 'Scenario 1'},
            {'label': 'Scenario 2', 'value': 'Scenario 2'},
            {'label': 'Scenario 3', 'value': 'Scenario 3'},
            {'label': 'Scenario 4', 'value': 'Scenario 4'},
        ],
        style={"textAlign": "left", 'color': 'black'}
    )
])

year_dropdown = html.Div([
    dcc.Dropdown(
        id='year_dropdown',
        options=[
            {'label': '2019', 'value': '2019'},
            {'label': '2020', 'value': '2020'}
        ],
        value='2019',
        style={"textAlign": "left", 'color': 'black'}
    )
])

general_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('General Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Scenario:'),
                scenario_dropdown
            ], width=4)
        ], className='pb-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Use example data?'),
                example_switch
            ], width=6)
        ], className='py-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Year:'),
                year_dropdown
            ], width=3)
        ], className='py-3', justify="center")
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# parameters settings


hours_slider = html.Div([
    dcc.Slider(
        id='hours_slider',
        min=0,
        max=100,
        step=1,
        value=50,
        marks={
            x: {'label': str(x) + '%'} for x in range(0, 100, 10)
        },
        tooltip={"placement": "bottom", "always_visible": True},
    )
])

power_slider = html.Div([
    dcc.Slider(
        id='power_slider',
        min=0,
        max=100,
        step=1,
        value=50,
        marks={
            x: {'label': str(x) + '%'} for x in range(0, 100, 10)
        },
        tooltip={"placement": "bottom", "always_visible": True},
    )
])

storage_switch = html.Div([
    dbc.RadioItems(
        id="storage_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}
        ],
        value='No'
    ),
], className="radio-group")

parameters_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('Project Parameters', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Percentage of hours over threshold:'),
                hours_slider
            ], width=10)
        ], className='pb-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Renewable power percentage threshold:'),
                power_slider
            ], width=10)
        ], className='py-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Use storage?'),
                storage_switch
            ], width=4)
        ], className='py-3', justify="center")
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# cost settings


budget_input = html.Div([
    dbc.Input(id='budget_input', placeholder='Type in a budget...', type="number", min=0,
              max=50, step=1)
])

profit_switch = html.Div([
    dbc.RadioItems(
        id="profit_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}
        ],
        value='Yes'
    ),
], className="radio-group")

time_span_slider = html.Div([
    dcc.Slider(
        id='time_span_slider',
        min=1,
        max=20,
        step=1,
        value=20,
        disabled=False,
        marks={
            x: {'label': str(x)} for x in range(0, 20, 5)
        },
        tooltip={"placement": "bottom", "always_visible": True},
    )
])

cost_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('Cost Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Budget (in billion €):'),
                budget_input
            ], width=6)
        ], className='pb-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Use expected profit during the simulation?'),
                profit_switch
            ], width=10)
        ], className='py-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Time period for profit calculation (years):'),
                time_span_slider
            ], width=10)
        ], className='py-3', justify="center")
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# biomass/solar settings


growth_switch = html.Div([
    dbc.RadioItems(
        id="growth_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}
        ],
        value='Yes'
    ),
], className="radio-group")

biomass_input = html.Div([
    dbc.Input(id='biomass_input', placeholder='Type in a factor...', type="number", min=0,
              max=100, step=1)
])

solar_input = html.Div([
    dbc.Input(id='solar_input', placeholder='Type in a factor...', type="number", min=0,
              max=100, step=1)
])

bio_solar_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('Biomass/Solar Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Use a yearly growth factor?'),
                growth_switch
            ], width=6)
        ], className='pb-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Biomass growth (in %):'),
                biomass_input
            ], width=6)
        ], className='py-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Solar growth (in %):'),
                solar_input
            ], width=6)
        ], className='py-3', justify="center")
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# wind settings


area_check = html.Div([
    dcc.Checklist(
        id='area_check',
        options=[
            {'label': 'Vorranggebiete', 'value': 'vor'},
            {'label': 'Potentialflächen', 'value': 'pot'}
        ],
        value=['vor'],
        inputStyle={"margin-left": "20px", 'margin-right': "5px"}
    )
])

# noinspection PyCallingNonCallable
dual_list = html.Div([
    DualList(id='dual_list', available=[{'label': x, 'value': x} for x in wea_modelle],
             selected=['Enercon E-115'], leftLabel='Use these models', rightLabel='Do not use these models')
])

# noinspection PyCallingNonCallable
wind_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('Wind Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Which areas should be used?'),
                area_check
            ], width=8)
        ], className='pb-3', justify="around"),
        dbc.Row([
            dbc.Col([
                dual_list
            ])
        ], className='py-3', justify="center")
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# app layout

start_button = html.Div([
    dbc.Button('Start', id='start_button', n_clicks=0),
    html.Div(id='start_output')
], className='text-center')

settings_children = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('REE-Simulation™')
                ])
            ], className='text-center')
        ], width=11)
    ], justify='center', className='pb-1'),
    dbc.Row([
        dbc.Col([
            general_settings,
            parameters_settings
        ], className='mt-1'),
        dbc.Col([
            cost_settings,
            bio_solar_settings
        ], className='mt-1'),
        dbc.Col([
            wind_settings,
        ], className='mt-1')
    ], className='px-3 py-1', justify='center')
])

results = html.Div([
    dbc.Row([
        dbc.Card([
            dbc.CardHeader([
                html.H4('Simulation results:')
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.P('Data:'),
                        dcc.Dropdown(id='dropdown_data',
                                     options=[
                                         {'label': 'ratio', 'value': 'ratio'},
                                         {'label': 'absolute', 'value': 'absolute'}
                                     ],
                                     value='ratio',
                                     style={"textAlign": "left", 'color': 'black'}
                                     )
                    ], width=1)
                ]),
                dbc.Row([
                    dcc.Graph(id='graph_year'),
                ], className='py-2'),
                dbc.Row([
                    dbc.Col([
                        html.P('Area:'),
                        dcc.Dropdown(id='dropdown_map',
                                     options=[
                                         {'label': 'Vor', 'value': 'Vor'},
                                         {'label': 'Pot', 'value': 'Pot'}
                                     ],
                                     value='Vor',
                                     style={"textAlign": "left", 'color': 'black'}
                                     )
                    ], width=1)
                ], className='pt-2'),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='map', figure=draw_vor())
                    ], width=7),
                    dbc.Col([
                        dcc.Graph(id='pie', figure=draw_pie())
                    ], width={'size': 5})
                ], className='py-2', justify="between"),
                dbc.Row([
                    dt.DataTable(id='table', columns=[{"name": i, "id": i} for i in table_df.columns],
                                 data=table_df.to_dict('records'), cell_selectable=False,
                                 style_header={
                                     'backgroundColor': 'rgb(10, 10, 10)',
                                     'color': 'white'},
                                 style_data={
                                     'backgroundColor': 'rgb(40, 40, 40)',
                                     'color': 'white'},
                                 style_data_conditional=(
                                     [
                                         {
                                             'if': {
                                                 'column_id': 'Wind (TWh)',
                                                 'filter_query': '{{Wind (TWh)}} = {}'.format(
                                                     table_df['Wind (TWh)'].nlargest(2).tolist()[1])
                                             },
                                             'backgroundColor': '#c9ffba',
                                             'color': 'black'
                                         },
                                         {
                                             'if': {
                                                 'column_id': 'Wind (TWh)',
                                                 'filter_query': '{{Wind (TWh)}} = {}'.format(
                                                     table_df['Wind (TWh)'].min())
                                             },
                                             'backgroundColor': '#ffbaba',
                                             'color': 'black'
                                         },

                                         # -----------------------------------------------------------------------------

                                         {
                                             'if': {
                                                 'column_id': 'Solar (TWh)',
                                                 'filter_query': '{{Solar (TWh)}} = {}'.format(
                                                     table_df['Solar (TWh)'].nlargest(2).tolist()[1])
                                             },
                                             'backgroundColor': '#c9ffba',
                                             'color': 'black'
                                         },
                                         {
                                             'if': {
                                                 'column_id': 'Solar (TWh)',
                                                 'filter_query': '{{Solar (TWh)}} = {}'.format(
                                                     table_df['Solar (TWh)'].min())
                                             },
                                             'backgroundColor': '#ffbaba',
                                             'color': 'black'
                                         },

                                         # -----------------------------------------------------------------------------

                                         {
                                             'if': {
                                                 'column_id': 'RE (TWh)',
                                                 'filter_query': '{{RE (TWh)}} = {}'.format(
                                                     table_df['RE (TWh)'].nlargest(2).tolist()[1])
                                             },
                                             'backgroundColor': '#c9ffba',
                                             'color': 'black'
                                         },
                                         {
                                             'if': {
                                                 'column_id': 'RE (TWh)',
                                                 'filter_query': '{{RE (TWh)}} = {}'.format(
                                                     table_df['RE (TWh)'].min())
                                             },
                                             'backgroundColor': '#ffbaba',
                                             'color': 'black'
                                         },

                                         # -----------------------------------------------------------------------------

                                         {
                                             'if': {
                                                 'column_id': 'Consum. (TWh)',
                                                 'filter_query': '{{Consum. (TWh)}} = {}'.format(
                                                     table_df['Consum. (TWh)'].nlargest(2).tolist()[1])
                                             },
                                             'backgroundColor': '#ffbaba',
                                             'color': 'black'
                                         },
                                         {
                                             'if': {
                                                 'column_id': 'Consum. (TWh)',
                                                 'filter_query': '{{Consum. (TWh)}} = {}'.format(
                                                     table_df['Consum. (TWh)'].min())
                                             },
                                             'backgroundColor': '#c9ffba',
                                             'color': 'black'
                                         },

                                         # -----------------------------------------------------------------------------

                                         {
                                             'if': {
                                                 'column_id': 'Deficit (TWh)',
                                                 'filter_query': '{{Deficit (TWh)}} = {}'.format(
                                                     table_df['Deficit (TWh)'].nlargest(2).tolist()[1])
                                             },
                                             'backgroundColor': '#ffbaba',
                                             'color': 'black'
                                         },
                                         {
                                             'if': {
                                                 'column_id': 'Deficit (TWh)',
                                                 'filter_query': '{{Deficit (TWh)}} = {}'.format(
                                                     table_df['Deficit (TWh)'].min())
                                             },
                                             'backgroundColor': '#c9ffba',
                                             'color': 'black'
                                         },

                                         # -----------------------------------------------------------------------------

                                         {
                                             'if': {
                                                 'column_id': 'Hours 100%',
                                                 'filter_query': '{{Hours 100%}} = {}'.format(
                                                     table_df['Hours 100%'].nlargest(2).tolist()[1])
                                             },
                                             'backgroundColor': '#c9ffba',
                                             'color': 'black'
                                         },
                                         {
                                             'if': {
                                                 'column_id': 'Hours 100%',
                                                 'filter_query': '{{Hours 100%}} = {}'.format(
                                                     table_df['Hours 100%'].min())
                                             },
                                             'backgroundColor': '#ffbaba',
                                             'color': 'black'
                                         },

                                     ]
                                 ),
                                 style_cell={
                                     'width': 'auto'
                                 }
                                 )
                ], className='py-2')
            ])
        ], inverse=True, className='text-center p-1')
    ], className='px-3 py-1')
])

app.layout = html.Div([
    html.Div(id='settings_page', children=settings_children, style={'display': 'inline'}),
    dbc.Row([
        start_button
    ], className='pt-3'),
    html.Div(id='results', children=results, style={'display': 'none'})
], style={"width": "99%"}, className='px-3 py-2')

scenario_1 = ['Yes', 75, 100, 'No', 10, 'No', dash.no_update, 'Yes', 40, 40,
              ['vor'], [], [{'label': x, 'value': x} for x in wea_modelle]]
scenario_2 = ['Yes', 100, 100, 'Yes', 10, 'No', dash.no_update, 'Yes', 40, 40,
              ['vor'], [], [{'label': x, 'value': x} for x in wea_modelle]]
scenario_3 = ['No', 100, 100, 'Yes', 10, 'No', dash.no_update, 'Yes', 40, 40,
              ['vor'], [], [{'label': x, 'value': x} for x in wea_modelle]]
scenario_4 = ['No', 100, 100, 'Yes', 10, 'Yes', 20, 'Yes', 40, 40,
              ['vor'], [], [{'label': x, 'value': x} for x in wea_modelle]]


@app.callback(
    [
        Output('example_switch', 'value'),
        Output('hours_slider', 'value'),
        Output('power_slider', 'value'),
        Output('storage_switch', 'value'),
        Output('budget_input', 'value'),
        Output('profit_switch', 'value'),
        Output('time_span_slider', 'value'),
        Output('growth_switch', 'value'),
        Output('biomass_input', 'value'),
        Output('solar_input', 'value'),
        Output('area_check', 'value'),
        Output('dual_list', 'selected'),
        Output('dual_list', 'available'),
    ],
    Input('scenario_dropdown', 'value')
)
def change_scenario(scenario):
    if scenario == 'Scenario 1':
        return scenario_1
    elif scenario == 'Scenario 2':
        return scenario_2
    elif scenario == 'Scenario 3':
        return scenario_3
    elif scenario == 'Scenario 4':
        return scenario_4
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('year_dropdown', 'disabled'),
        Output('year_dropdown', 'value')
    ],
    Input('example_switch', 'value')
)
def year_lock(value):
    if value == 'Yes':
        return False, '2019'
    elif value == 'No':
        return True, None
    else:
        pass


@app.callback(
    Output('map', 'figure'),
    [
        Input('dropdown_map', 'value')
    ]
)
def change_map(value):
    if value == 'Vor':
        return draw_vor()
    elif value == 'Pot':
        return draw_pot()
    else:
        pass


@app.callback(
    Output('graph_year', 'figure'),
    [
        Input('dropdown_data', 'value')
    ]
)
def change_graph(data):
    if data == 'ratio':
        return drawEE_percentage()
    elif data == 'absolute':
        return drawEE_absolute()


@app.callback(
    Output('time_span_slider', 'disabled'),
    Input('profit_switch', 'value')
)
def slider_lock(value):
    if value == 'Yes':
        return False
    elif value == 'No':
        return True
    else:
        pass


@app.callback(
    [
        Output('biomass_input', 'disabled'),
        Output('solar_input', 'disabled')
    ],
    Input('growth_switch', 'value')
)
def growth_input_lock(value):
    if value == 'Yes':
        return False, False
    elif value == 'No':
        return True, True
    else:
        pass


@app.callback(
    [
        Output('start_output', 'children'),
        Output('results', 'style'),
        Output('settings_page', 'style'),
        Output('start_button', 'children')
    ],
    Input('start_button', 'n_clicks'),
    [
        State('scenario_dropdown', 'value'),
        State('example_switch', 'value'),
        State('year_dropdown', 'value'),
        State('hours_slider', 'value'),
        State('power_slider', 'value'),
        State('storage_switch', 'value'),
        State('budget_input', 'value'),
        State('profit_switch', 'value'),
        State('time_span_slider', 'value'),
        State('growth_switch', 'value'),
        State('biomass_input', 'value'),
        State('solar_input', 'value'),
        State('area_check', 'value'),
        State('dual_list', 'leftLabel'),
        State('dual_list', 'available'),
        State('results', 'style'),
        State('settings_page', 'style')
    ]
)
def start_sim(n, scenario, exmpl_sw, year, hours, power, storage, budget, profit, profit_years, growth, bio, solar,
              area, dont_use, use, results, settings):
    if n == 0:
        raise PreventUpdate
    else:
        if year is not None:
            year_val = year
        else:
            year_val = 'Not given'

        if profit == 'No':
            calc_time = 'No calculation'
        else:
            calc_time = str(profit_years) + ' years'

        if budget is not None:
            budget_str = str(budget) + ' bn. €'
        else:
            budget_str = 'Not given'

        if bio is not None:
            bio_str = str(bio) + '%'
        else:
            bio_str = 'Not given'

        if solar is not None:
            solar_str = str(solar) + '%'
        else:
            solar_str = 'Not given'

        areas_str = ', '.join(area)
    '------------------------------------------------------------------------'
    'HEADER'
    def test_asd():
        main.META_EE_Anteil = 0.75  # Muss Decimal angegeben werden
        main.META_EE_Speicher = 1.0  # Grenzwert bis Speicher nicht mehr ausgebaut werden 100%
        main.META_year = 2020
        '- - - - - - - - - - - - - - - - - - - -'
        'BIO'
        main.META_biomasse = True
        main.META_expansionBio = 0.00  # in Prozent
        '- - - - - - - - - - - - - - - - - - - -'
        'PV'
        main.META_PV = True
        main.META_expansionPV = 0.00  # in Prozent
        '- - - - - - - - - - - - - - - - - - - -'
        'WKA'
        main.META_wind = True
        main.META_expansionWind = True
        main.META_be_planned_expansion = False

        main.META_faktorAusbauFlDist = 1.0  # in Kilometer
        main.META_VorFl = True  # True -> Ausbauflaeche wird genutzt
        main.META_PotFl = True  # True -> Ausbauflaeche wird genutzt
        main.META_repowering = False  # True -> Anlagen >10 Jahre oder <1500KW Leistung werden abgerissen und neu gebaut (2:1)

        main.META_ausbaubegrenzungsfaktor = 0.5  # WIRD NOCH BENÖTIGT. MOMENTAN OHNE FUNKTION
        main.META_negativ_Graph_methode = True  # True = Kompch False = Gildenstern
        main.META_windanalyse = False
        '- - - - - - - - - - - - - - - - - - - -'
        'Speicher'
        main.META_startcapacity = 0.8  # Angabe in Prozent wie voll die Speicher im Startpunkt sind
        main.META_strorage_safty_compansion = 1.20  # Wieviel safty Speicher ausgebaut werden soll zusätzlich

        main.META_speichervorAusbau = True  # True -> vor Ausbau Analyse beachtet Speicher
        main.META_storage_expansion = True  # True -> Speicher werden ausgebaut
        main.META_Laegerdorf = True
        main.META_max_compressed_air = 13500000000
        main.META_compressed_air = True
        '- - - - - - - - - - - - - - - - - - - -'
        'Database'
        main.META_DATA_generate_windenergy_plannendareas = False # True wenn die Liste erstellt werden soll
        main.META_DATA_verbrauch_komuliert = False  # True wenn die Liste erstellt werden soll
        print(main.META_DATA_verbrauch_komuliert, 'main.META_DATA_verbrauch_komuliert')
        main.META_DATA_DBWKAreload = False  # True wenn die DB der WKA Lastgänge erstellt werden soll
        main.META_DATA_DB_min_hight = 100  # Wert gibt die min höhe der WKA für die DB Lastgänge erstellt werden soll
        main.META_DATA_plannedAreas_potVor_getCoords = False  # True wenn die Ausbauflächen keine Standorte besitzen
        #                                           -> Wetterstationen werden ebenfalls hinzugefügt
        main.META_DATA_plannedAreas_potVor_getWeather = False  # True wenn die Ausbauflächen keine zugeordnete Wetterstation besitzen
        print(main.META_DATA_plannedAreas_potVor_getWeather, 'main.META_DATA_plannedAreas_potVor_getWeather')
        main.META_DATA_be_plannedWKA_getCoords = False  # True wenn die Coords zugeordnet werden müssen

        main.META_DATA_be_plannedWKA_getWeatherID = False  # True wenn die Weather ID zugeordnet werden muss
        main.META_DATA_be_plannedWKA_power = False  # True wenn die Leistung ausgerechnet werden muss
        main.META_DATA_pv_power = False  # True wenn die Leistung von PV erneut gerechnet werden muss
        main.META_DATA_wind_power = False  # True wenn die Leistung von Wind erneut gerechnet werden muss

    test_asd()
    main.re_simulation()

    if results['display'] == 'none' and settings['display'] == 'inline':

        return html.Div([

            '''html.B(),
            html.H4('Used settings:'),
            html.P('Scenario: ' + str(scenario)),
            html.P('Use example data: ' + str(exmpl_sw)),
            html.P('Selected year: ' + str(year_val)),
            html.P('Hours over threshold: ' + str(hours) + '%'),
            html.P('Power threshold: ' + str(power) + '%'),
            html.P('Use storage: ' + str(storage)),
            html.P('Budget: ' + str(budget_str)),
            html.P('Use profit: ' + str(profit)),
            html.P('Calculation period: ' + str(calc_time)),
            html.P('Use growth factor: ' + str(growth)),
            html.P('Biomass growth: ' + str(bio_str)),
            html.P('Solar growth: ' + str(solar_str)),
            html.P('Areas to use: ' + str(areas_str)),
            html.P('Models to use: ' + str(dont_use))'''

        ]), {'display': 'inline'}, {'display': 'none'}, 'Back'

    elif results['display'] == 'inline' and settings['display'] == 'none':
        return html.Div(), {'display': 'none'}, {'display': 'inline'}, 'Start'
    else:
        print('oops')
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
    # host='141.22.13.112'
