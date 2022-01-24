import os
import shutil
import time
import dash
import html as html
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table as dt
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from matplotlib import colors as mcolors
import main

print('Programmstart')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server

colors = mcolors.CSS4_COLORS
names = list(colors)
for i in names:
    if 'light' in i or 'white' in i:
        names.remove(i)

'''
df = pd.read_csv('data/GruenEnergie_2019_ausbau.csv', sep=';', decimal=',', encoding='latin1')
df['Datum'] = pd.to_datetime(df['Datum'])

# ----------------------------------------------------------------------------------------------------------------------

conv = df['Diff_EE_zu_Verb'].loc[df['Diff_EE_zu_Verb'] < 0].sum()
conv *= -1
df_sum = pd.DataFrame()
df_sum['Energiemenge'] = [df['Verbrauch_Gesamt'].sum() - conv, df['Erzeugung_PV'].sum(), conv]
df_sum['Art'] = ['Wind', 'Solar', 'Konventionell']
'''
# ----------------------------------------------------------------------------------------------------------------------

wea_modelle = pd.read_excel('data/WEA-Typen.xlsx')['Modell'].tolist()
wea_modelle = list(set(wea_modelle))
wea_modelle.pop(0)
wea_modelle.remove('v')

# ----------------------------------------------------------------------------------------------------------------------

'''
color_map = {}
for index, i in enumerate(areas_pot_df['Wetter-ID_Pot'].unique()):
    color_map[i] = names[index]
'''

table_df = pd.read_csv('data/table.csv', sep=';', decimal=',', encoding='utf-8')

'''def drawEE_percentage(sizing):
    return px.line(df, x="Datum", y='EE_Anteil', color=sizing,
                   title='Ratio Renewable Energy to Consumption').update_layout(
        template='plotly_dark', title_x=0.5).add_hline(y=1).update_traces(showlegend=True)'''


def coords_to_lat_lon(df, coords_header):
    def listFromStr(text, seperator):
        list_of_str = text.split(seperator)
        return list_of_str

    def editCoords_list(coords):
        lat_ = []
        lon_ = []
        for i in coords:
            i = str(i)
            i = i.replace('[', '')
            i = i.replace(']', '')
            i = i.replace('(', '')
            i = i.replace(')', '')
            i = i.replace("'", '')
            i = list(listFromStr(i, ', '))
            lat_.append(float(i[0]))
            lon_.append(float(i[1]))

        return lat_, lon_

    lat, lon = editCoords_list(df[coords_header].tolist())

    df['Latitude'] = lat
    df['Longitude'] = lon


def drawEE_percentage():
    fig = go.Figure()

    '''fig.add_trace(go.Scatter(x=df['Datum'], y=df['Verbrauch_Gesamt'], marker=dict(color='blue', opacity=0.7),
                             name="Verbrauch"))'''
    fig.add_trace(
        go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Percentage_true_with_gaps'], marker=dict(color='green'),
                   name="RE >= 100%"))
    fig.add_trace(
        go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Percentage_false_with_gaps'], marker=dict(color='red'),
                   name="RE < 100%"))
    fig.update_layout(template='plotly_dark', title='Ratio: Renewable Energy Production to Consumption', title_x=0.5,
                      xaxis_title="Date",
                      yaxis_title="RE Production / Consumption",
                      legend_title="Legend")
    fig.update_xaxes(dtick='M1')
    fig.add_hline(y=1)

    return fig


def drawEE_absolute():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Gesamt_true_with_gaps'], marker=dict(color='green'),
                   name="RE >= 100%"))
    fig.add_trace(
        go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Gesamt_false_with_gaps'], marker=dict(color='red'),
                   name="RE < 100%"))
    fig.add_trace(go.Scatter(x=df_analyse['Datum'], y=df_analyse['Verbrauch_Gesamt'], marker=dict(color='blue', opacity=0.2),
                             name="Consumption"))
    fig.update_layout(template='plotly_dark', title='Absolute Numbers', title_x=0.5,
                      xaxis_title="Date",
                      yaxis_title="Power (in kW)",
                      legend_title="Legend")
    fig.update_xaxes(dtick='M1')

    return fig


'''
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

    return px.scatter(df, x="Datum", y='Verbrauch_Gesamt').update_layout(
        template='plotly_dark').update_traces(showlegend=True)

    return fig


def draw_pie():
    return px.pie(df_sum, 'Art', 'Energiemenge', title='Used Energy').update_layout(
        template='plotly_dark', title_x=0.5)

'''


def draw_vor(sizing):
    df = df_ausbau_vor.copy()
    if sizing == 'Power':
        sizing = 'Leistung_inMW_Vor'
        df = df.loc[df['Leistung_inMW_Vor'] != 0]
    else:
        sizing = 'nettoFreieFlaeche_Vor'

    return px.scatter_mapbox(df, lat='Latitude', lon='Longitude', title='Simulated expansion',
                             # hover_name='ID_Weatherstation',
                             hover_data=['ID_Weatherstation_Vor', 'StadtVor', 'haVor', 'Anzahl WEAs_Vor', 'Anzahl_Vor',
                                         'Modell_Vor', 'nettoFreieFlaeche_Vor', 'Leistung_inMW_Vor', 'InvestKosten_inMio_Vor',
                                         'Latitude', 'Longitude'],
                             labels={
                                 'ID_Weatherstation_Vor': 'Weatherstation ID',
                                 "StadtVor": "Region",
                                 "Anzahl WEAs_Vor": "Wind turbines before expansion",
                                 "nettoFreieFlaeche_Vor": "Free area left (in ha)",
                                 'Modell_Vor': 'Used model',
                                 'Anzahl_Vor': 'Wind turbines after expansion',
                                 'Leistung_inMW_Vor': 'Power',
                                 'InvestKosten_inMio_Vor': 'Investment costs',
                                 'haVor': 'Total area (in ha)'
                             },
                             color='ID_Weatherstation_Vor', color_discrete_map={}, size=sizing, size_max=12,
                             zoom=6.3, center={'lat': 54.2, 'lon': 9.8}).update_layout(
        mapbox_style="open-street-map", template='plotly_dark', title_x=0.5, legend_title='Wetter ID'
    )


