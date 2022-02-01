import base64
import io
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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server

'''
colors = mcolors.CSS4_COLORS
names = list(colors)
for i in names:
    if 'light' in i or 'white' in i:
        names.remove(i)


df = pd.read_csv('data/GruenEnergie_2019_ausbau.csv', sep=';', decimal=',', encoding='latin1')
df['Datum'] = pd.to_datetime(df['Datum'])

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

color_map = {}
for index, i in enumerate(areas_pot_df['Wetter-ID_Pot'].unique()):
    color_map[i] = names[index]
    
def drawEE_percentage(sizing):
    return px.line(df, x="Datum", y='EE_Anteil', color=sizing,
                   title='Ratio Renewable Energy to Consumption').update_layout(
        template='plotly_dark', title_x=0.5).add_hline(y=1).update_traces(showlegend=True)'''

tooltip_text = 'Click for Explanation'
upload_modal_text = 'You have to upload your own data for this simulation. The data has to be in a very specific format, ' \
                    'read the instruction pdf-file or look at the example data provided by the download button on the left. ' \
                    'Please upload the individual .csv-files and not a folder!'

global exportFolder
global list_files
global zip_folder
global df_cost_report_sum
global df_cost_report_wind
global df_cost_report_storage
global df_ausbau_vor
global df_ausbau_pot
global df_analyse
global df_datasheet
global df_month_report
global hours_goal

global error_memory
error_memory = False


def check_own_data():
    pv_list = ['Datum', 'Erzeugung_PV']
    wind_list = ['Datum', 'Erzeugung_Wind']
    wind_eisman_list = ['Datum', 'Erzeugung_Wind', 'verluste_eisman_wind']
    biomass_list = ['Datum', 'Erz_Biomasse_Gesamt']
    consumption_list = ['Datum', 'Verbrauch_Gesamt', 'Verbrauch_HH', 'Verbrauch_SH']
    wind_weather_list = ['Datum', 'Wind_m/s_1975', 'Wind_grad_1975', 'Wind_m/s_4466', 'Wind_grad_4466', 'Wind_m/s_2115',
                         'Wind_grad_2115', 'Wind_m/s_788', 'Wind_grad_788', 'Wind_m/s_2303', 'Wind_grad_2303', 'Wind_m/s_4393',
                         'Wind_grad_4393', 'Wind_m/s_2907', 'Wind_grad_2907', 'Wind_m/s_5078', 'Wind_grad_5078', 'Wind_m/s_2564',
                         'Wind_grad_2564', 'Wind_m/s_4919', 'Wind_grad_4919', 'Wind_m/s_5930', 'Wind_grad_5930', 'Wind_m/s_1379',
                         'Wind_grad_1379', 'Wind_m/s_4039', 'Wind_grad_4039', 'Wind_m/s_3086', 'Wind_grad_3086', 'Wind_m/s_2429',
                         'Wind_grad_2429', 'Wind_m/s_6108', 'Wind_grad_6108', 'Wind_m/s_6163', 'Wind_grad_6163', 'Wind_m/s_3897',
                         'Wind_grad_3897', 'Wind_m/s_1200', 'Wind_grad_1200', 'Wind_m/s_19171', 'Wind_grad_19171']

    list_of_lists = [pv_list, wind_list, wind_eisman_list, biomass_list, consumption_list, wind_weather_list]

    list_of_files = os.listdir('Import/own_data')
    for file in list_of_files:
        c = 0
        file_path = os.path.join('Import/own_data', file)
        df = pd.read_csv(file_path, sep=';', decimal=',', encoding='utf-8')
        df_cols = df.columns.values.tolist()
        del df_cols[0]
        for header_list in list_of_lists:
            if header_list == df_cols:
                c += 1
            else:
                pass
        if c == 0:
            return file

    return ''


def check_headers_datasheet(df):
    header_list = ['Titel', 'Expanded Wind', 'Wind combined', 'Eisman Wind combined', 'PV', 'Biomass', 'RE combined',
                   'Difference', 'Storage loss', 'Difference (RE+Storage)', 'Consumption combined']
    headers_copy = header_list.copy()
    actual_cols = df.columns.values.tolist()

    for i in headers_copy:
        if i not in actual_cols:
            header_list.remove(i)

    return df[header_list]


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
        go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Percentage_true_with_gaps'].multiply(100),
                   marker=dict(color='green'), name="RE >= 100%"))
    fig.add_trace(
        go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Percentage_false_with_gaps'].multiply(100),
                   marker=dict(color='red'), name="RE < 100%"))
    fig.update_layout(template='plotly_dark', title='Ratio: Renewable Energy Production to Consumption', title_x=0.5,
                      xaxis_title="Date",
                      yaxis_title="RE / Consumption (in %)",
                      legend_title="Legend")
    fig.add_hline(y=100)

    return fig