def draw_pot(sizing):
    df = df_ausbau_pot.copy()
    if sizing == 'Power':
        sizing = 'Leistung_inMW_Pot'
        df = df.loc[df['Leistung_inMW_Pot'] != 0]
    else:
        sizing = 'nettoFreieFlaeche_Pot'

    return px.scatter_mapbox(df, lat='Latitude', lon='Longitude', title='Simulated expansion',
                             # hover_name='StadtPot',
                             hover_data=['ID_Weatherstation_Pot', 'StadtPot', 'haPot', 'Anzahl WEAs_Pot', 'Anzahl_Pot',
                                         'Modell_Pot', 'nettoFreieFlaeche_Pot', 'Leistung_inMW_Pot', 'InvestKosten_inMio_Pot',
                                         'Latitude', 'Longitude'],
                             labels={
                                 'ID_Weatherstation_Pot': 'Weatherstation ID',
                                 "StadtPot": "Region",
                                 "Anzahl WEAs_Pot": "Wind turbines before expansion",
                                 "nettoFreieFlaeche_Pot": "Free area left (in ha)",
                                 'Modell_Pot': 'Used model',
                                 'Anzahl_Pot': 'Wind turbines after expansion',
                                 'Leistung_inMW_Pot': 'Power',
                                 'InvestKosten_inMio_Pot': 'Investment costs',
                                 'haPot': 'Total area (in ha)'
                             },
                             color='ID_Weatherstation_Pot', color_discrete_map={}, size=sizing, size_max=12,
                             zoom=6.3, center={'lat': 54.2, 'lon': 9.8},
                             ).update_layout(
        mapbox_style="open-street-map", template='plotly_dark', title_x=0.5, legend_title='Wetter ID'
    )


def make_monthly_table():
    return dt.DataTable(columns=[{"name": i, "id": i} for i in df_month_report.columns],
                        tooltip_header={i: i for i in df_month_report.columns},
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0,
                            'height': 'auto'
                        },
                        data=df_month_report.to_dict('records'), cell_selectable=False,
                        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
                        tooltip_data=[
                            {
                                column: {'value': str(value), 'type': 'markdown'}
                                for column, value in row.items()
                            } for row in df_month_report.to_dict('records')
                        ],
                        style_header={
                            'backgroundColor': 'rgb(10, 10, 10)',
                            'color': 'white',
                        },
                        style_data={
                            'backgroundColor': 'rgb(40, 40, 40)',
                            'color': 'white'
                        },
                        css=[{
                            'selector': '.dash-table-tooltip',
                            'rule': 'background-color: grey; font-family: monospace; color: white'
                        }],
                        style_data_conditional=(
                            [
                                {
                                    'if': {
                                        'column_id': 'Wind (TWh)',
                                        'filter_query': '{{Wind (TWh)}} = {}'.format(
                                            df_month_report['Wind (TWh)'].nlargest(2).tolist()[1])
                                    },
                                    'backgroundColor': '#c9ffba',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'Wind (TWh)',
                                        'filter_query': '{{Wind (TWh)}} = {}'.format(
                                            df_month_report['Wind (TWh)'].min())
                                    },
                                    'backgroundColor': '#ffbaba',
                                    'color': 'black'
                                },

                                # -----------------------------------------------------------------------------

                                {
                                    'if': {
                                        'column_id': 'PV (TWh)',
                                        'filter_query': '{{PV (TWh)}} = {}'.format(
                                            df_month_report['PV (TWh)'].nlargest(2).tolist()[1])
                                    },
                                    'backgroundColor': '#c9ffba',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'PV (TWh)',
                                        'filter_query': '{{PV (TWh)}} = {}'.format(
                                            df_month_report['PV (TWh)'].min())
                                    },
                                    'backgroundColor': '#ffbaba',
                                    'color': 'black'
                                },

                                # -----------------------------------------------------------------------------

                                {
                                    'if': {
                                        'column_id': 'Combined RE (TWh)',
                                        'filter_query': '{{Combined RE (TWh)}} = {}'.format(
                                            df_month_report['Combined RE (TWh)'].nlargest(2).tolist()[1])
                                    },
                                    'backgroundColor': '#c9ffba',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'Combined RE (TWh)',
                                        'filter_query': '{{Combined RE (TWh)}} = {}'.format(
                                            df_month_report['Combined RE (TWh)'].min())
                                    },
                                    'backgroundColor': '#ffbaba',
                                    'color': 'black'
                                },

                                # -----------------------------------------------------------------------------

                                {
                                    'if': {
                                        'column_id': 'Consumption (TWh)',
                                        'filter_query': '{{Consumption (TWh)}} = {}'.format(
                                            df_month_report['Consumption (TWh)'].nlargest(2).tolist()[1])
                                    },
                                    'backgroundColor': '#ffbaba',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'Consumption (TWh)',
                                        'filter_query': '{{Consumption (TWh)}} = {}'.format(
                                            df_month_report['Consumption (TWh)'].min())
                                    },
                                    'backgroundColor': '#c9ffba',
                                    'color': 'black'
                                },

                                # -----------------------------------------------------------------------------

                                {
                                    'if': {
                                        'column_id': 'Deficit/Conventional (TWh)',
                                        'filter_query': '{{Deficit/Conventional (TWh)}} = {}'.format(
                                            df_month_report['Deficit/Conventional (TWh)'].nlargest(2).tolist()[1])
                                    },
                                    'backgroundColor': '#ffbaba',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'Deficit/Conventional (TWh)',
                                        'filter_query': '{{Deficit/Conventional (TWh)}} = {}'.format(
                                            df_month_report['Deficit/Conventional (TWh)'].min())
                                    },
                                    'backgroundColor': '#c9ffba',
                                    'color': 'black'
                                },

                                # -----------------------------------------------------------------------------

                                {
                                    'if': {
                                        'column_id': 'Hours 100%',
                                        'filter_query': '{{Hours 100%}} = {}'.format(
                                            df_month_report['Hours 100%'].nlargest(2).tolist()[1])
                                    },
                                    'backgroundColor': '#c9ffba',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'Hours 100%',
                                        'filter_query': '{{Hours 100%}} = {}'.format(
                                            df_month_report['Hours 100%'].min())
                                    },
                                    'backgroundColor': '#ffbaba',
                                    'color': 'black'
                                },

                            ]
                        ),
                        )


def make_cost_table():
    return dt.DataTable(columns=[{"name": i, "id": i} for i in df_cost_report.columns],
                        tooltip_header={i: i for i in df_cost_report.columns},
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0,
                            'height': 'auto'
                        },
                        data=df_cost_report.to_dict('records'), cell_selectable=False,
                        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
                        tooltip_data=[
                            {
                                column: {'value': str(value), 'type': 'markdown'}
                                for column, value in row.items()
                            } for row in df_cost_report.to_dict('records')
                        ],
                        style_header={
                            'backgroundColor': 'rgb(10, 10, 10)',
                            'color': 'white',
                        },
                        style_data={
                            'backgroundColor': 'rgb(40, 40, 40)',
                            'color': 'white'
                        },
                        css=[{
                            'selector': '.dash-table-tooltip',
                            'rule': 'background-color: grey; font-family: monospace; color: white'
                        }],
                        )


def make_datasheet_table():
    return dt.DataTable(columns=[{"name": i, "id": i} for i in df_datasheet.columns],
                        tooltip_header={i: i for i in df_datasheet.columns},
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0,
                            'height': 'auto'
                        },
                        data=df_datasheet.to_dict('records'), cell_selectable=False,
                        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
                        tooltip_data=[
                            {
                                column: {'value': str(value), 'type': 'markdown'}
                                for column, value in row.items()
                            } for row in df_datasheet.to_dict('records')
                        ],
                        style_header={
                            'backgroundColor': 'rgb(10, 10, 10)',
                            'color': 'white',
                        },
                        style_data={
                            'backgroundColor': 'rgb(40, 40, 40)',
                            'color': 'white'
                        },
                        css=[{
                            'selector': '.dash-table-tooltip',
                            'rule': 'background-color: grey; font-family: monospace; color: white'
                        }],
                        ),


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
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=False
    ),
], className="radio-group")

scenario_dropdown = html.Div([
    dcc.Dropdown(
        id='scenario_dropdown',
        options=[
            {'label': 'Task 1', 'value': 'Scenario 1'},
            {'label': 'Task 2', 'value': 'Scenario 2'},
            {'label': 'Task 3', 'value': 'Scenario 3'},
            {'label': 'No expasion', 'value': 'Scenario 4'},
            {'label': 'Fast simulation', 'value': 'Scenario 5'},
            {'label': 'Economic solution', 'value': 'Scenario 6'},
        ],
        value='Scenario 1',
        style={"textAlign": "left", 'color': 'black'}
    )
])

year_dropdown = html.Div([
    dcc.Dropdown(
        id='year_dropdown',
        options=[
            {'label': '2019', 'value': 2019},
            {'label': '2020', 'value': 2020}
        ],
        value=2019,
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
            ], width=4),
            dbc.Col([], width=1),
            dbc.Col([
                dbc.Button('Explanation', id='scenario_modal_button'),
                dbc.Modal(
                    [
                        dbc.ModalHeader(children=[], close_button=True, id='scenario_modal_header'),
                        dbc.ModalBody(id='scenario_modal_body'),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close",
                                id="close-centered",
                                className="ms-auto",
                                n_clicks=0,
                            )
                        ),
                    ],
                    id="scenario_modal",
                    centered=True,
                    is_open=False,
                )
            ], width=4)
        ], className='pb-3', justify="center", align='center'),
        dbc.Row([
            dbc.Col([
                html.P('Use own data?'),
                example_switch
            ], width=3),
            dbc.Col([
                html.P('Year:'),
                year_dropdown
            ], width=3)
        ], className='py-3 px-3', justify="around"),
        dbc.Row([

        ], className='py-3', justify="center"),
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# eisman settings

eisman_switch = html.Div([
    dbc.RadioItems(
        id="eisman_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=False
    ),
], className="radio-group")

eisman_wind_slider = html.Div([
    dcc.RangeSlider(
        id='eisman_wind_slider',
        min=0,
        max=35,
        step=0.5,
        marks={
            x: {'label': str(x) + 'm/s'} for x in range(0, 35, 5)
        },
        value=[13, 19, 25],
        pushable=0.5,
        tooltip={"placement": "bottom", "always_visible": True}
    )
])

eisman_percentage_slider = html.Div([
    dcc.RangeSlider(
        id='eisman_percentage_slider',
        min=0,
        max=100,
        step=1,
        marks={
            x: {'label': str(x) + '%'} for x in range(0, 100, 10)
        },
        value=[40, 70, 100],
        pushable=1,
        tooltip={"placement": "bottom", "always_visible": True}
    )
])

eisman_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('Eisman Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Use Eisman?'),
                eisman_switch
            ], width=4)
        ], className='pb-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Wind speeds to regulate at:'),
                eisman_wind_slider
            ], width=10)
        ], className='pb-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Power regulation loss:'),
                eisman_percentage_slider
            ], width=10)
        ], className='py-3', justify="center"),
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# biomass/solar_input settings


solar_switch = html.Div([
    dbc.RadioItems(
        id="solar_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=True
    ),
], className="radio-group")

solar_input = html.Div([
    dbc.Input(id='solar_input', placeholder='Type in a factor...', type="number", min=0,
              max=1000, step=1)
])

biomass_switch = html.Div([
    dbc.RadioItems(
        id="biomass_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=True
    ),
], className="radio-group")

biomass_input = html.Div([
    dbc.Input(id='biomass_input', placeholder='Type in a factor...', type="number", min=0,
              max=1000, step=1)
])

biomass_solar_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('Biomass/Solar Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Use biomass?'),
                biomass_switch
            ], width=6),
            dbc.Col([
                html.P('Use solar power?'),
                solar_switch
            ], width=6)
        ], className='pb-3 px-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(['Biomass growth:', html.Br(), '(in %)']),
                biomass_input
            ], width=5),
            dbc.Col([
                html.P(['Solar growth:', html.Br(), '(in %)']),
                solar_input
            ], width=5)
        ], className='py-3 px-3', justify="around"),
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# wind settings


wind_expansion_switch = html.Div([
    dbc.RadioItems(
        id="wind_expansion_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=True
    ),
], className="radio-group")

planned_wind_switch = html.Div([
    dbc.RadioItems(
        id="planned_wind_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=True
    ),
], className="radio-group")

wind_hours_slider = html.Div([
    dcc.Slider(
        id='wind_hours_slider',
        min=0,
        max=100,
        value=75,
        step=1,
        marks={
            x: {'label': str(x) + '%'} for x in range(0, 100, 10)
        },
        tooltip={"placement": "bottom", "always_visible": True},
    )
])

methods_wind_check = html.Div([
    dcc.Checklist(
        id='methods_wind_check',
        options=[
            {'label': 'Vorranggebiete', 'value': 'vor'},
            {'label': 'Potentialflächen', 'value': 'pot'},
        ],
        value=['vor'],
        inputStyle={"margin-left": "20px", 'margin-right': "5px"}
    )
])