def drawEE_absolute(value):
    fig = go.Figure()

    if value == 'RE':
        fig.add_trace(
            go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Gesamt_true_with_gaps'], marker=dict(color='green'),
                       name="RE >= 100%"))
        fig.add_trace(
            go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Gesamt_false_with_gaps'], marker=dict(color='red'),
                       name="RE < 100%"))
        fig.add_trace(go.Scatter(x=df_analyse['Datum'], y=df_analyse['Verbrauch_Gesamt'], marker=dict(color='blue', opacity=0.2),
                                 name="Consumption"))
    elif value == 'mix':
        headers = df_analyse.columns.values.tolist()
        if 'Erz_Biomasse_Gesamt' in headers:
            fig.add_trace(
                go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erz_Biomasse_Gesamt'], marker=dict(color='green'),
                           name="Biomass"))
        if 'Erz_PV_Gesamt' in headers:
            fig.add_trace(
                go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erz_PV_Gesamt'], marker=dict(color='orange'),
                           name="Solar"))
        if 'Erzeugung_Wind_Gesamt' in headers:
            fig.add_trace(go.Scatter(x=df_analyse['Datum'], y=df_analyse['Erzeugung_Wind_Gesamt'], marker=dict(color='blue'),
                                     name="Wind"))

    elif value == 'storage':
        fig.add_trace(
            go.Scatter(x=df_analyse['Datum'], y=df_analyse['Speicherstatus'], marker=dict(color='blue'),
                       name="Storage capacity (kWh)"))
        fig.add_trace(
            go.Scatter(x=df_analyse['Datum'], y=df_analyse['Ein(+)-/ Ausspeisung(-)'], marker=dict(color='green'),
                       name="Feeding in/out"))
        fig.add_trace(
            go.Scatter(x=df_analyse['Datum'], y=df_analyse['Speicherverluste'], marker=dict(color='red'),
                       name="Energy loss"))

    fig.update_layout(template='plotly_dark', title='Absolute Numbers', title_x=0.5,
                      xaxis_title="Date",
                      yaxis_title="Power (in kW)",
                      legend_title="Legend")
    fig.update_yaxes(exponentformat='e')

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
'''


def draw_pie(biomass, solar):
    headers = ['Wind (TWh)', 'PV (TWh)', 'Biomass (TWh)', 'Deficit/Conventional (TWh)']
    consum = df_month_report['Consumption (TWh)'].iloc[-1]

    if not biomass:
        headers.remove('Biomass (TWh)')
    if not solar:
        headers.remove('PV (TWh)')

    values = df_month_report[headers].iloc[-1].tolist()

    for index, i in enumerate(headers):
        headers[index] = headers[index].replace(' (TWh)', '')

    if 'Diff_Erz_zu_Verb_mit_Speicher' in df_analyse:
        negative_values = df_analyse.loc[df_analyse['Diff_Erz_zu_Verb_mit_Speicher'] < 0]
        negative_values = negative_values['Diff_Erz_zu_Verb_mit_Speicher'].tolist()
        values[-1] = abs(sum(negative_values)) / 1000000000

    other_re = sum(values[1:])
    values[0] = consum - other_re

    df = pd.DataFrame()
    df['Energy source'] = headers
    df['Used energy (in TWh)'] = values
    fig = px.pie(df, values='Used energy (in TWh)', names='Energy source', title='Energy Usage').update_layout(
        template='plotly_dark', title_x=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


def draw_vor(sizing):
    df = df_ausbau_vor.copy()
    if sizing == 'Power':
        sizing = 'Leistung_inMW_Vor'
        df = df.loc[df['Leistung_inMW_Vor'] != 0]
    else:
        sizing = 'nettoFreieFlaeche_Vor'

    return px.scatter_mapbox(df, lat='Latitude', lon='Longitude', title='Simulated expansion - Vorranggebiete',
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
                                 'Leistung_inMW_Vor': 'Power (in MW)',
                                 'InvestKosten_inMio_Vor': 'Investment costs (in Mio. €)',
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

    return px.scatter_mapbox(df, lat='Latitude', lon='Longitude', title='Simulated expansion - Potentialflächen',
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
                                 'Leistung_inMW_Pot': 'Power (in MW)',
                                 'InvestKosten_inMio_Pot': 'Investment costs (in Mio. €)',
                                 'haPot': 'Total area (in ha)'
                             },
                             color='ID_Weatherstation_Pot', color_discrete_map={}, size=sizing, size_max=12,
                             zoom=6.3, center={'lat': 54.2, 'lon': 9.8},
                             ).update_layout(
        mapbox_style="open-street-map", template='plotly_dark', title_x=0.5, legend_title='Wetter ID'
    )


def make_monthly_table(storage):
    '''
        styling = []
        if storage:
            styling = [
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
                        'column_id': 'Biomass (TWh)',
                        'filter_query': '{{Biomass (TWh)}} = {}'.format(
                            df_month_report['Biomass (TWh)'].nlargest(2).tolist()[1])
                    },
                    'backgroundColor': '#c9ffba',
                    'color': 'black'
                },
                {
                    'if': {
                        'column_id': 'Biomass (TWh)',
                        'filter_query': '{{Biomass (TWh)}} = {}'.format(
                            df_month_report['Biomass (TWh)'].min())
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
                        'column_id': 'Storage feed in (TWh)',
                        'filter_query': '{{Storage feed in (TWh)}} = {}'.format(
                            df_month_report['Storage feed in (TWh)'].nlargest(2).tolist()[1])
                    },
                    'backgroundColor': '#c9ffba',
                    'color': 'black'
                },
                {
                    'if': {
                        'column_id': 'Storage feed in (TWh)',
                        'filter_query': '{{Storage feed in (TWh)}} = {}'.format(
                            df_month_report['Storage feed in (TWh)'].min())
                    },
                    'backgroundColor': '#ffbaba',
                    'color': 'black'
                },

                # -----------------------------------------------------------------------------

                {
                    'if': {
                        'column_id': 'Storage feed out (TWh)',
                        'filter_query': '{{Storage feed out (TWh)}} = {}'.format(
                            df_month_report['Storage feed out (TWh)'].nlargest(2).tolist()[1])
                    },
                    'backgroundColor': '#c9ffba',
                    'color': 'black'
                },
                {
                    'if': {
                        'column_id': 'Storage feed out (TWh)',
                        'filter_query': '{{Storage feed out (TWh)}} = {}'.format(
                            df_month_report['Storage feed out (TWh)'].min())
                    },
                    'backgroundColor': '#ffbaba',
                    'color': 'black'
                },
            ]
        else:
            styling = [
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
                        'column_id': 'Biomass (TWh)',
                        'filter_query': '{{Biomass (TWh)}} = {}'.format(
                            df_month_report['Biomass (TWh)'].nlargest(2).tolist()[1])
                    },
                    'backgroundColor': '#c9ffba',
                    'color': 'black'
                },
                {
                    'if': {
                        'column_id': 'Biomass (TWh)',
                        'filter_query': '{{Biomass (TWh)}} = {}'.format(
                            df_month_report['Biomass (TWh)'].min())
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
    ]
    '''

    return dt.DataTable(columns=[{"name": i, "id": i} for i in df_month_report.columns],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0,
                            'height': 'auto'
                        },
                        data=df_month_report.to_dict('records'), cell_selectable=False,
                        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'rgb(10, 10, 10)',
                            'color': 'white',
                            'whiteSpace': 'normal',
                            'textAlign': 'center'
                        },
                        style_data={
                            'backgroundColor': 'rgb(40, 40, 40)',
                            'color': 'white'
                        },
                        # style_data_conditional=styling,
                        )


def make_cost_table(df):
    return dt.DataTable(columns=[{"name": i, "id": i} for i in df.columns],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0,
                            'whiteSpace': 'normal',
                        },
                        data=df.to_dict('records'), cell_selectable=False,
                        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'rgb(10, 10, 10)',
                            'color': 'white',
                            'whiteSpace': 'normal',
                            'textAlign': 'center'
                        },
                        style_data={
                            'backgroundColor': 'rgb(40, 40, 40)',
                            'color': 'white',
                        },
                        #                        style_cell_conditional=[
                        #                           {
                        #                              'if': {
                        #                                 'column_id': 'Model',
                        #                            },
                        #                           'width': '25%'
                        #                      }
                        #                 ]
                        )


def make_datasheet_table():
    df = df_datasheet.copy()

    df = check_headers_datasheet(df)

    return dt.DataTable(columns=[{"name": i, "id": i} for i in df.columns],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0,
                            'whiteSpace': 'normal',
                        },
                        data=df.to_dict('records'), cell_selectable=False,
                        style_table={'overflowY': 'auto', 'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'rgb(10, 10, 10)',
                            'color': 'white',
                            'whiteSpace': 'normal',
                            'textAlign': 'center'
                        },
                        style_data={
                            'backgroundColor': 'rgb(40, 40, 40)',
                            'color': 'white'
                        },
                        # style_data_conditional=[
                        #    {
                        #        'if': {
                        #            'column_id': 'Titel',
                        #        },
                        #        'width': '50px'
                        #    }
                        # ]
                        ),


'''
    tooltip_header={i: i for i in df_datasheet.columns},
    tooltip_data=[
    {
        column: {'value': str(value), 'type': 'markdown'}
        for column, value in row.items()
    } for row in df_datasheet.to_dict('records')
    ],
    css=[{
        'selector': '.dash-table-tooltip',
        'rule': 'background-color: grey; font-family: monospace; color: white'
    }],
'''

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
            {'label': 'Task 1', 'value': 'Task 1'},
            {'label': 'Task 2', 'value': 'Task 2'},
            {'label': 'Task 3', 'value': 'Task 3'},
            {'label': 'Scenario 2030', 'value': 'Scenario 2030'},
            {'label': 'Current State', 'value': 'Current State'},
            {'label': '100% Wind', 'value': '100% Wind'},
            {'label': '95% Green', 'value': '95% Green'},
        ],
        value='Task 1',
        style={"textAlign": "left", 'color': 'black'},
        clearable=False
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
        style={"textAlign": "left", 'color': 'black'},
        clearable=False
    )
])

general_settings = dbc.Card([
    dbc.CardHeader([
        html.H5('General Settings', style={"text-decoration": 'underline'})
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P('Scenario:', id='scenario_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='scenario_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Task 1')], close_button=True, id='scenario_modal_header'),
                    dbc.ModalBody(id='scenario_modal_body'),
                ], id="scenario_modal", centered=True, is_open=False,
                ),
                scenario_dropdown
            ], width=4),
        ], className='pb-3', justify="center", align='center'),
        dbc.Row([
            dbc.Col([
                html.P('Use own data?', id='example_switch_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='example_switch_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Own Data')], close_button=True),
                    dbc.ModalBody(
                        'Own data can be uploaded for simulation. If you click "yes" on this button, an example folder and '
                        'further instruction will be provided when clicking the "Start"-Button. Alternatively you can download '
                        'the instruction.pdf through the "Download Instructions"-Button.'),
                ], id="example_switch_modal", centered=True, is_open=False,
                ),
                example_switch
            ], width=3),
            dbc.Col([
                html.P('Year:', id='year_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='year_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Simulation Year')], close_button=True),
                    dbc.ModalBody(html.P(['Choose the year for the simulation. We have provided example data for the years 2019 '
                                          'and 2020.', html.Br(),
                                          'For own data: Be sure to put the correct year in the .csv-files!'])
                                  ),
                ], id="year_modal", centered=True, is_open=False,
                ),
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
        value=[0, 30, 60],
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
                html.P('Use Eisman?', id='eisman_switch_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='eisman_switch_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Eisman')], close_button=True),
                    dbc.ModalBody(
                        'Turn on to take grid overloads into account and regulate power production of wind power plants '
                        'based on current wind speed.'),
                ], id="eisman_switch_modal", centered=True, is_open=False,
                ),
                eisman_switch
            ], width=4)
        ], className='pb-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Wind speeds to regulate at:', id='eisman_wind_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='eisman_wind_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Eisman: Wind Speed')], close_button=True),
                    dbc.ModalBody(
                        'Pick three wind speed thresholds for when power regulation should be applied.'),
                ], id="eisman_wind_modal", centered=True, is_open=False,
                ),
                eisman_wind_slider
            ], width=10)
        ], className='pb-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P('Power regulation:', id='eisman_percentage_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='eisman_percentage_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Eisman: Power Regulation')], close_button=True),
                    dbc.ModalBody(html.P([
                        'To what percentage should eisman reduce the actually produced power to at the selected wind speeds.',
                        html.Br(),
                        html.Span('Note: ', style={'textDecoration': 'underline'}),
                        'The smallest wind speed relates to the highest percentage value! For example if the lowest wind speed '
                        'is 13m/s and the highest percentage value is 60%, the programm will reduce the power of all affected '
                        'wind turbines by 40% if the wind speed exceeds 13m/s.'
                    ])
                    ),
                ], id="eisman_percentage_modal", centered=True, is_open=False,
                ),
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
                html.P('Use biomass?', id='biomass_switch_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='biomass_switch_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Biomass')], close_button=True),
                    dbc.ModalBody(
                        'Turn on to take biomass energy production into account.'),
                ], id="biomass_switch_modal", centered=True, is_open=False,
                ),
                biomass_switch
            ], width=6),
            dbc.Col([
                html.P('Use solar power?', id='solar_switch_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='solar_switch_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Solar')], close_button=True),
                    dbc.ModalBody(
                        'Turn on to take solar energy production into account.'),
                ], id="solar_switch_modal", centered=True, is_open=False,
                ),
                solar_switch
            ], width=6)
        ], className='pb-3 px-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(['Biomass growth:', html.Br(), '(in %)'], id='biomass_input_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='biomass_input_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Biomass Growth')], close_button=True),
                    dbc.ModalBody(
                        'This value determines the natural yearly expansion of biomass. With this growth value, the programm '
                        'can make approximations for biomass energy production of future years based on current data. Since '
                        'it is a natural growth factor, no further investment costs are needed from our side.'),
                ], id="biomass_input_modal", centered=True, is_open=False,
                ),
                biomass_input
            ], width=5),
            dbc.Col([
                html.P(['Solar growth:', html.Br(), '(in %)'], id='solar_input_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='solar_input_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Solar Growth')], close_button=True),
                    dbc.ModalBody(
                        'This value determines the natural yearly expansion of solar power. With this growth value, the programm '
                        'can make approximations for solar energy production of future years based on current data. Since '
                        'it is a natural growth factor, no further investment costs are needed from our side.'),
                ], id="solar_input_modal", centered=True, is_open=False,
                ),
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
                html.P('Expand wind energy?', id='wind_expansion_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='wind_expansion_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Wind Expansion')], close_button=True),
                    dbc.ModalBody(
                        'Should the programm simulate building out own wind turbines?'),
                ], id="wind_expansion_modal", centered=True, is_open=False,
                ),
                wind_expansion_switch
            ], width=6),
            dbc.Col([
                html.P('Use planned wind turbines?', id='planned_wind_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='planned_wind_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Planned Wind')], close_button=True),
                    dbc.ModalBody(
                        'If turned on, the programm will use already planned wind turbines for that year.'),
                ], id="planned_wind_modal", centered=True, is_open=False,
                ),
                planned_wind_switch
            ], width=6)
        ], className='pb-3 px-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(['Expand wind until:', html.Br(), '(percentage of hours over 100% RE per year)'], id='wind_hours_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='wind_hours_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Wind Expansion Goal')], close_button=True),
                    dbc.ModalBody(
                        'The year 2019 has 8760 hours so if for example a value of 75% is chosen, the simulation will expand '
                        'upon wind turbines until either the set goal was reached (75% of 8760 hours = 6570 hours) or '
                        'until all possible areas have been completely used up.'),
                ], id="wind_hours_modal", centered=True, is_open=False,
                ),
                wind_hours_slider
            ], width=10)
        ], className='py-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P('Choose expansion options:', id='wind_options_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='wind_options_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Wind Expansion Options')], close_button=True),
                    dbc.ModalBody(html.P([
                        html.Span('Vorranggebiete:', style={"text-decoration": 'underline'}), html.Br(),
                        'These are preferential areas for expanding wind turbines with no legal issues.', html.Br(),
                        html.Span('Potentialflächen:', style={"text-decoration": 'underline'}), html.Br(),
                        'These areas are more complicated to expand wind turbines on due to a variety of legal complications. '
                        'One of these can be the area being to close to a nature reserve or town. So while some of these issues '
                        'might not completely hinder an expansion, they definitely are not as well suited for expanding wind '
                        'turbines.'
                    ]),
                        'placeholder text'),
                ], id="wind_options_modal", centered=True, is_open=False,
                ),
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
                html.P('Use Storage?', id='storage_switch_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='storage_switch_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Storage')], close_button=True),
                    dbc.ModalBody(
                        'This switch will determine whether storages should be used to compensate for the undesired fluctuations '
                        'in renewable energy production.'),
                ], id="storage_switch_modal", centered=True, is_open=False,
                ),
                storage_switch
            ], width=6),
            dbc.Col([
                html.P('Expand storage?', id='storage_expansion_switch_text',
                       style={"textDecoration": "underline", "cursor": "pointer"}),
                dbc.Tooltip(
                    tooltip_text, target='storage_expansion_switch_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Storage Expansion')], close_button=True),
                    dbc.ModalBody(
                        'Choose whether to expand upon the existing storages or not.'),
                ], id="storage_expansion_switch_modal", centered=True, is_open=False,
                ),
                storage_expansion_switch
            ], width=6)
        ], className='py-3 px-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(
                    'Start capacity:', id='start_capacity_text',
                    style={"textDecoration": "underline", "cursor": "pointer"}
                ),
                dbc.Tooltip(
                    tooltip_text, target='start_capacity_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Start Capacity')], close_button=True),
                    dbc.ModalBody(
                        'The start capacity determines how "full" the chosen storages should be at the beginning of the year. '
                        'This will be determined through a percentage value referring to the maximum capacity. For example '
                        'if the combined storage capacity is 100GWh and a value of 50% has been chosen, the year starts off '
                        'with 50GWh worth of stored energy.'),
                ], id="start_capacity_modal", centered=True, is_open=False,
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
                dbc.Tooltip(
                    tooltip_text, target='storage_expansion_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Storage Expansion Goal')], close_button=True),
                    dbc.ModalBody(
                        'What should be the final percentage of hours over 100% renewable energy, storages will be expanded '
                        'after the set hour goal for wind is reached (see wind settings slider).'),
                ], id="storage_expansion_modal", centered=True, is_open=False,
                ),
                storage_expansion_slider
            ], width=10)
        ], className='py-3', justify="center"),
        dbc.Row([
            dbc.Col([
                html.P(
                    'Safety padding (in %):', id='safety_padding_text',
                    style={"textDecoration": "underline", "cursor": "pointer"}
                ),
                dbc.Tooltip(
                    tooltip_text, target='safety_padding_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Safety padding')], close_button=True),
                    dbc.ModalBody(
                        'This option will create a safety padding for expanding storage. For example if the minimum '
                        'amount of capacity needed to reach the 100% hour threshold is 100GWh, you can '
                        'determine a safety padding of 20% and the programm will expand the storage to 120GWh.'
                        '(more budget needed, but more realistic)'),
                ], id="safety_padding_modal", centered=True, is_open=False,
                ),
                safety_padding_slider
            ], width=10)
        ], className='py-3', justify="around"),
        dbc.Row([
            dbc.Col([
                html.P(
                    'Choose storage options:', id='storage_options_text',
                    style={"textDecoration": "underline", "cursor": "pointer"}
                ),
                dbc.Tooltip(
                    tooltip_text, target='storage_options_text', placement='top'
                ),
                dbc.Modal([
                    dbc.ModalHeader([html.H5('Storage Options')], close_button=True),
                    dbc.ModalBody(html.P([
                        html.Span('Existing storages: ', style={"text-decoration": 'underline'}), html.Br(),
                        'Right now the only existing storage used in the simulation is the '
                        'water pump storage in "Geesthacht". Only operational costs will be considered for this storage.',
                        html.Br(),
                        html.Span('Laegerdorf: ', style={"text-decoration": 'underline'}), html.Br(),
                        'A planned water pump storage located in Schleswig-Holstein. Building and operational '
                        'costs will be considered for this storage.',
                        html.Br(),
                        html.Span('Compressed air: ', style={"text-decoration": 'underline'}), html.Br(),
                        'This storage technology will most likely be indispensable for reaching the 100% hour '
                        'goal. With an estimated capacity potential of 13.5TWh in Schleswig-Holstein alone, it has the necessary '
                        'capacity for long energy droughts.'])
                    ),
                ], id="storage_options_modal", centered=True, is_open=False,
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
            html.Div(children=[html.P('The simulation might take up to 15 minutes'),
                               html.B(),
                               html.P('Do not press the button twice or all simulation progress will be lost!!!')],
                     id='start_output'),
            dbc.Button('Start', id='start_button', n_clicks=0, disabled=False),
        ])
    ], className='py-2', justify='center'),
    dbc.Row([
        dbc.Col([
            html.Div(id='spinner_div')
        ])
    ], justify='center', className='py-2'),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Interval(id="progress_interval", n_intervals=0, interval=500, disabled=True, max_intervals=100),
                dbc.Progress(id="progress"),
                html.P('(Progress is just an approximation)')
            ], id='progress_div', style={'display': 'none'})
        ], width=5)
    ], justify='center', className='py-2'),
], className='text-center')

support_button = html.Div([
    dbc.Button('Before simulation', id='support_button', n_clicks=0, disabled=False, style={'display': 'none'}),
], className='text-center')

download_button = html.Div([
    dbc.Button('Download Results', id='download_results_button'),
    dcc.Download(id='download_results')
], className='text-center')

upload_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader('Upload Data', close_button=True),
        dbc.ModalBody(html.P(upload_modal_text), id='upload_modal_text'),
        dbc.ModalFooter([
            dbc.Button('Download example', id='example_download_button'),
            dcc.Download(id='example_download'),
            dcc.Upload(
                [dbc.Button('Upload own data')],
                id='upload_button',
                multiple=True
            ),
            dbc.Button('Start', id='final_start_button', disabled=True, n_clicks=0)
        ])
    ], id="upload_modal", centered=True, is_open=False,
    )
])

settings_children = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H3('REE-Szenariensimulator Hamburg-Schleswig-Holstein'),
                    html.H4('Integrationsprojekt Profs. Eger/Renz'),
                ]),
                dbc.CardBody([
                    html.H5('Realisierung durch Team RE-Solutions: ', style={"text-decoration": 'underline'}),
                    html.P([
                        'Maximilian Boje', html.Br(),
                        'Lasse Gildenstern', html.Br(),
                        'Siham Kaibour', html.Br(),
                        'Maximilian Kompch', html.Br(),
                        'Nils Kranauge', html.Br(),
                        'Alshimaa Muhamed', html.Br(),
                        'Alexander Wengert', html.Br(),
                    ])
                ])
            ], className='text-center')
        ], width=11)
    ], justify='center', className='pb-1'),
    dbc.Row([
        dbc.Col([
            dbc.Button('Download Documentation', id='instructions_button'),
            dcc.Download(id='instructions_download')
        ], width='auto')
    ], className='py-1', justify='center'),
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
                                         {'label': 'Ratio', 'value': 'ratio'},
                                         {'label': 'Absolute RE', 'value': 'RE'},
                                         {'label': 'Energy mix', 'value': 'mix'},
                                     ],
                                     value='ratio',
                                     style={"textAlign": "left", 'color': 'black'},
                                     clearable=False
                                     )
                    ], width=1)
                ], className='pt-3'),
                dbc.Row([
                    dcc.Graph(id='graph_year'),
                ], className='py-3'),
                dbc.Row([
                    dbc.Col([
                        html.H4('Monthly Overview', style={"text-decoration": 'underline'}),
                        html.Div(id='monthly_table')
                    ])
                ], className='py-3'),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.P('Area:'),
                                dcc.Dropdown(id='dropdown_map',
                                             options=[
                                                 {'label': 'Vor', 'value': 'Vor'},
                                                 {'label': 'Pot', 'value': 'Pot'}
                                             ],
                                             value='Vor',
                                             style={"textAlign": "left", 'color': 'black'},
                                             clearable=False
                                             )
                            ], width=3),
                            dbc.Col([
                                html.P('Sizing:'),
                                dcc.Dropdown(id='dropdown_map_size',
                                             options=[
                                                 {'label': 'Power', 'value': 'Power'},
                                                 {'label': 'Free area', 'value': 'Area'}
                                             ],
                                             value='Power',
                                             style={"textAlign": "left", 'color': 'black'},
                                             clearable=False
                                             )
                            ], width=3),
                        ], justify='around'),
                        dbc.Row([
                            dcc.Graph(id='map')
                        ], className='pt-1')
                    ], width=6),
                    dbc.Col([
                        dbc.Row([
                            html.H5('Pie Explanation', id='pie_text',
                                    style={"text-decoration": 'underline', "cursor": "pointer"}),
                            dbc.Modal([
                                dbc.ModalHeader([html.H5('Used energy chart')], close_button=True),
                                dbc.ModalBody(
                                    'This pie chart show the amount of energy that is actually used. Basically if the total '
                                    'yearly energy consumption is 20TWh and 30TWh were produced by wind energy '
                                    'alone, not all the energy can be used. This also takes hours into account '
                                    'in which renewable energy (storages included) did not completely cover the required amount '
                                    'of energy. For these hours we still have to rely on conventional energy sources.'),
                            ], id="pie_modal", centered=True, is_open=False,
                            ),
                        ]),
                        dbc.Row([
                            dcc.Graph(id='graph_pie')
                        ])
                    ], width=6)
                ], className='py-1', align='end'),
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
    ], className='px-3 pb-3')
])

app.layout = html.Div([
    html.Div(id='settings_page', children=settings_children, style={'display': 'inline'}),
    dbc.Row([
        start_button,
        upload_modal
    ], className='py-2', justify='center'),
    html.Div(id='results', children=results, style={'display': 'none'}),
    support_button
], style={"width": "99%"}, className='px-3 py-2')

scenario_1 = [False, False, [13, 19, 25], [0, 30, 60], True, True, 5, 10, True, True, 75, ['vor', 'pot'], False, False, 0]
scenario_2 = [False, False, [13, 19, 25], [0, 30, 60], True, True, 5, 10, True, True, 75, ['vor', 'pot'], True, True, 50]
scenario_3 = [True, False, [13, 19, 25], [0, 30, 60], True, True, 5, 10, True, True, 75, ['vor', 'pot'], True, True, 50]
scenario_2030 = [False, False, [13, 19, 25], [0, 30, 60], True, True, 50, 200, True, True, 76, ['vor', 'pot'], True, True, 50]
scenario_current = [False, False, [13, 19, 25], [0, 30, 60], True, True, 0, 0, False, True, 0, [], True, False, 50]
scenario_100_wind = [False, False, [13, 19, 25], [0, 30, 60], True, True, 0, 0, True, True, 100, ['vor', 'pot'], False, False, 0]
scenario_95_percent = [False, False, [13, 19, 25], [0, 30, 60], True, True, 5, 10, True, True, 65, ['vor', 'pot'], True, True, 50]


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
    ],
    Input('scenario_dropdown', 'value'),
    State('scenario_dropdown', 'options')
)
def change_scenario(value, options):
    if value == options[0]['value']:
        return scenario_1
    elif value == options[1]['value']:
        return scenario_2
    elif value == options[2]['value']:
        return scenario_3
    elif value == options[3]['value']:
        return scenario_2030
    elif value == options[4]['value']:
        return scenario_current
    elif value == options[5]['value']:
        return scenario_100_wind
    elif value == options[6]['value']:
        return scenario_95_percent
    else:
        raise PreventUpdate


@app.callback(
    Output('storage_options_check', 'value'),
    [
        Input('storage_switch', 'value'),
        Input('storage_expansion_switch', 'value'),
    ]
)
def storage_options_method(switch, expansion):
    if not switch:
        return []
    if switch and not expansion:
        return ['existing']
    return ['existing', 'laegerdorf', 'air']


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
        State('scenario_dropdown', 'options'),
        State('storage_expansion_slider', 'value')
    ]
)
def lock_storage_expansion(value, scenario, options, current_storage):
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
            return value, slider_intervals(value), 100
        elif scenario == options[4]['value']:
            return value, slider_intervals(value), 0
        elif scenario == options[5]['value']:
            return value, slider_intervals(value), 0
        elif scenario == options[6]['value']:
            return value, slider_intervals(value), 95
        else:
            raise PreventUpdate
    else:
        if value >= current_storage:
            return value, slider_intervals(value), value
        elif value < current_storage:
            return value, slider_intervals(value), current_storage
        else:
            raise PreventUpdate


# scenario modal texts
tt_1 = 'Goal of task 1 is to achieve 100% RE production for 75% of the time. The means to achieve this goal ' \
       'are existing biomass plants, solar panels and wind turbines, which can all be expanded upon. Power storages should not ' \
       'be used to complete this task. The goal should be reached within an allowed budget of 10 Bn. €.'

tt_2 = 'Goal of task 2 is to achieve 100% RE production for 100% of the time. To accomplish this goal wind turbines and power ' \
       'storages are allowed to be used and expanded upon. Like before the intended budget for a successful completion are 10 ' \
       'bn. €.'

tt_3 = 'Goal of task 3 is to achieve 100% RE production for 100% of the time, just like task 2. For this simulation the user ' \
       'should use their own data (see upload button). The means to achieve this goal are the same as in task 2.'

tt_4 = 'This scenario will simulate a possible state of 2030 with heavily increased number of biomass, solar and wind energy ' \
       'production plants.'

tt_5 = 'This scenario will simulate the current state of renewable energy production by neither expanding upon the energy ' \
       'production nor the power storages. It will use existing power storages and existing means of power production ' \
       '(will include planned wind turbines).'

tt_6 = 'This scenario aims to generate 100% renewable energy throughout the whole year by only expanding on wind energy.'

tt_7 = 'In this scenario we analyze the cost behaviour of storage expansions. By only expanding enough storage to supply 95% ' \
       'of the yearly hours with 100% renewable energies, there should be a noticable difference in investment cost to ' \
       'supplying 100% of the hours with renewable energies. (Wind and storage values are picked for an economical optimum)'


@app.callback(
    [
        Output('scenario_modal', 'is_open'),
        Output('scenario_modal_header', 'children'),
        Output('scenario_modal_body', 'children')
    ],
    [
        Input("scenario_text", "n_clicks"),
    ],
    [
        State("scenario_modal", "is_open"),
        State('scenario_dropdown', 'value'),
        State('scenario_dropdown', 'options')
    ]
)
def scenario_tooltip(n1, is_open, scenario, options):
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
    elif scenario == options[5]['value']:
        picked = tt_6
    elif scenario == options[6]['value']:
        picked = tt_7
    else:
        picked = ''
    if n1:
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


# -----------------------------------------------------------------------------------------------------------------------
# Modals


@app.callback(
    Output('example_switch_modal', 'is_open'),
    Input('example_switch_text', 'n_clicks'),
    State('example_switch_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('pie_modal', 'is_open'),
    Input('pie_text', 'n_clicks'),
    State('pie_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('year_modal', 'is_open'),
    Input('year_text', 'n_clicks'),
    State('year_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('eisman_switch_modal', 'is_open'),
    Input('eisman_switch_text', 'n_clicks'),
    State('eisman_switch_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('eisman_wind_modal', 'is_open'),
    Input('eisman_wind_text', 'n_clicks'),
    State('eisman_wind_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('eisman_percentage_modal', 'is_open'),
    Input('eisman_percentage_text', 'n_clicks'),
    State('eisman_percentage_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('biomass_switch_modal', 'is_open'),
    Input('biomass_switch_text', 'n_clicks'),
    State('biomass_switch_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('solar_switch_modal', 'is_open'),
    Input('solar_switch_text', 'n_clicks'),
    State('solar_switch_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('biomass_input_modal', 'is_open'),
    Input('biomass_input_text', 'n_clicks'),
    State('biomass_input_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('solar_input_modal', 'is_open'),
    Input('solar_input_text', 'n_clicks'),
    State('solar_input_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('wind_expansion_modal', 'is_open'),
    Input('wind_expansion_text', 'n_clicks'),
    State('wind_expansion_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('planned_wind_modal', 'is_open'),
    Input('planned_wind_text', 'n_clicks'),
    State('planned_wind_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('wind_hours_modal', 'is_open'),
    Input('wind_hours_text', 'n_clicks'),
    State('wind_hours_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('wind_options_modal', 'is_open'),
    Input('wind_options_text', 'n_clicks'),
    State('wind_options_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('storage_switch_modal', 'is_open'),
    Input('storage_switch_text', 'n_clicks'),
    State('storage_switch_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('storage_expansion_switch_modal', 'is_open'),
    Input('storage_expansion_switch_text', 'n_clicks'),
    State('storage_expansion_switch_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('start_capacity_modal', 'is_open'),
    Input('start_capacity_text', 'n_clicks'),
    State('start_capacity_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


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
    Output('safety_padding_modal', 'is_open'),
    Input('safety_padding_text', 'n_clicks'),
    State('safety_padding_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('storage_options_modal', 'is_open'),
    Input('storage_options_text', 'n_clicks'),
    State('storage_options_modal', 'is_open'),
    prevent_initial_call=True
)
def storage_expansion_modal(n, is_open):
    if n:
        return not is_open
    return is_open


# -----------------------------------------------------------------------------------------------------------------------


@app.callback(
    [
        Output('upload_modal', 'is_open'),
        Output('final_start_button', 'n_clicks')
    ],
    [
        Input('start_button', 'n_clicks'),
        Input('final_start_button', 'n_clicks'),
    ],
    [
        State('upload_modal', 'is_open'),
        State('example_switch', 'value'),
        State('final_start_button', 'n_clicks')
    ],
    prevent_initial_call=True
)
def storage_expansion_modal(n_start, n_final, is_open, value, n_state):
    if n_start == 0 and n_final == 0:
        raise PreventUpdate
    if not value:
        return is_open, n_state + 1
    if n_start or n_final:
        return not is_open, dash.no_update
    return is_open, dash.no_update


@app.callback(
    Output("example_download", "data"),
    Input("example_download_button", "n_clicks"),
    prevent_initial_call=True,
)
def download_example(n_clicks):
    return dcc.send_file('Import/example_folder.zip')


@app.callback(
    [
        Output('final_start_button', 'disabled'),
        Output('upload_modal_text', 'children'),
    ],
    Input('upload_button', 'contents'),
    [
        State('upload_button', 'filename'),
        State('year_dropdown', 'value')
    ],
    prevent_initial_call=True
)
def upload_data(list_of_contents, list_of_names, year):
    if list_of_contents is not None:
        checklist_needed_files = [
            'Erz_kumuliert_' + str(year) + '_PV.csv',
            'Erz_kumuliert_' + str(year) + '_Wind.csv',
            'Erz_kumuliert_' + str(year) + '_Wind_eisman.csv',
            'Erz_kumuliert_Biomasse_' + str(year) + '.csv',
            'Verbrauch_kumuliert_' + str(year) + '.csv',
            'Wind_Wetterdaten_' + str(year) + '.csv'
        ]

        # check if uploaded files have proper names
        if len(list_of_names) == len(checklist_needed_files):
            for i in range(len(list_of_names)):
                if list_of_names[i] in checklist_needed_files:
                    pass
                else:
                    return True, html.P([upload_modal_text, html.Br(), html.Br(),
                                         'Wrong filename: ' + list_of_names[i]])
        else:
            return True, html.P([upload_modal_text, html.Br(), html.Br(),
                                 'Wrong amount of files!'])

        # delete files
        list_of_files = os.listdir('Import/own_data')
        for file in list_of_files:
            file_path = os.path.join('Import/own_data', file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                # print(f'Failed to delete "{file_path}". Reason: {e}')
                pass

        # save new files
        for index in range(len(list_of_names)):
            file_content = list_of_contents[index]
            file_name = list_of_names[index]
            content_type, content_string = file_content.split(',')
            decoded = base64.b64decode(content_string)
            try:
                df = pd.read_csv(io.StringIO(decoded.decode(encoding='utf-8', errors='replace')),
                                 sep=';', decimal=',', index_col=False)
                df.to_csv('Import/own_data/' + file_name, sep=';', decimal=',', encoding='utf-8-sig')
            except Exception as e:
                # print(e)
                pass

        wrong_file = check_own_data()
        if wrong_file == '':
            return False, html.P([upload_modal_text, html.Br(), html.Br(),
                                  'The necessary files were successfully uploaded!'])
        else:
            return True, html.P([upload_modal_text, html.Br(), html.Br(),
                                 f'Wrong formatting in file: "{wrong_file}"!'])

    else:
        return True, dash.no_update


@app.callback(
    [
        Output('safety_padding_slider', 'value'),
        Output('safety_padding_slider', 'disabled'),
    ],
    [
        Input('storage_expansion_slider', 'value'),
        Input('storage_expansion_slider', 'disabled'),
    ]
)
def padding(value, disabled):
    if value < 100:
        return 0, True
    elif disabled:
        return dash.no_update, True
    return 5, False


@app.callback(
    [
        Output('spinner_div', 'children'),
        Output('progress_div', 'style'),
        Output('progress_interval', 'disabled'),
        Output('progress_interval', 'n_intervals'),
        Output('progress_interval', 'interval'),
    ],
    [
        Input('final_start_button', 'n_clicks'),
        Input('start_button', 'children'),
        Input('start_output', 'children'),
    ],
    [
        State('support_button', 'n_clicks'),
        State('example_switch', 'value'),
        State('eisman_switch', 'value'),
        State('wind_expansion_switch', 'value'),
        State('storage_switch', 'value'),
        State('storage_expansion_switch', 'value'),
    ],
    prevent_initial_call=True
)
def spinner(n, value, start_output, n_support, own_data, eisman, wind_expansion, storage_switch, storage_expansion):
    global error_memory
    if error_memory:
        error_memory = False
        return html.Div(), {'display': 'none'}, True, 0, dash.no_update
    if n > n_support:
        if value == 'Start':

            start_value = 15
            if not own_data:
                start_value -= 4
            if not eisman:
                start_value -= 4
            if not wind_expansion:
                start_value -= 3.25
            if not storage_switch:
                start_value -= 1.25
            if not storage_expansion:
                start_value -= 2.25

            intervals = int(((start_value * 60) / 100) * 1000)

            return dbc.Button(
                [dbc.Spinner(size="sm"), " Simulating..."],
                color="secondary",
                disabled=True), {'display': 'inline'}, False, 0, intervals
        elif value == 'Back':
            return html.Div(), {'display': 'none'}, True, 0, dash.no_update
    elif value == 'Back':
        return html.Div(), {'display': 'none'}, True, 0, dash.no_update
    else:
        return dash.no_update, {'display': 'none'}, True, 0, dash.no_update


@app.callback(
    [
        Output("progress", "value"),
    ],
    [
        Input("progress_interval", "n_intervals")
    ],
    prevent_initial_call=True
)
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    progress = min(n % 110, 100)
    # only add text after 5% progress to ensure text isn't squashed too much
    return [progress]


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
        return [{'label': str(x), 'value': x} for x in range(2000, 2100, 1)], 2019
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
    ],
    [
        Input('storage_switch', 'value'),
        Input('storage_expansion_switch', 'value'),
    ]
)
def disable_storage(storage, expansion):
    if storage and expansion:
        return False, False
    elif storage and not expansion:
        return False, True
    elif not storage:
        return True, True
    else:
        pass


@app.callback(
    Output('monthly_table', 'children'),
    [
        Input('start_button', 'children')
    ],
    State('storage_switch', 'value')
)
def montly_table(value, storage):
    if value == 'Start':
        return dash.no_update
    elif value == 'Back':
        return make_monthly_table(storage)
    else:
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
        return dash.no_update


@app.callback(
    Output('costs', 'children'),
    [
        Input('start_button', 'children')
    ]
)
def costs_table(value):
    if value == 'Start':
        return dash.no_update
    elif value == 'Back':
        if len(df_cost_report_wind.index) == 0 and len(df_cost_report_storage.index) == 0:
            return html.Div([
                html.P('No expenses were made.')
            ])
        elif len(df_cost_report_wind.index) == 0:
            return html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H5('Wind:', style={'textDecoration': 'underline'}),
                        html.P('No wind turbines were build.')
                    ], width=6),
                    dbc.Col([
                        html.H5('Storage:', style={'textDecoration': 'underline'}),
                        make_cost_table(df_cost_report_storage)
                    ], width=6),
                ], className='py-2'),
                dbc.Row([
                    dbc.Col([
                        html.H5('Overall costs:', style={'textDecoration': 'underline'}),
                        make_cost_table(df_cost_report_sum)
                    ], width=4)
                ], className='py-2', justify='center')
            ])
        elif len(df_cost_report_storage.index) == 0:
            return html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H5('Wind:', style={'textDecoration': 'underline'}),
                        make_cost_table(df_cost_report_wind)
                    ], width=6),
                    dbc.Col([
                        html.H5('Storage:', style={'textDecoration': 'underline'}),
                        html.P('No storages were build.')
                    ], width=6),
                ], className='py-2'),
                dbc.Row([
                    dbc.Col([
                        html.H5('Overall costs:', style={'textDecoration': 'underline'}),
                        make_cost_table(df_cost_report_sum)
                    ], width=4)
                ], className='py-2', justify='center')
            ])
        else:
            return html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H5('Wind:', style={'textDecoration': 'underline'}),
                        make_cost_table(df_cost_report_wind)
                    ], width=6),
                    dbc.Col([
                        html.H5('Storage:', style={'textDecoration': 'underline'}),
                        make_cost_table(df_cost_report_storage)
                    ], width=6),
                ], className='py-2'),
                dbc.Row([
                    dbc.Col([
                        html.H5('Overall costs:', style={'textDecoration': 'underline'}),
                        make_cost_table(df_cost_report_sum)
                    ], width=4)
                ], className='py-2', justify='center')
            ])
    else:
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
    Output('dropdown_data', 'options'),
    Input('support_button', 'n_clicks'),
    State('storage_switch', 'value'),
    prevent_initial_call=True
)
def graph_dropdown(n, value):
    if value:
        return [
            {'label': 'Ratio', 'value': 'ratio'},
            {'label': 'Absolute RE', 'value': 'RE'},
            {'label': 'Energy mix', 'value': 'mix'},
            {'label': 'Storage', 'value': 'storage'},
        ]
    return [
        {'label': 'Ratio', 'value': 'ratio'},
        {'label': 'Absolute RE', 'value': 'RE'},
        {'label': 'Energy mix', 'value': 'mix'},
    ]


@app.callback(
    Output('graph_year', 'figure'),
    [
        Input('dropdown_data', 'value'),
        Input('start_button', 'children')
    ],
    State('dropdown_data', 'options')
)
def change_graph(data, children, options):
    if children == 'Start':
        return dash.no_update
    elif children == 'Back':
        if data == options[0]['value']:
            return drawEE_percentage()
        elif data == options[1]['value']:
            return drawEE_absolute(data)
        elif data == options[2]['value']:
            return drawEE_absolute(data)
        elif len(options) == 4:
            if data == options[3]['value']:
                return drawEE_absolute(data)
        else:
            pass


@app.callback(
    Output('graph_pie', 'figure'),
    Input('start_button', 'children'),
    [
        State('biomass_switch', 'value'),
        State('solar_switch', 'value'),
    ],
    prevent_initial_call=True
)
def pie(children, biomass, solar):
    if children == 'Start':
        return dash.no_update
    elif children == 'Back':
        return draw_pie(biomass, solar)
    else:
        pass


@app.callback(
    Output("download_results", "data"),
    Input("download_results_button", "n_clicks"),
    prevent_initial_call=True,
)
def download(n_clicks):
    return dcc.send_file(zip_folder + '.zip')


@app.callback(
    Output("instructions_download", "data"),
    Input("instructions_button", "n_clicks"),
    prevent_initial_call=True,
)
def download(n_clicks):
    return dcc.send_file('ThinkNewFitness_BusinessPlan.pdf')


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
    Input('final_start_button', 'n_clicks'),
    prevent_initial_call=True
)
def click_support_button(n):
    time.sleep(1)
    return n


def make_settings_text(settings):
    with open(exportFolder + '/settings.txt', 'w') as data:
        data.write(settings[0])


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
    prevent_initial_call=True
)
def start_sim(n, exmpl_sw, year, wind_expansion_value, bio_sw, bio_inp, solar_sw, solar_inp, wind_expansion,
              planned_wind, methods_wind, storage_sw, storage_expansion_sw, storage_expansion_value,
              start_capacity_value, safety_padding_value, storage_options, eisman_sw, eisman_wind, eisman_percentage,
              results_value, settings_value):
    '------------------------------------------------------------------------'
    'HEADER'

    if results_value['display'] == 'none' and settings_value['display'] == 'inline':

        simulation_results_folders = os.listdir('REE_AnalyseCompleted')
        full_path = ["REE_AnalyseCompleted/{0}".format(x) for x in simulation_results_folders]

        while len(simulation_results_folders) >= 5:
            oldest_file = min(full_path, key=os.path.getctime)
            shutil.rmtree(oldest_file)
            simulation_results_folders = os.listdir('REE_AnalyseCompleted')
            full_path = ["REE_AnalyseCompleted/{0}".format(x) for x in simulation_results_folders]

        '- - - - - - - - - - - - - - - - - - - -'
        main.META_EE_Anteil = wind_expansion_value / 100  # Muss Decimal angegeben werden
        main.META_EE_Speicher = storage_expansion_value / 100  # Grenzwert bis Speicher nicht mehr ausgebaut werden 100%
        main.META_year = year
        main.META_own_data = exmpl_sw
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
        main.META_first_power_limit = eisman_percentage[2] / 100
        main.META_sec_power_limit = eisman_percentage[1] / 100
        main.META_third_power_limit = eisman_percentage[0] / 100
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
        main.META_DATA_verbrauch_kumuliert = False  # True wenn die Liste erstellt werden soll
        main.META_DATA_DBWKAreload = False  # True wenn die DB der WKA Lastgänge erstellt werden soll
        main.META_DATA_DB_min_hight = 100  # Wert gibt die min höhe der WKA für die DB Lastgänge erstellt werden soll
        main.META_DATA_plannedAreas_potVor_getCoords = False  # True wenn die Ausbauflächen keine Standorte besitzen
        #                                           -> Wetterstationen werden ebenfalls hinzugefügt
        main.META_DATA_plannedAreas_potVor_getWeather = False  # True wenn die Ausbauflächen keine zugeordnete Wetterstation besitzen
        main.META_DATA_be_plannedWKA_getCoords = False  # True wenn die Coords zugeordnet werden müssen

        main.META_DATA_be_plannedWKA_getWeatherID = False  # True wenn die Weather ID zugeordnet werden muss
        main.META_DATA_be_plannedWKA_power = False  # True wenn die Leistung ausgerechnet werden muss
        main.META_DATA_pv_power = False  # True wenn die Leistung von PV erneut gerechnet werden muss
        main.META_DATA_wind_power = False  # True wenn die Leistung von Wind erneut gerechnet werden muss
        main.META_DATA_eisman = False

        global exportFolder
        global list_files
        global zip_folder
        global error_memory

        # exportFolder, cost_report, dataframe_expansion_area, export_simulation_bevor_expansion, SimulationEE_after_expansion
        try:
            exportFolder, folder1, folder2, zip_folder = main.re_simulation()
        except:
            error_memory = True
            return [[html.P([
                'The simulation might take up to 10 minutes', html.Br(),
                'Do not press the button twice or all simulation progress will be lost!!!', html.Br(),
                html.Span('ERROR: Provided data was not in expected format! Please refresh the browser and try again.',
                          style={'textDecoration': 'underline'})
            ])], {'display': 'none'}, {'display': 'inline'}, 'Start']

        cost_report_sum = [x for x in os.listdir(exportFolder) if 'CostReport_gesamt' in x]
        cost_report_wind = [x for x in os.listdir(exportFolder) if 'CostReport_wka' in x]
        cost_report_storage = [x for x in os.listdir(exportFolder) if 'CostReport_storage' in x]
        ausgebaute_flaeche = [x for x in os.listdir(exportFolder) if 'AusgebauteFlaechen' in x]
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

        final_file = list_files[-1]
        datasheet_final = list_files[0]

        global df_cost_report_sum
        global df_cost_report_wind
        global df_cost_report_storage
        global df_ausbau_vor
        global df_ausbau_pot
        global df_analyse
        global df_datasheet
        global df_month_report

        # ---------------------------------------------------------------------------------------------------
        # cost reports

        df_cost_report_sum = pd.read_csv(exportFolder + '/' + cost_report_sum[0], sep=';', decimal=',', encoding='utf-8')
        df_cost_report_sum = df_cost_report_sum.round(2)

        if len(cost_report_wind) != 0:
            df_cost_report_wind = pd.read_csv(exportFolder + '/' + cost_report_wind[0], sep=';', decimal=',', encoding='utf-8')
        else:
            df_cost_report_wind = pd.DataFrame()

        if len(cost_report_storage) != 0:
            df_cost_report_storage = pd.read_csv(exportFolder + '/' + cost_report_storage[0], sep=';', decimal=',',
                                                 encoding='utf-8')
        else:
            df_cost_report_storage = pd.DataFrame()

        # ---------------------------------------------------------------------------------------------------

        df_ausbau_vor = pd.read_csv(exportFolder + '/' + ausgebaute_flaeche[0], sep=';', decimal=',', encoding='utf-8',
                                    usecols=['StadtVor', 'haVor', 'Coords Vor', 'ID_Weatherstation_Vor', 'Wetter-ID_Vor',
                                             'Anzahl WEAs_Vor', 'nettoFreieFlaeche_Vor', 'Modell_Vor', 'Anzahl_Vor',
                                             'InvestKosten_inMio_Vor', 'Leistung_inMW_Vor'])
        df_ausbau_pot = pd.read_csv(exportFolder + '/' + ausgebaute_flaeche[0], sep=';', decimal=',', encoding='utf-8',
                                    usecols=['StadtPot', 'haPot', 'Coords Pot', 'ID_Weatherstation_Pot', 'Wetter-ID_Pot',
                                             'Anzahl WEAs_Pot', 'nettoFreieFlaeche_Pot', 'Modell_Pot', 'Anzahl_Pot',
                                             'InvestKosten_inMio_Pot', 'Leistung_inMW_Pot'])

        df_analyse = pd.read_csv(final_file, sep=';', decimal=',', encoding='utf-8')
        df_datasheet = pd.read_csv(datasheet_final, sep=';', decimal=',', encoding='utf-8')
        df_month_report = pd.read_csv(final_month, sep=';', decimal=',', encoding='utf-8')

        # ----------------------------------------------------------------------------------------------------------------------

        coords_to_lat_lon(df_ausbau_vor, 'Coords Vor')
        coords_to_lat_lon(df_ausbau_pot, 'Coords Pot')

        df_ausbau_vor = df_ausbau_vor[df_ausbau_vor['Wetter-ID_Vor'] != 0]
        df_ausbau_vor = df_ausbau_vor.sort_values(by=['ID_Weatherstation_Vor'])
        df_ausbau_vor['haVor'] = df_ausbau_vor['haVor'].map(float)
        df_ausbau_vor = df_ausbau_vor[
            ['StadtVor', 'ID_Weatherstation_Vor', 'haVor', 'Anzahl WEAs_Vor', 'nettoFreieFlaeche_Vor', 'Modell_Vor',
             'Anzahl_Vor', 'InvestKosten_inMio_Vor', 'Latitude', 'Longitude', 'Leistung_inMW_Vor']]

        df_ausbau_pot = df_ausbau_pot[df_ausbau_pot['Wetter-ID_Pot'] != 0]
        df_ausbau_pot = df_ausbau_pot.sort_values(by=['ID_Weatherstation_Pot'])
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

        global hours_goal

        year_hours = df_analyse['EE>100%'].count()
        true_count = df_analyse['EE>100%'].tolist().count(True)
        hours_goal = 0
        goal_name = ''
        if storage_expansion_sw:
            goal_name = 'storage expansion'
            hours_goal = storage_expansion_value / 100
        elif wind_expansion:
            goal_name = 'wind expansion'
            hours_goal = wind_expansion_value / 100

        reached_percentage = true_count / year_hours

        if hours_goal == 0:
            results_text = html.Div([
                html.P('No goal was set.'),
                html.B(),
                html.P(f'Without expanding wind or energy storages the simulation achieved 100% RE '
                       f'for {round(reached_percentage * 100, 1)}% of the time.')
            ])
        elif reached_percentage >= hours_goal:
            results_text = html.Div([
                html.P('The set goal was reached.'),
                html.B(),
                html.P(f'Goal: {hours_goal * 100} % (with {goal_name})'),
                html.B(),
                html.P(f'Reached: {round(reached_percentage * 100, 1)} %')
            ])
        else:
            results_text = html.Div([
                html.P('The set goal was not reached.'),
                html.B(),
                html.P(f'Goal: {hours_goal * 100} % (with {goal_name})'),
                html.B(),
                html.P(f'Reached: {round(reached_percentage * 100, 1)} %')
            ])

        settings = [
            f'Own data: {exmpl_sw}\n'
            f'Simulation year: {year}\n'
            f'Eisman: {eisman_sw}\n'
            f'Eisman wind speeds: {eisman_wind}\n'
            f'Eisman power regulation: {eisman_percentage}\n'
            f'Use biomass: {bio_sw}\n'
            f'Biomass expansion: {bio_inp}%\n'
            f'Use solar Power: {solar_sw}\n'
            f'Solar Power expansion: {solar_inp}%\n'
            f'Expand wind: {wind_expansion}\n'
            f'Use planned wind turbines: {planned_wind}\n'
            f'Wind expansion goal: {wind_expansion_value}%\n'
            f'Wind expansion methods: {methods_wind}\n'
            f'Use storage: {storage_sw}\n'
            f'Expand storage: {storage_expansion_sw}\n'
            f'Start capacity: {start_capacity_value}%\n'
            f'Storage expansion goal: {storage_expansion_value}%\n'
            f'Safety padding: {safety_padding_value}%\n'
            f'Storage expansion options: {storage_options}\n'
        ]

        make_settings_text(settings)

        main.createZIP(folder1, folder2, zip_folder)

        return [results_text, {'display': 'inline'}, {'display': 'none'}, 'Back']

    elif results_value['display'] == 'inline' and settings_value['display'] == 'none':

        return [[html.P('The simulation might take up to 10 minutes'),
                 html.B(),
                 html.P('Do not press the button twice or all simulation progress will be lost!!!')],
                {'display': 'none'}, {'display': 'inline'}, 'Start']
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
    # host='141.22.13.112'