wind_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('Wind Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Expand wind energy?'),
                wind_expansion_switch
            ], width=6),
            dbc.Col([
                html.P('Use planned wind turbines?'),
                planned_wind_switch
            ], width=6)
        ], className='pb-3 px-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(['Expand wind until:', html.Br(), '(percentage of hours over 100% RE per year)']),
                wind_hours_slider
            ], width=10)
        ], className='py-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P('Choose expansion options:'),
                methods_wind_check
            ], width=12)
        ], className='py-3', justify="around"),
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# storage settings

storage_switch = html.Div([
    dbc.RadioItems(
        id="storage_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=True
    ),
], className="radio-group")

storage_expansion_switch = html.Div([
    dbc.RadioItems(
        id="storage_expansion_switch",
        className="btn-group",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-secondary",
        labelCheckedClassName="active",
        options=[
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=False
    ),
], className="radio-group")

storage_expansion_slider = html.Div([
    dcc.Slider(
        id='storage_expansion_slider',
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

start_capacity_slider = html.Div([
    dcc.Slider(
        id='start_capacity_slider',
        min=0,
        max=100,
        step=1,
        value=60,
        marks={
            x: {'label': str(x) + '%'} for x in range(0, 100, 10)
        },
        tooltip={"placement": "bottom", "always_visible": True},
    )
])

safety_padding_slider = html.Div([
    dcc.Slider(
        id='safety_padding_slider',
        min=0,
        max=50,
        step=0.5,
        value=0.5,
        marks={
            x: {'label': str(x) + '%'} for x in range(0, 50, 5)
        },
        tooltip={"placement": "bottom", "always_visible": True},
    )
])

storage_options_check = html.Div([
    dcc.Checklist(
        id='storage_options_check',
        options=[
            {'label': 'Existing storages', 'value': 'existing'},
            {'label': 'Laegerdorf', 'value': 'laegerdorf'},
            {'label': 'Compressed air', 'value': 'air'}
        ],
        value=['existing', 'laegerdorf', 'air'],
        inputStyle={"margin-left": "20px", 'margin-right': "5px"}
    )
])

storage_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('Storage Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Use Storage?'),
                storage_switch
            ], width=6),
            dbc.Col([
                html.P('Expand storage?'),
                storage_expansion_switch
            ], width=6)
        ], className='py-3 px-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(
                    'Start capacity:', id='start_capacity_tt',
                    style={"textDecoration": "underline", "cursor": "pointer"}
                ),
                dbc.Tooltip(
                    'To what extend should the storages be filled up at the start of the year',
                    target='start_capacity_tt'
                ),
                start_capacity_slider
            ], width=10)
        ], className='py-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(
                    ['Expand storage until:', html.Br(), '(percentage of hours over 100% RE per year)'],
                    id='storage_expansion_text',
                    style={"textDecoration": "underline", "cursor": "pointer"}
                ),
                dbc.Modal([
                    dbc.ModalHeader('Storage expansion', close_button=True),
                    dbc.ModalBody(
                        'What should be the final percentage of hours over 100% renewable energy, storages will be expanded '
                        'after the value for wind is reached (see wind settings).'),
                ], id="storage_expansion_modal", centered=True, is_open=False,
                ),
                storage_expansion_slider
            ], width=10)
        ], className='py-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P(
                    'Safety padding (in %):', id='safety_padding_tt',
                    style={"textDecoration": "underline", "cursor": "pointer"}
                ),
                dbc.Tooltip(
                    'This option will create a safety padding for expanding storage. For example if the minimum '
                    'amount of capacity needed to reach the earlier determined hour threshold is 100GWh, you can '
                    'determine a safety padding of 20% and the programm will expand the storage to 120GWh '
                    '(more budget needed, but more realistic)',
                    target='safety_padding_tt'
                ),
                safety_padding_slider
            ], width=10)
        ], className='py-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(
                    'Choose storage options:', id='storage_options_tt',
                    style={"textDecoration": "underline", "cursor": "pointer"}
                ),
                dbc.Tooltip(
                    'Existing storages: Right now the only existing storage used in the simulation is the '
                    'water pump storage in "Geesthacht". Only operational costs will be considered for this storage.\n'
                    'Laegerdorf: A planned water pump storage located in Schleswig-Holstein. Building and operational '
                    'costs will be considered for this storage.\n'
                    'Compressed air: This storage technology will probably be indispensable for most scenarios. '
                    'With an estimated capacity potential of 13.5TWh in Schleswig-Holstein it has the necessary '
                    'capacity for long energy droughts.',
                    target='storage_options_tt'
                )
            ], width='auto'),
            dbc.Col([
                storage_options_check
            ], width=12)
        ], className='py-3', justify="around")
    ])
], className='text-center p-1')

# ----------------------------------------------------------------------------------------------------------------------
# app layout

start_button = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div(children=[html.P('The simulation might take up to 10 minutes'),
                               html.B(),
                               html.P('Do not press the button twice or all simulation progress will be lost!!!')],
                     id='start_output'),
            dbc.Button('Start', id='start_button', n_clicks=0, disabled=False),
        ])
    ], className='py-3', justify='center'),
    dbc.Row([
        dbc.Col([
            html.Div(id='spinner_div')
        ])
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
                dbc.Progress(id="progress")
            ])
        ])
    ], justify='center')
], className='text-center')

support_button = html.Div([
    dbc.Button('Memory: Start', id='support_button', n_clicks=0, disabled=False, style={'display': 'none'}),
], className='text-center')

download_button = html.Div([
    dbc.Button('Download Results', id='download_button'),
    dcc.Download(id='download_component')
], className='text-center')

settings_children = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('RE-Simulation™')
                ])
            ], className='text-center')
        ], width=11)
    ], justify='center', className='pb-1'),
    dbc.Row([
        dbc.Col([
            general_settings,
            eisman_settings
        ], className='mt-1'),
        dbc.Col([
            biomass_solar_settings,
            wind_settings
        ], className='mt-1'),
        dbc.Col([
            storage_settings
        ], className='mt-1')
    ], className='px-3 py-1', justify='center')
])

results = html.Div([
    dbc.Row([
        dbc.Card([
            dbc.CardHeader([
                html.H3('Simulation results:', style={"text-decoration": 'underline'})
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4('Energy Overview'),
                        html.Div(id='data_sheet')
                    ])
                ], className='py-3'),
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
                ], className='py-3'),
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
                    ], width=1),
                    dbc.Col([
                        html.P('Sizing:'),
                        dcc.Dropdown(id='dropdown_map_size',
                                     options=[
                                         {'label': 'Power', 'value': 'Power'},
                                         {'label': 'Free area', 'value': 'Area'}
                                     ],
                                     value='Power',
                                     style={"textAlign": "left", 'color': 'black'}
                                     )
                    ], width=1)
                ], className='pt-3'),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='map')
                    ], width=6),
                    dbc.Col([

                    ], width=6)
                ], className='py-3', justify="between"),
                dbc.Row([
                    dbc.Col([
                        html.H4('Monthly Overview', style={"text-decoration": 'underline'}),
                        html.Div(id='monthly_table')
                    ])
                ], className='py-3'),
                dbc.Row([
                    dbc.Col([
                        html.H4('Costs Overview', style={"text-decoration": 'underline'}),
                        html.Div(id='costs')
                    ])
                ], className='py-3'),
                dbc.Row([
                    download_button
                ], className='py-3', justify='center')
            ])
        ], inverse=True, className='text-center p-1')
    ], className='px-3 py-1')
])

app.layout = html.Div([
    html.Div(id='settings_page', children=settings_children, style={'display': 'inline'}),
    dbc.Row([
        start_button
    ], className='py-3', justify='center'),
    html.Div(id='results', children=results, style={'display': 'none'}),
    support_button
], style={"width": "99%"}, className='px-3 py-2')

scenario_1 = [False, True, [13, 19, 25], [40, 70, 100], True, True, 5, 5, True, True, 75, ['vor', 'pot'], False, False, 0, 0, []]
scenario_2 = [False, True, [13, 19, 25], [40, 70, 100], True, True, 5, 5, True, True, 75, ['vor', 'pot'], True, True, 20, 0,
              ['existing', 'laegerdorf', 'air']]
scenario_3 = [True, True, [13, 19, 25], [40, 70, 100], True, True, 5, 5, True, True, 75, ['vor', 'pot'], True, True, 20, 0,
              ['existing', 'laegerdorf', 'air']]
scenario_4 = [False, False, [13, 19, 25], [40, 70, 100], True, True, 5, 5, False, True, 0, [], True, False, 20, 0,
              ['existing']]
scenario_5 = [False, False, [13, 19, 25], [40, 70, 100], True, True, 0, 0, False, False, 75, [], False, False, 0, 0, []]
scenario_6 = [False, True, [13, 19, 25], [40, 70, 100], True, True, 5, 5, True, True, 75, [], True, True, 20, 0,
              ['existing', 'laegerdorf', 'air']]


@app.callback(
    [
        Output('example_switch', 'value'),
        Output('eisman_switch', 'value'),
        Output('eisman_wind_slider', 'value'),
        Output('eisman_percentage_slider', 'value'),
        Output('biomass_switch', 'value'),
        Output('solar_switch', 'value'),
        Output('biomass_input', 'value'),
        Output('solar_input', 'value'),
        Output('wind_expansion_switch', 'value'),
        Output('planned_wind_switch', 'value'),
        Output('wind_hours_slider', 'value'),
        Output('methods_wind_check', 'value'),
        Output('storage_switch', 'value'),
        Output('storage_expansion_switch', 'value'),
        Output('start_capacity_slider', 'value'),
        Output('safety_padding_slider', 'value'),
        Output('storage_options_check', 'value'),
    ],
    Input('scenario_dropdown', 'value'),
    State('scenario_dropdown', 'options', )
)
def change_scenario(value, options):
    if value == options[0]['value']:
        return scenario_1
    elif value == options[1]['value']:
        return scenario_2
    elif value == options[2]['value']:
        return scenario_3
    elif value == options[3]['value']:
        return scenario_4
    elif value == options[4]['value']:
        return scenario_5
    else:
        raise PreventUpdate


# scenario modal texts
tt_1 = 'Goal of task 1 is to achieve 100% RE production for 75% of the time. The means to achieve this goal ' \
       'are existing biomass plants, solar panels and wind turbines, which can all be expanded upon. Power storages should not ' \
       'be used to complete this task. The goal should be reached within an allowed budget of 10 Bn. €.'

tt_2 = 'Goal of task 2 is to achieve 100% RE production for 100% of the time. To accomplish this goal wind turbines and power ' \
       'storages are allowed to be used and expanded upon. Like before the intended budget for a successful completion are 10 bn. €.'

tt_3 = 'Goal of task 3 is to achieve 100% RE production for 100% of the time, just like task 2. For this simulation the user ' \
       'should use their own data (see upload button). The means to achieve this goal are the same as in task 2.'

tt_4 = 'This scenario will simulate the current state of renewable energy production by neither expanding upon the energy ' \
       'production nor the power storages. It will use existing power storages and existing means of power production ' \
       '(will include planned wind turbines).'

tt_5 = 'fürn wengert :*'


@app.callback(
    Output('storage_expansion_modal', 'is_open'),
    Input('storage_expansion_text', 'n_clicks'),
    State('storage_expansion_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [
        Output('scenario_modal', 'is_open'),
        Output('scenario_modal_header', 'children'),
        Output('scenario_modal_body', 'children')
    ],
    [
        Input("scenario_modal_button", "n_clicks"),
        Input("close-centered", "n_clicks")
    ],
    [
        State("scenario_modal", "is_open"),
        State('scenario_dropdown', 'value'),
        State('scenario_dropdown', 'options')
    ]
)
def scenario_tooltip(n1, n2, is_open, scenario, options):
    if scenario == options[0]['value']:
        picked = tt_1
    elif scenario == options[1]['value']:
        picked = tt_2
    elif scenario == options[2]['value']:
        picked = tt_3
    elif scenario == options[3]['value']:
        picked = tt_4
    elif scenario == options[4]['value']:
        picked = tt_5
    else:
        print('modal no scenario was picked')
        picked = ''
    if n1 or n2:
        return not is_open, scenario, picked
    return is_open, scenario, picked


def slider_intervals(value):
    if value >= 90:
        return {x: {'label': str(x) + '%'} for x in range(value, 100, 2)}
    elif value >= 50:
        return {x: {'label': str(x) + '%'} for x in range(value, 100, 5)}
    elif value < 50:
        return {x: {'label': str(x) + '%'} for x in range(value, 100, 10)}
    else:
        pass


@app.callback(
    [
        Output('storage_expansion_slider', 'min'),
        Output('storage_expansion_slider', 'marks'),
        Output('storage_expansion_slider', 'value'),
    ],
    [
        Input('wind_hours_slider', 'value'),
        Input('scenario_dropdown', 'value')
    ],
    [
        State('scenario_dropdown', 'options')
    ]
)
def lock_storage_expansion(value, scenario, options):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'scenario_dropdown':
        if scenario == options[0]['value']:
            return value, slider_intervals(value), 0
        elif scenario == options[1]['value']:
            return value, slider_intervals(value), 100
        elif scenario == options[2]['value']:
            return value, slider_intervals(value), 100
        elif scenario == options[3]['value']:
            return value, slider_intervals(value), 0
        elif scenario == options[4]['value']:
            return value, slider_intervals(value), 0
        else:
            print('slider scenario error')
            raise PreventUpdate
    else:
        return value, slider_intervals(value), value


@app.callback(
    Output('spinner_div', 'children'),
    [
        Input('start_button', 'n_clicks'),
        Input('start_button', 'children')
    ],
    State('support_button', 'n_clicks')
)
def spinner(n, value, n_support):
    if n == 0:
        return dash.no_update
    elif n > n_support:
        if value == 'Start':
            return dbc.Button(
                [dbc.Spinner(size="sm"), " Simulating..."],
                color="secondary",
                disabled=True,
            )
        elif value == 'Back':
            return html.Div()
    elif value == 'Back':
        return html.Div()
    else:
        return dash.no_update


@app.callback(
    [
        Output('year_dropdown', 'options'),
        Output('year_dropdown', 'value')
    ],
    Input('example_switch', 'value')
)
def year_lock(value):
    if not value:
        return [{'label': '2019', 'value': 2019}, {'label': '2020', 'value': 2020}], 2019
    elif value:
        return [{'label': str(x), 'value': x} for x in range(2000, 2100, 1)], None
    else:
        pass


@app.callback(
    Output('wind_hours_slider', 'disabled'),
    Input('wind_expansion_switch', 'value')
)
def disable_wind_expansion(value):
    if value:
        return False
    elif not value:
        return True
    else:
        pass


@app.callback(
    [
        Output('eisman_wind_slider', 'disabled'),
        Output('eisman_percentage_slider', 'disabled')
    ],
    Input('eisman_switch', 'value')
)
def disable_eisman(value):
    if value:
        return False, False
    elif not value:
        return True, True
    else:
        pass


@app.callback(
    [
        Output('start_capacity_slider', 'disabled'),
        Output('storage_expansion_slider', 'disabled'),
        Output('safety_padding_slider', 'disabled'),
    ],
    [
        Input('storage_switch', 'value'),
        Input('storage_expansion_switch', 'value'),
    ]
)
def disable_storage(storage, expansion):
    if storage and expansion:
        return False, False, False
    elif storage and not expansion:
        return False, True, True
    elif not storage:
        return True, True, True
    else:
        pass


@app.callback(
    Output('monthly_table', 'children'),
    [
        Input('start_button', 'children')
    ]
)
def montly_table(value):
    if value == 'Start':
        return dash.no_update
    elif value == 'Back':
        return make_monthly_table()
    else:
        print('TABLE ERROR!!!')
        return dash.no_update


@app.callback(
    Output('data_sheet', 'children'),
    [
        Input('start_button', 'children')
    ]
)
def datasheet_table(value):
    if value == 'Start':
        return dash.no_update
    elif value == 'Back':
        return make_datasheet_table()
    else:
        print('TABLE ERROR!!!')
        return dash.no_update


@app.callback(
    Output('costs', 'children'),
    [
        Input('start_button', 'children')
    ]
)
def montly_table(value):
    if value == 'Start':
        return dash.no_update
    elif value == 'Back':
        return make_cost_table()
    else:
        print('TABLE ERROR!!!')
        return dash.no_update


@app.callback(
    Output('map', 'figure'),
    [
        Input('dropdown_map', 'value'),
        Input('dropdown_map_size', 'value'),
        Input('start_button', 'children')
    ]

)
def change_map(area, size, children):
    if children == 'Start':
        return dash.no_update
    elif children == 'Back':
        if area == 'Vor':
            return draw_vor(size)
        elif area == 'Pot':
            return draw_pot(size)
        else:
            pass


@app.callback(
    Output('graph_year', 'figure'),
    [
        Input('dropdown_data', 'value'),
        Input('start_button', 'children')
    ]
)
def change_graph(data, children):
    if children == 'Start':
        return dash.no_update
    elif children == 'Back':
        if data == 'ratio':
            return drawEE_percentage()
        elif data == 'absolute':
            return drawEE_absolute()
        else:
            pass


@app.callback(
    Output("download_component", "data"),
    Input("download_button", "n_clicks"),
    prevent_initial_call=True,
)
def download(n_clicks):
    return dcc.send_file(zip_folder + '.zip')


@app.callback(
    Output('biomass_input', 'disabled'),
    Input('biomass_switch', 'value')
)
def growth_input_lock(value):
    if value:
        return False
    elif not value:
        return True
    else:
        pass


@app.callback(
    Output('solar_input', 'disabled'),
    Input('solar_switch', 'value')
)
def growth_input_lock(value):
    if value:
        return False
    elif not value:
        return True
    else:
        pass


@app.callback(
    Output('support_button', 'n_clicks'),
    Input('start_button', 'n_clicks')
)
def click_support_button(n):
    time.sleep(1)
    return n


@app.callback(
    [
        Output('start_output', 'children'),
        Output('results', 'style'),
        Output('settings_page', 'style'),
        Output('start_button', 'children'),
    ],
    [
        Input('support_button', 'n_clicks')
    ],
    [
        State('example_switch', 'value'),
        State('year_dropdown', 'value'),
        State('wind_hours_slider', 'value'),
        State('biomass_switch', 'value'),
        State('biomass_input', 'value'),
        State('solar_switch', 'value'),
        State('solar_input', 'value'),
        State('wind_expansion_switch', 'value'),
        State('planned_wind_switch', 'value'),
        State('methods_wind_check', 'value'),
        State('storage_switch', 'value'),
        State('storage_expansion_switch', 'value'),
        State('storage_expansion_slider', 'value'),
        State('start_capacity_slider', 'value'),
        State('safety_padding_slider', 'value'),
        State('storage_options_check', 'value'),
        State('eisman_switch', 'value'),
        State('eisman_wind_slider', 'value'),
        State('eisman_percentage_slider', 'value'),
        State('results', 'style'),
        State('settings_page', 'style'),
    ],
)
def start_sim(n, exmpl_sw, year, wind_expansion_value, bio_sw, bio_inp, solar_sw, solar_inp, wind_expansion,
              planned_wind, methods_wind, storage_sw, storage_expansion_sw, storage_expansion_value,
              start_capacity_value, safety_padding_value, storage_options, eisman_sw, eisman_wind, eisman_percentage,
              results_value, settings_value):
    if n == 0:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    '------------------------------------------------------------------------'
    'HEADER'

    if results_value['display'] == 'none' and settings_value['display'] == 'inline':

        list_of_files = os.listdir('REE_AnalyseCompleted')
        full_path = ["REE_AnalyseCompleted/{0}".format(x) for x in list_of_files]

        if len(list_of_files) >= 10:
            oldest_file = min(full_path, key=os.path.getctime)
            shutil.rmtree(oldest_file)

        '- - - - - - - - - - - - - - - - - - - -'
        main.META_EE_Anteil = wind_expansion_value / 100  # Muss Decimal angegeben werden
        main.META_EE_Speicher = storage_expansion_value / 100  # Grenzwert bis Speicher nicht mehr ausgebaut werden 100%
        main.META_year = year
        '- - - - - - - - - - - - - - - - - - - -'
        'BIO'
        main.META_biomasse = bio_sw
        main.META_expansionBio = bio_inp / 100  # in Prozent
        '- - - - - - - - - - - - - - - - - - - -'
        'PV'
        main.META_PV = solar_sw
        main.META_expansionPV = solar_inp / 100  # in Prozent
        '- - - - - - - - - - - - - - - - - - - -'
        'Eisman'
        main.META_eisman = eisman_sw
        main.META_first_wind_limit = eisman_wind[0]
        main.META_sec_wind_limit = eisman_wind[1]
        main.META_third_wind_limit = eisman_wind[2]
        main.META_first_power_limit = (100 - eisman_percentage[0]) / 100
        main.META_sec_power_limit = (100 - eisman_percentage[1]) / 100
        main.META_third_power_limit = (100 - eisman_percentage[2]) / 100
        '- - - - - - - - - - - - - - - - - - - -'
        'WKA'
        main.META_wind = True
        main.META_expansionWind = wind_expansion
        main.META_be_planned_expansion = planned_wind

        main.META_faktorAusbauFlDist = 1.0  # in Kilometer
        main.META_VorFl = 'vor' in methods_wind  # True -> Ausbauflaeche wird genutzt
        main.META_PotFl = 'pot' in methods_wind  # True -> Ausbauflaeche wird genutzt
        main.META_repowering = 'repowering' in methods_wind  # True -> Anlagen >10 Jahre oder <1500KW Leistung werden abgerissen und neu gebaut (2:1)

        main.META_ausbaubegrenzungsfaktor = 0.5  # WIRD NOCH BENÖTIGT. MOMENTAN OHNE FUNKTION
        main.META_negativ_Graph_methode = True  # True = Kompch False = Gildenstern
        main.META_windanalyse = False
        '- - - - - - - - - - - - - - - - - - - -'
        'Speicher'
        main.META_use_storage = storage_sw
        main.META_startcapacity = start_capacity_value / 100  # Angabe in Prozent wie voll die Speicher im Startpunkt sind
        main.META_storage_safety_padding = safety_padding_value / 100  # Wieviel safty Speicher ausgebaut werden soll zusätzlich

        main.META_storage_before_expansion = 'existing' in storage_options  # True -> vor Ausbau Analyse beachtet Speicher
        main.META_storage_expansion = storage_expansion_sw  # True -> Speicher werden ausgebaut
        main.META_Laegerdorf = 'laegerdorf' in storage_options
        main.META_max_compressed_air = 13500000000
        main.META_compressed_air = 'air' in storage_options
        '- - - - - - - - - - - - - - - - - - - -'
        'Database'
        main.META_DATA_generate_windenergy_plannendareas = False  # True wenn die Liste erstellt werden soll
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
        main.META_DATA_eisman = False

        global exportFolder
        global list_files
        global zip_folder
        # exportFolder, cost_report, dataframe_expansion_area, export_simulation_bevor_expansion, SimulationEE_after_expansion
        exportFolder, zip_folder = main.re_simulation()

        cost_report = [x for x in os.listdir(exportFolder) if 'CostReport' in x]
        ausgebaute_flaeche = [x for x in os.listdir(exportFolder) if 'AusgebauteFlaechen' in x]
        freie_flaeche = [x for x in os.listdir(exportFolder) if 'FreieFlaechen_vorAusbau' in x]
        month_before = [x for x in os.listdir(exportFolder) if 'monthReport_befor' in x]
        month_after = [x for x in os.listdir(exportFolder) if 'monthReport_afterRE' in x]
        month_storage = [x for x in os.listdir(exportFolder) if 'monthReport_afterStorage' in x]
        before_expansion = [x for x in os.listdir(exportFolder) if 'REE_befor' in x]
        after_expansion = [x for x in os.listdir(exportFolder) if 'REE_afterREexpansion' in x]
        after_storage = [x for x in os.listdir(exportFolder) if 'REE_afterStorageExpansion' in x]
        data_storage = [x for x in os.listdir(exportFolder) if 'DataReport_afterStorageExpansion' in x]
        data_after_expansion = [x for x in os.listdir(exportFolder) if 'DataReport_afterREexpansion' in x]
        data_before_expansion = [x for x in os.listdir(exportFolder) if 'DataReport_beforREexpansion' in x]

        month_list = [month_before, month_after, month_storage]
        final_month = ''

        for i in month_list:
            if len(i) != 0:
                final_month = exportFolder + '/' + i[0]

        list_files = [data_storage, data_after_expansion, data_before_expansion, before_expansion, after_expansion, after_storage]
        temp_list = list_files.copy()

        for jindex, j in enumerate(temp_list):
            if len(j) == 0:
                list_files.remove(j)
        for kindex, k in enumerate(list_files):
            list_files[kindex] = exportFolder + '/' + k[0]
            print(list_files[kindex])

        final_file = list_files[-1]
        datasheet_final = list_files[0]

        print(final_file)

        global df_cost_report
        global df_ausbau_vor
        global df_ausbau_pot
        global df_freie_flaeche
        global df_analyse
        global df_datasheet
        global df_month_report

        df_cost_report = pd.read_csv(exportFolder + '/' + cost_report[0], sep=';', decimal=',', encoding='utf-8')
        df_cost_report = df_cost_report.round(2)
        df_ausbau_vor = pd.read_csv(exportFolder + '/' + ausgebaute_flaeche[0], sep=';', decimal=',', encoding='utf-8',
                                    usecols=['StadtVor', 'haVor', 'Coords Vor', 'ID_Weatherstation_Vor', 'Wetter-ID_Vor',
                                             'Anzahl WEAs_Vor', 'nettoFreieFlaeche_Vor', 'Modell_Vor', 'Anzahl_Vor',
                                             'InvestKosten_inMio_Vor', 'Leistung_inMW_Vor'])
        df_ausbau_pot = pd.read_csv(exportFolder + '/' + ausgebaute_flaeche[0], sep=';', decimal=',', encoding='utf-8',
                                    usecols=['StadtPot', 'haPot', 'Coords Pot', 'ID_Weatherstation_Pot', 'Wetter-ID_Pot',
                                             'Anzahl WEAs_Pot', 'nettoFreieFlaeche_Pot', 'Modell_Pot', 'Anzahl_Pot',
                                             'InvestKosten_inMio_Pot', 'Leistung_inMW_Pot'])

        # df_freie_flaeche = pd.read_csv(exportFolder + '/' + freie_flaeche[0], sep=';', decimal=',', encoding='utf-8')
        df_analyse = pd.read_csv(final_file, sep=';', decimal=',', encoding='utf-8')
        df_datasheet = pd.read_csv(datasheet_final, sep=';', decimal=',', encoding='utf-8')
        df_month_report = pd.read_csv(final_month, sep=';', decimal=',', encoding='utf-8')

        # ----------------------------------------------------------------------------------------------------------------------

        coords_to_lat_lon(df_ausbau_vor, 'Coords Vor')
        coords_to_lat_lon(df_ausbau_pot, 'Coords Pot')

        df_ausbau_vor = df_ausbau_vor[df_ausbau_vor['Wetter-ID_Vor'] != 0]
        df_ausbau_vor = df_ausbau_vor.sort_values(by=['ID_Weatherstation_Vor'])
        # df_ausbau_vor['ID_Weatherstation'] = df_ausbau_vor['ID_Weatherstation'].map(str)
        df_ausbau_vor['haVor'] = df_ausbau_vor['haVor'].map(float)
        df_ausbau_vor = df_ausbau_vor[
            ['StadtVor', 'ID_Weatherstation_Vor', 'haVor', 'Anzahl WEAs_Vor', 'nettoFreieFlaeche_Vor', 'Modell_Vor',
             'Anzahl_Vor', 'InvestKosten_inMio_Vor', 'Latitude', 'Longitude', 'Leistung_inMW_Vor']]

        df_ausbau_pot = df_ausbau_pot[df_ausbau_pot['Wetter-ID_Pot'] != 0]
        df_ausbau_pot = df_ausbau_pot.sort_values(by=['ID_Weatherstation_Pot'])
        # df_ausbau_pot['ID_Weatherstation'] = df_ausbau_pot['ID_Weatherstation'].map(str)
        df_ausbau_pot['haPot'] = df_ausbau_pot['haPot'].map(float)
        df_ausbau_pot = df_ausbau_pot[
            ['StadtPot', 'ID_Weatherstation_Pot', 'haPot', 'Anzahl WEAs_Pot', 'nettoFreieFlaeche_Pot', 'Modell_Pot',
             'Anzahl_Pot', 'InvestKosten_inMio_Pot', 'Latitude', 'Longitude', 'Leistung_inMW_Pot']]

        # ----------------------------------------------------------------------------------------------------------------------

        header_list = df_analyse.columns.values.tolist()
        production = ''

        if 'Erzeugung_mit_Speicher' in header_list:
            production = 'Erzeugung_mit_Speicher'
        elif 'Erzeugung_Gesamt' in header_list:
            production = 'Erzeugung_Gesamt'

        df_analyse['Erzeugung_Gesamt_true_with_gaps'] = df_analyse[production].values
        df_analyse['Erzeugung_Gesamt_false_with_gaps'] = df_analyse[production].values

        df_analyse.loc[df_analyse['EE>100%'] == False, 'Erzeugung_Gesamt_true_with_gaps'] = 'NaN'
        df_analyse.loc[df_analyse['EE>100%'] == True, 'Erzeugung_Gesamt_false_with_gaps'] = 'NaN'

        # ----------------------------------------------------------------------------------------------------------------------

        df_analyse['Erzeugung_Percentage_true_with_gaps'] = df_analyse['EE_Anteil'].values
        df_analyse['Erzeugung_Percentage_false_with_gaps'] = df_analyse['EE_Anteil'].values

        df_analyse.loc[df_analyse['EE>100%'] == False, 'Erzeugung_Percentage_true_with_gaps'] = 'NaN'
        df_analyse.loc[df_analyse['EE>100%'] == True, 'Erzeugung_Percentage_false_with_gaps'] = 'NaN'

        # ----------------------------------------------------------------------------------------------------------------------

        year_hours = df_analyse['EE>100%'].count()
        true_count = df_analyse['EE>100%'].tolist().count(True)
        hours_goal = 0
        if storage_expansion_sw:
            hours_goal = storage_expansion_value / 100
        elif wind_expansion:
            hours_goal = wind_expansion_value / 100

        reached_percentage = true_count / year_hours

        if hours_goal == 0:
            results_text = html.Div([
                html.P('No goal was set.'),
                html.B(),
                html.P(f'Reached: {round(reached_percentage * 100, 1)} %')
            ])
        elif reached_percentage >= hours_goal:
            results_text = html.Div([
                html.P('The set goal was reached.'),
                html.B(),
                html.P(f'Goal: {hours_goal * 100} %'),
                html.B(),
                html.P(f'Reached: {round(reached_percentage * 100, 1)} %')
            ])
        else:
            results_text = html.Div([
                html.P('The set goal was not reached.'),
                html.B(),
                html.P(f'Goal: {hours_goal * 100} %'),
                html.B(),
                html.P(f'Reached: {round(reached_percentage * 100, 1)} %')
            ])

        return [results_text, {'display': 'inline'}, {'display': 'none'}, 'Back']
    elif results_value['display'] == 'inline' and settings_value['display'] == 'none':
        return [[html.P('The simulation might take up to 10 minutes'),
                 html.B(),
                 html.P('Do not press the button twice or all simulation progress will be lost!!!')],
                {'display': 'none'}, {'display': 'inline'}, 'Start']
    else:
        print('start button callback error')
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
    # host='141.22.13.112'
