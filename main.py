import pandas as pd
from pathlib import Path
from datetime import datetime
import database
import database as db
import geo
import geo as gpd
import internetDownload as itd
import main
import sandbox
import dataPreparation as dataprep
import logik as lgk
import time
import shutil
import os,zipfile
import matplotlib.pyplot as plt

'''def start_mainDataBase(META_EE_Anteil,META_EE_Speicher ):

    if __name__ == '__main__':'''
# Meta_GUI_OFF = True
global META_EE_Anteil  # Muss Decimal angegeben werden 0.75
global META_EE_Speicher  # Grenzwert bis Speicher nicht mehr ausgebaut werden 100% 1.0
global META_year  # 2020
'- - - - - - - - - - - - - - - - - - - -'
'BIO'
global META_biomasse  # True
global META_expansionBio  # in Prozent 0.00
'- - - - - - - - - - - - - - - - - - - -'
'PV'
global META_PV  # True
global META_expansionPV  # in Prozent 0.00
'- - - - - - - - - - - - - - - - - - - -'
'Eisman'
global META_eisman # True on False off
global META_first_wind_limit # 13ms
global META_sec_wind_limit # 19ms
global META_third_wind_limit # 25ms
global META_first_power_limit # 0.6
global META_sec_power_limit # 0.3
global META_third_power_limit # 0.0

'- - - - - - - - - - - - - - - - - - - -'
'WKA'
global META_wind  # = True
global META_expansionWind  # = True
global META_be_planned_expansion  # = False

global META_faktorAusbauFlDist  # 1.0  # in Kilometer
global META_VorFl  # = True  # True -> Ausbauflaeche wird genutzt
global META_PotFl  # = True  # True -> Ausbauflaeche wird genutzt
global META_repowering  # = False  # True -> Anlagen >10 Jahre oder <1500KW Leistung werden abgerissen und neu gebaut (2:1)

global META_ausbaubegrenzungsfaktor  # = 0.5 #WIRD NOCH BENÖTIGT. MOMENTAN OHNE FUNKTION
global META_negativ_Graph_methode  # = True  # True = Kompch False = Gildenstern
global META_windanalyse  # = False
'Speicher'
global META_use_storage # True use False ignore
global META_startcapacity  # = 0.8  # Angabe in Prozent wie voll die Speicher im Startpunkt sind
global META_storage_safety_padding  # = 1.20  # Wieviel safty Speicher ausgebaut werden soll zusätzlich

global META_storage_before_expansion  # = True  # True -> vor Ausbau Analyse beachtet Speicher
global META_storage_expansion  # = True  # True -> Speicher werden ausgebaut
global META_Laegerdorf  # = True
global META_max_compressed_air  # = 13500000000
global META_compressed_air  # = True

'- - - - - - - - - - - - - - - - - - - -'
'DATABASE'

global META_DATA_generate_windenergy_plannendareas  # = False # True wenn die Liste erstellt werden soll
global META_DATA_verbrauch_komuliert  # = False  # True wenn die Liste erstellt werden soll

global META_DATA_DBWKAreload  # = False  # True wenn die DB der WKA Lastgänge erstellt werden soll
global META_DATA_DB_min_hight  # = 100 # Wert gibt die min höhe der WKA für die DB Lastgänge erstellt werden soll
global META_DATA_plannedAreas_potVor_getCoords  # = False  # True wenn die Ausbauflächen keine Standorte besitzen
#                                           -> Wetterstationen werden ebenfalls hinzugefügt
global META_DATA_plannedAreas_potVor_getWeather  # = False  # True wenn die Ausbauflächen keine zugeordnete Wetterstation besitzen
global META_DATA_be_plannedWKA_getCoords  # = False  # True wenn die Coords zugeordnet werden müssen

global META_DATA_be_plannedWKA_getWeatherID  # = False  # True wenn die Weather ID zugeordnet werden muss
global META_DATA_be_plannedWKA_power  # False  # True wenn die Leistung ausgerechnet werden muss
global META_DATA_pv_power  # = False  # True wenn die Leistung von PV erneut gerechnet werden muss
global META_DATA_wind_power  # = False  # True wenn die Leistung von Wind erneut gerechnet werden muss
global META_DATA_eisman


def set_globals():

    main.META_EE_Anteil = 0.75  # Muss Decimal angegeben werden
    main.META_EE_Speicher = 0.90  # Grenzwert bis Speicher nicht mehr ausgebaut werden 100%
    main.META_year = 2019
    '- - - - - - - - - - - - - - - - - - - -'
    'BIO'
    main.META_biomasse = True
    main.META_expansionBio = 0.00  # in Prozent
    '- - - - - - - - - - - - - - - - - - - -'
    'PV'
    main.META_PV = True
    main.META_expansionPV = 0.00  # in Prozent
    '- - - - - - - - - - - - - - - - - - - -'

    'Eisman'
    main.META_eisman = True
    main.META_first_wind_limit = 13
    main.META_sec_wind_limit = 19
    main.META_third_wind_limit = 25
    main.META_first_power_limit = 0.6
    main.META_sec_power_limit = 0.3
    main.META_third_power_limit = 0.0
    '- - - - - - - - - - - - - - - - - - - -'
    'WKA'
    main.META_wind = True
    main.META_expansionWind = True
    main.META_be_planned_expansion = True

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
    main.META_storage_safety_padding = 0.00  # Wieviel safty Speicher ausgebaut werden soll zusätzlich

    main.META_use_storage = True
    main.META_storage_before_expansion = True  # True -> vor Ausbau Analyse beachtet Speicher
    main.META_storage_expansion = True  # True -> Speicher werden ausgebaut
    main.META_Laegerdorf = True
    main.META_max_compressed_air = 13500000000
    main.META_compressed_air = True
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


def re_simulation():
    print('Start der Simulation')
    print(main.META_DATA_verbrauch_komuliert)
    print('1. Datenlage wird überprüft und ggf. erneuert')
    '- - - - - - - - - - - - - - - - - - - -'
    'Wert nicht wichtig für die GUI'
    temp_ausbau = False  #
    PV_Gesamt = 0
    erz_Bio = 0
    be_planned_wka_power = 0
    Wind_Gesamt = 0
    '- - - - - - - - - - - - - - - - - - - -'

    'General'
    META_DATA_Inputcsv = 'utf-8'  # wird für das einlesen der Daten verwendet
    META_DATA_OUTPUTcsv = 'utf-8-sig'  # wird für das auslesen der Daten verwendet

    '---------------------------------------------------------------------------------------------------------'
    '!!!WICHTIGE DATEN!!!' \
    'ohne diese Daten kann keine Simulation gestartet werden'

    try:
        openfilename = 'Datenbank/Wetter/StundeWindStationen_Coords.csv'
        print(openfilename)
        windWeatherStation = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)
        raise RuntimeError('Programmabbruch da die Wetterstationen für Wind nicht eingelesen werden konnten\n'
                        'falsches Format: ', openfilename)

    try:
        openfilename = 'Datenbank/Wetter/StundeSolarStationen_Coords.csv'
        print(openfilename)
        solarWeatherStation = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)
        raise RuntimeError('Programmabbruch da die Wetterstationen für Solar nicht eingelesen werden konnten')

    try:
        openfilename = 'Datenbank/WEAModell/WEAModell.csv'
        print(openfilename)
        WEAModell = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='latin1')
    except:
        print('falsches Format: ', openfilename)
        raise RuntimeError('Programmabbruch da die Modelle der WEA nicht eingelesen werden konnten')

    '---------------------------------------------------------------------------------------------------------'
    'Verbrauch'
    if main.META_DATA_verbrauch_komuliert == False:
        try:
            openfilename = "Datenbank/Verbrauch/Verbrauch_komuliert_" + str(META_year) + ".csv"
            print(openfilename)
            verbrauch_HH_SH = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            main.META_DATA_verbrauch_komuliert = True

    '---------------------------------------------------------------------------------------------------------'
    'WETTER'
    try:
        openfilename = 'Datenbank/Wetter/Wind_Wetterdaten_' + str(main.META_year) + '.csv'
        print(openfilename)
        windWeatherData = pd.read_csv(openfilename, delimiter=';', decimal=',', header=0, encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)

    try:
        openfilename = 'Datenbank/Wetter/PV_Wetterdaten_' + str(main.META_year) + '.csv'
        print(openfilename)
        solarWeatherData = pd.read_csv(openfilename, delimiter=';', decimal=',', header=0, encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)

    '---------------------------------------------------------------------------------------------------------'
    'ERZEUGUNG'

    'GESAMT PV'
    if main.META_PV == True:
        try:
            openfilename = 'Datenbank/Erzeugung/Erz_komuliert_' + str(main.META_year) + '_PV.csv'
            print(openfilename)
            PV_Gesamt = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            main.META_DATA_pv_power = True

    'GESAMT BIOMASSE'
    if main.META_biomasse == True:
        try:
            openfilename = 'Datenbank/Erzeugung/Erz_komuliert_Biomasse_' + str(main.META_year) + '.csv'
            print(openfilename)
            erz_Bio = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            raise RuntimeError('Programmabbruch da Jahresverlauf der Biomasse nicht eingelesen werden konnten')

    'GESAMT WIND'
    if main.META_wind == True:
        if main.META_eisman == False and main.META_DATA_wind_power == False:
            try:
                openfilename = 'Datenbank/Erzeugung/Erz_komuliert_' + str(main.META_year) + '_Wind.csv'
                print(openfilename)
                Wind_Gesamt = pd.read_csv(openfilename, delimiter=';', encoding='utf-8',decimal=',')
            except:
                print('falsches Format: ', openfilename)
                main.META_DATA_wind_power = True

        if main.META_eisman == True and main.META_DATA_wind_power == False:
            try:
                eisman_name = 'eisman_' + str(main.META_first_wind_limit) + '_' + str(
                    main.META_sec_wind_limit) + '_' + str(main.META_third_wind_limit) + '_' + str(
                    main.META_first_power_limit) + '_' + str(main.META_sec_power_limit) + '_' + str(
                    main.META_third_power_limit)

                openfilename = 'Datenbank/Erzeugung/Erz_komuliert_' + str(main.META_year) + '_Wind_' + eisman_name + '.csv'
                print(openfilename)
                Wind_Gesamt = pd.read_csv(openfilename, delimiter=';', encoding='utf-8',decimal=',')
            except:
                print('falsches Format: ', openfilename)
                main.META_DATA_eisman = True


    'GESAMT bereits geplanter Ausbau'
    if main.META_DATA_generate_windenergy_plannendareas == False:
        if main.META_eisman == False:
            try:
                openfilename = 'Datenbank/Erzeugung/Erz_komuliert_geplanterAusbau_' + str(main.META_year) + '_Wind.csv'
                print(openfilename)
                be_planned_wka_power = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                main.META_DATA_generate_windenergy_plannendareas = True

        if main.META_eisman == True:
            try:
                eisman_name = 'eisman_' + str(main.META_first_wind_limit) + '_' + str(
                    main.META_sec_wind_limit) + '_' + str(main.META_third_wind_limit) + '_' + str(
                    main.META_first_power_limit) + '_' + str(main.META_sec_power_limit) + '_' + str(
                    main.META_third_power_limit)

                openfilename = 'Datenbank/Erzeugung/Erz_komuliert_geplanterAusbau_' + str(main.META_year) + '_Wind_' + eisman_name + '.csv'
                print(openfilename)
                be_planned_wka_power = pd.read_csv(openfilename, delimiter=';', encoding='utf-8',decimal=',')
            except:
                print('falsches Format: ', openfilename)
                main.META_DATA_generate_windenergy_plannendareas = True

    # theoretisch geprüft 14.01 AW
    '---------------------------------------------------------------------------------------------------------'
    'ALLGEMEIN AUSBAUFLÄCHEN'

    'AusbauFlächen -> freie Pot und Vor Flächen, je nach Entscheidung werden die Daten bearbeitet'
    if main.META_wind == True:
        'Area with coords and weather ID'
        if main.META_DATA_plannedAreas_potVor_getWeather == False and main.META_DATA_plannedAreas_potVor_getCoords == False:
            try:
                openfilename = 'Datenbank/ConnectwithID/AusbauStandorte_Coords_weatherID.csv'
                print(openfilename)
                expansion_area_wind_vorpot = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                main.META_DATA_plannedAreas_potVor_getWeather == True
        'Area with coords but without weather ID'
        if main.META_DATA_plannedAreas_potVor_getWeather == True and main.META_DATA_plannedAreas_potVor_getCoords == False:
            try:
                openfilename = 'Datenbank/ConnectwithID/AusbauStandorte_Coords.csv'
                print(openfilename)
                expansion_area_wind_vorpot = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                main.META_DATA_plannedAreas_potVor_getCoords = True

        'Area without coords and weather ID'
        if main.META_DATA_plannedAreas_potVor_getWeather == True and main.META_DATA_plannedAreas_potVor_getCoords == True:
            try:
                openfilename = 'Datenbank/Ausbauflaechen/AusbauStandorte_gesamt_SH/AlleStandorte.csv'
                print(openfilename)
                expansion_area_wind_vorpot = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                raise RuntimeError('Programmabbruch da die Vorrang- und Potentialflächen nicht eingelesen werden konnten')

    #theoretisch geprüft 14.01 AW

    'Ausbau der bereits geplanten WKA Anlagen'
    if main.META_be_planned_expansion == True:
        'Area with coords and weather ID'
        if main.META_DATA_be_plannedWKA_getCoords == False and main.META_DATA_be_plannedWKA_getWeatherID == False:
            try:
                openfilename = 'Datenbank/ConnectwithID/Erzeugung/WindparksSH_geplanterAusbau_UTM_WeatherID_2019_2020.csv'
                print(openfilename)
                plannedWKA_areas = pd.read_csv(openfilename, delimiter=';', encoding='utf-8', decimal=',', na_values=0)
                plannedWKA_areas = plannedWKA_areas.fillna(0)
            except:
                print('falsches Format: ', openfilename)
                main.META_DATA_be_plannedWKA_getCoords == True
        'Area with coords but without weather ID'
        if main.META_DATA_be_plannedWKA_getCoords == False and main.META_DATA_be_plannedWKA_getWeatherID == True:
            try:
                openfilename = 'Datenbank/ConnectwithID/Erzeugung/WindparksSH_WetterID_2019_UTM'
                print(openfilename)
                plannedWKA_areas = pd.read_csv(openfilename, delimiter=';', encoding='utf-8', decimal=',', na_values=0)
                plannedWKA_areas = plannedWKA_areas.fillna(0)
            except:
                print('falsches Format: ', openfilename)
                main.META_DATA_be_plannedWKA_getCoords == True
                main.META_DATA_be_plannedWKA_getWeatherID = True
        'Area without coords and weather ID'
        if main.META_DATA_be_plannedWKA_getCoords == True and main.META_DATA_be_plannedWKA_getWeatherID == True:
            try:
                openfilename = 'Datenbank/ConnectwithID/Erzeugung/WindparksSH_geplanterAusbau.csv'
                print(openfilename)
                plannedWKA_areas = pd.read_csv(openfilename, delimiter=';', encoding='utf-8', decimal=',', na_values=0)
                plannedWKA_areas = plannedWKA_areas.fillna(0)
            except:
                print('falsches Format: ', openfilename)
                raise RuntimeError('Programmabbruch da die WKA des geplanten Ausbaus nicht eingelesen werden konnten')

    # theoretisch geprüft 14.01 AW
    '----------------------------------------------------------------------------------------------------------------------'
    "Öffnen der verschiedenen WEA Modelle."
    "KEY = MODELL -> Modell Name"
    temp_WKA = lgk.wea_modell_dictionary_class(WEAModell, useImport=False)
    dictWKAModell = temp_WKA.getdict()

    "Öffnen der verschiedenen Wetterstationen."
    "KEY = ID -> NUMMER der Wettersation"
    temp_WeatherID = lgk.weather_station_dictionary_class(windWeatherStation, useImport=False)
    dictWeatherID = temp_WeatherID.getdict()
    # print(temp_WeatherID.printWetterStation())
    "Öffnen der verschiedenen Speicher"
    listStorage = []

    if main.META_storage_before_expansion == True and main.META_use_storage == True:

        storage = lgk.StorageModell('PumpspeicherKraftwerk-Geesthacht', 'Geesthacht', 600000,
                                    main.META_startcapacity * 600000, 0.8, 120000, 0.0, 0.08)

        listStorage.append(storage)
        print('Storage is allocated', listStorage[-1].modell)

    '-----------------------------------------------------------------------------------------------------------------'
    'ERZEUGUNG NEU BERECHNEN'
    weatherIDlist = windWeatherStation['Stations_id'].tolist().copy()

    if main.META_DATA_pv_power == True and main.META_PV == True:
        # STATIONEN VORHER NOCH GEPRÜFT WERDEN
        lgk.generation_PV_energy(main.META_year, 'PV', 'HH')
        lgk.generation_PV_energy(main.META_year, 'PV', 'SH')
        openfilename = 'Datenbank/Erzeugung/Erz_komuliert_' + str(main.META_year) + '_PV.csv'

        PV_Gesamt = lgk.erzeugungPerStunde(main.META_year, openfilename, 'PV', weatherIDlist)

    if main.META_wind == True:
        if main.META_DATA_wind_power == True or main.META_DATA_eisman == True:
            print('new wind energy will be creat')
            eisman_name = 'eisman_' + str(main.META_first_wind_limit) + '_' + str(
                main.META_sec_wind_limit) + '_' + str(main.META_third_wind_limit) + '_' + str(
                main.META_first_power_limit) + '_' + str(main.META_sec_power_limit) + '_' + str(
                main.META_third_power_limit)

            # STATIONEN VORHER NOCH ÜBERPRÜFEN
            leistung_eisman = lgk.generation_wind_energy(main.META_year, dictWKAModell, dictWeatherID, 'Wind', 'HH',
                                        main.META_first_wind_limit,
                                        main.META_sec_wind_limit, main.META_third_wind_limit,
                                        main.META_first_power_limit, main.META_sec_power_limit,
                                        main.META_third_power_limit, eisman=main.META_eisman)
            print('Fertig mit Erzeugung HH')
            leistung_eisman += lgk.generation_wind_energy(main.META_year, dictWKAModell, dictWeatherID, 'Wind', 'SH',
                                        main.META_first_wind_limit,
                                        main.META_sec_wind_limit, main.META_third_wind_limit,
                                        main.META_first_power_limit, main.META_sec_power_limit,
                                        main.META_third_power_limit, eisman=main.META_eisman)

            print('Fertig mit Erzeugung SH')

            if main.META_DATA_eisman == True:


                openfilename = 'Datenbank/Erzeugung/Erz_komuliert_' + str(main.META_year) + '_Wind_' + eisman_name + '.csv'

                Wind_Gesamt = lgk.erzeugungPerStunde(main.META_year, openfilename, 'Wind', weatherIDlist,
                                                    complete_export=True, eisman= True)
                Wind_Gesamt['verluste_eisman_wind'] = leistung_eisman
            else:
                openfilename = 'Datenbank/Erzeugung/Erz_komuliert_' + str(main.META_year) + '_Wind.csv'
                Wind_Gesamt = lgk.erzeugungPerStunde(main.META_year, openfilename, 'Wind', weatherIDlist,
                                                     complete_export=True, eisman= False)
    '-----------------------------------------------------------------------------------------------------------------'
    '''Funktionen welche nur einmal Aufgerufen werden. Diese dienen nur zur Datenvorbereitung. 
        Sie haben nichts mit der Datenanlyse zu tun. Die Analyse finden gesondert statt.'''
    'Verbrauch HH und SH'
    if main.META_DATA_verbrauch_komuliert == True:
        print('verbrauchGesamt reload will be regenerated and reloaded')
        verbrauch_HH_SH = lgk.verbrauchGesamt(main.META_year)
    '-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -'
    'expansion area Vor and Pot'
    if main.META_wind == True:
        'Ausbauflaechen get Coords and get Weather ID'
        if main.META_DATA_plannedAreas_potVor_getCoords == True:
            print('plannedAreasgetCoords will be regenerated and reloaded')
            expansion_area_wind_vorpot = dataprep.plannendAreas_getCoords(expansion_area_wind_vorpot, export=True)
            expansion_area_wind_vorpot = dataprep.plannedAreas_getWeather(expansion_area_wind_vorpot, windWeatherStation,
                                                                          export=True)
        'Ausbauflaechen with Coords get Weather ID'
        if main.META_DATA_plannedAreas_potVor_getWeather == True:
            print('plannedAreas_getWeather will be regenerated and reloaded')
            expansion_area_wind_vorpot = dataprep.plannedAreas_getWeather(expansion_area_wind_vorpot, windWeatherStation,
                                                                          export=True)

    'be plannend area without Coords and without weather ID'
    if main.META_be_planned_expansion ==True:
        if main.META_DATA_be_plannedWKA_getCoords == True and main.META_DATA_be_plannedWKA_getWeatherID == True:
            print('plannedAreasgetCoords will be regenerated and reloaded')
            temp_exportname = 'Datenbank/ConnectwithID/Erzeugung/WindparksSH_geplanterAusbau_UTM_WeatherID_2019_2020.csv'
            plannedWKA_areas = db.utm_to_gk(META_year, temp_exportname, plannedWKA_areas)
            plannedWKA_areas = dataprep.plannedWKA_toUTM_and_connectWeahterID(windWeatherStation, plannedWKA_areas)
            main.META_DATA_generate_windenergy_plannendareas = True
        'be plannend area with Coords but without weather ID'
        if main.META_DATA_be_plannedWKA_getWeatherID == True and main.META_DATA_be_plannedWKA_getCoords == False:
            plannedWKA_areas = dataprep.plannedWKA_toUTM_and_connectWeahterID(windWeatherStation, plannedWKA_areas)
            main.META_DATA_generate_windenergy_plannendareas = True
        'be plannend area with Coords but without weather ID'
        if main.META_DATA_generate_windenergy_plannendareas == True:
            temp_beplanned = lgk.erzeugung_WKA_areawith_weatherID(META_year, windWeatherData, plannedWKA_areas,
                                                                        dictWKAModell,dictWeatherID,
                                                                        META_first_wind_limit=main.META_first_wind_limit,
                                                                        META_sec_wind_limit=main.META_sec_wind_limit,
                                                                        META_third_wind_limit=main.META_third_wind_limit,
                                                                        META_first_power_limit=main.META_first_power_limit,
                                                                        META_sec_power_limit=main.META_sec_power_limit,
                                                                        META_third_power_limit=main.META_third_power_limit,
                                                                         export=True, eisman=main.META_eisman)

            be_planned_wka_power = temp_beplanned[0]
            be_planned_eisman = temp_beplanned[1]
            'Summe der einzelnen WKA Anlagen'
            if main.META_eisman == False:
                temp_exportname = 'Datenbank/Erzeugung/Erz_komuliert_geplanterAusbau_' + str(META_year) + '_Wind.csv'

            if main.META_eisman == True:
                eisman_name = 'eisman_' + str(main.META_first_wind_limit) + '_' + str(
                    main.META_sec_wind_limit) + '_' + str(main.META_third_wind_limit) + '_' + str(
                    main.META_first_power_limit) + '_' + str(main.META_sec_power_limit) + '_' + str(
                    main.META_third_power_limit)

                temp_exportname = 'Datenbank/Erzeugung/Erz_komuliert_geplanterAusbau_' + str(
                    main.META_year) + '_Wind_' + eisman_name + '.csv'

            be_planned_wka_power = lgk.erzeugungPerStunde_singleFrame(META_year, be_planned_wka_power, temp_exportname,
                                                                      eisman_list=be_planned_eisman,
                                                                      eisman=main.META_eisman,
                                                                      export=True)



    # lgk.erzeugungPerStunde(2019, 'Wind', weatherIDlist, single_ID_export= True )
    # lgk.erzeugungPerStunde(2020, 'Wind', weatherIDlist, single_ID_export=True)
    '----------------------------------------------------------------------------------------------------------------------'
    if main.META_DATA_DBWKAreload == False:
        if main.META_eisman == False:
            try:
                openfilename = 'Datenbank/WEAModell/DB_WKA_' + str(main.META_year) + '_' + str(
                    main.META_DATA_DB_min_hight) + '.csv'
                print(openfilename)
                DB_WKA = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                print('Datenbank konnte nicht geöffnet werden')
                print('Datenbank wird automatisch erzeugt')
                main.META_DATA_DBWKAreload = True
        if main.META_eisman == True:
            eisman_name = 'eisman_' + str(main.META_first_wind_limit) + '_' + str(
                main.META_sec_wind_limit) + '_' + str(main.META_third_wind_limit) + '_' + str(
                main.META_first_power_limit) + '_' + str(main.META_sec_power_limit) + '_' + str(
                main.META_third_power_limit)
            try:
                openfilename = 'Datenbank/WEAModell/DB_WKA_' + str(main.META_year) + '_' + str(
                    main.META_DATA_DB_min_hight)+'_'+str(eisman_name)+ '.csv'
                print(openfilename)
                DB_WKA = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                print('Datenbank konnte nicht geöffnet werden')
                print('Datenbank wird automatisch erzeugt')
                main.META_DATA_DBWKAreload = True
    'DatenBank WKA'
    if main.META_DATA_DBWKAreload == True:
        print('DBWKA reload will be regenerated and reloaded')
        DB_WKA = lgk.DB_WKA(main.META_year, dictWKAModell, dictWeatherID, windWeatherData, main.META_DATA_DB_min_hight,
                            META_first_wind_limit=main.META_first_wind_limit,
                            META_sec_wind_limit=main.META_sec_wind_limit,
                            META_third_wind_limit=main.META_third_wind_limit,
                            META_first_power_limit=main.META_first_power_limit,
                            META_sec_power_limit=main.META_sec_power_limit,
                            META_third_power_limit=main.META_third_power_limit,
                            export=True, eisman=main.META_eisman)


    #theoretisch und praktisch geprüft 14.01 AW
    '______________________________________________________________________________________________________________________'
    # dataprep.plannedAreas_toUTM_and_connectWeahterID('Wind', 'SH', windWeatherStation)
    # dataprep.erzeugung_plannendAreas(META_year, plannedWKA)
    # lgk.erzeugungPerStunde(META_year, 'Wind')
    # temp_windlastprofil = lgk.windlastprofil(META_year)
    # lgk.standortquality(META_year, windWeatherData, WEAModell)
    # db.utm_to_gk(2019, 'Wind', 'SH')
    # db.utm_to_gk(2019, 'Wind', 'HH')
    # db.utm_to_gk(2020, 'Wind', 'SH')
    # db.utm_to_gk(2020, 'Wind', 'HH')
    '______________________________________________________________________________________________________________________'
    "KEY FACTORS zum Ausbau -> muss noch angepasst werden"
    "Analyse wird mit allen Dateien in einem eigenen Ordner gespeichert"
    uhrzeit = datetime.now().strftime('%d-%m-%Y_%H-%M')
    exportFolder = 'REE_AnalyseCompleted/REE_Analysejahr_' + str(main.META_year) + '_' + str(uhrzeit) + '/'
    export_folder_for_gui = 'REE_AnalyseCompleted/REE_Analysejahr_' + str(main.META_year) + '_' + str(uhrzeit)
    export_zip_folder = 'REE_AnalyseCompleted/REE_Analysejahr_' + str(main.META_year) + '_' + str(uhrzeit)
    export_ziel_folder = exportFolder + 'export'
    path = Path(exportFolder)
    path.mkdir(parents=True, exist_ok=True)
    '------------------------------------------------------------------------------------------------------------------'
    'Muss noch überarbeitet werden'



    '------------------------------------------------------------------------------------------------------------------'
    '--------------------------------------------!-!-!SIMULATIONSSTART!-!-!--------------------------------------------'
    '------------------------------------------------------------------------------------------------------------------'
    list_count_expansion_wka = []
    list_count_expansion_power = []
    list_name_expansion_wka = []
    list_key_expansion_wka = []
    list_energy_per_year = []
    "Erste Simulation ohne einen Ausbau durch die Software"
    "In Bearbeitung"
    if main.META_windanalyse == True:
        try:
            openfilename = 'Datenbank/Wetter/WindAnalyse/Windanlyse_' + str(META_year) + '.csv'
            print(openfilename)
            windanlyse = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            windanlyse = lgk.windlastprofil(META_year, exportFolder, export=True, )

        # Export in Simulationsordner
        exportname2 = exportFolder + 'Windanlyse_' + str(META_year) + '.csv'
        windanlyse.to_csv(exportname2, sep=';', encoding='utf-8-sig', index=True, decimal=',')

    # PV_Gesamt = lgk.erzeugungPerStunde(year, 'PV')
    # Wind_Gesamt = lgk.erzeugungPerStunde(year, 'Wind')
    if main.META_be_planned_expansion == True:
        del be_planned_wka_power['Datum']
    if main.META_PV == True:
        del PV_Gesamt['Datum']
    if main.META_biomasse == True:
        del erz_Bio['Datum']

    del DB_WKA['Datum']
    # EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung], axis=1, sort=False)

    temp_wind = Wind_Gesamt.copy()  # ->wird für die Darstellung der Daten benötigt
    print('Erste Analyse startet')
    EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                               be_planned_wka_power,
                               verbrauch_HH_SH,key_name= 'beforREexpansion', ausbau=False, export=True,
                               geplanterAusbau= main.META_be_planned_expansion, biomes= main.META_biomasse,
                               wind=main.META_wind, PV= main.META_PV, expansionPV= main.META_expansionPV,
                               expansionBio=main.META_expansionBio, speicher= main.META_use_storage,
                               eisman=META_eisman)

    SimulationEE_vorAusbau = EE_Analyse[0].copy()
    export_simulation_bevor_expansion = SimulationEE_vorAusbau.copy()
    EE_Anteil = EE_Analyse[1]
    print('EE Anteil in Prozent vor Ausbau: ', round(EE_Anteil * 100, 2), '%')

    '------------------------------------------------------------------------------------------------------------------'
    "Überprüfung weleche Vor/Pot Flächen zur Verfügung stehen. "
    # Daten müssen nicht in den Export ORDNER!!!
    verbauteVor = lgk.connect_oldWKA_to_expansionArea(META_year, 'Vor', expansion_area_wind_vorpot,
                                                      META_faktorAusbauFlDist,export=False,
                                                      geplanterAusbau=META_be_planned_expansion)


    '''verbautPot = lgk.stand_distance_analyse(META_year, 'Pot', ausbauStandorte_Coords, META_faktorAusbauFlDist,
                                            export=False, geplanterAusbau=META_geplanterAusbau)'''
    dataframe_expansion_area = lgk.freie_ha_vor(META_year, exportFolder, expansion_area_wind_vorpot, verbauteVor, export=True)

    dataframe_expansion_area['Modell_Vor'] = ['-'] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['Anzahl_Vor'] = [0] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['Leistung_inMW_Vor'] = [0] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['InvestKosten_inMio_Vor'] = [0] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['BetriebsKosten_inMio_Vor'] = [0] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['Modell_Pot'] = ['-'] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['Anzahl_Pot'] = [0] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['Leistung_inMW_Pot'] = [0] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['InvestKosten_inMio_Pot'] = [0] * len(dataframe_expansion_area['ID'])
    dataframe_expansion_area['BetriebsKosten_inMio_Pot'] = [0] * len(dataframe_expansion_area['ID'])

    "Nun ist bekannt welche Potenzial Flächen und Welche Vorrangflächen frei Verfügbar sind."
    '______________________________________________________________________________________________________________________'
    "ProzentualerAusbau BIOMASSE/PV"
    expansionBio = 0
    expansionPV = 0
    if META_biomasse == True:
        print('expansion Bio')
        expansionBio = lgk.percentage_expansion(SimulationEE_vorAusbau['Erz_Biomasse_Gesamt'], main.META_expansionBio)
        print('New Energysum GWh: ', sum(expansionBio) / 1000000)
        sum_expansionBio = sum(expansionBio)
    if META_PV == True:
        print('expansion PV')
        expansionPV = lgk.percentage_expansion(SimulationEE_vorAusbau['Erzeugung_PV'], main.META_expansionPV)
        print('New Energysum GWh: ', sum(expansionPV)/1000000)
        sum_expansionPV = sum(expansionPV)
    if META_wind == True:
        expansionWind = [1] * len(SimulationEE_vorAusbau)
    '______________________________________________________________________________________________________________________'
    "!!!Ausbau WIND STARTET!!!"
    if main.META_expansionWind == True:
        temp_ausbau = True
        temp_ausgebauteAnlagen = ['test'] * len(SimulationEE_vorAusbau)
        expansionWind = [1] * len(SimulationEE_vorAusbau)
        expansionWind_eisman = [1] * len(SimulationEE_vorAusbau)

    def expansion_wind(pot_Vor, EE_Anteil, tempausbau_true):
        for i in range(len(dictWeatherID)):
            print('------------------------------------------------------')
            print('Start run: ', i, '/ max runs: ', len(dictWeatherID))
            print('EE Anteil in Prozent: ', round(EE_Anteil * 100, 2), '%')
            print('expansion EE Anteil border in Prozent: ', round(main.META_EE_Anteil * 100, 2), '%')

            start = time.process_time()
            temp_len_db_wka = len(temp_DB_WKA)
            if temp_len_db_wka == 0:
                print('------------------------------------------------------')
                print('no more WKA in DB -> expansion stopt for ', pot_Vor, '-Areas')
                print('------------------------------------------------------')
                break
            if i == 0:
                temp_wind = Wind_Gesamt.copy()
                EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                           be_planned_wka_power, verbrauch_HH_SH,
                                           expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                           geplanterAusbau=META_be_planned_expansion, biomes=META_biomasse,
                                           wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                           expansionBio=META_expansionBio, speicher=main.META_use_storage,
                                           eisman=main.META_eisman, ausbauWindeisman=expansionWind_eisman)

                EE_Anteil = EE_Analyse[1]
                print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                SimulationEE_nachAusbau = EE_Analyse[0].copy()

            elif i > 0 and temp_ausbau == True:
                temp_wind = Wind_Gesamt.copy()
                EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                           be_planned_wka_power, verbrauch_HH_SH,
                                           expansionWind, expansionPV, expansionBio,
                                           ausbauWindeisman=expansionWind_eisman, ausbau=temp_ausbau, export=False,
                                           geplanterAusbau=META_be_planned_expansion, biomes=META_biomasse,
                                           wind=META_wind, PV=META_PV, expansionPV=META_expansionPV, eisman=META_eisman,
                                           expansionBio=META_expansionBio, speicher=main.META_use_storage)

                EE_Anteil = EE_Analyse[1]
                print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                SimulationEE_nachAusbau = EE_Analyse[0].copy()

            if EE_Anteil >= main.META_EE_Anteil:
                print('FERTIG EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                break

            if tempausbau_true == True:
                if main.META_storage_before_expansion == False or main.META_use_storage == False:
                    temp_Diff_EE = SimulationEE_nachAusbau['Diff_EE_zu_Verb'].copy()
                else:
                    temp_Diff_E = SimulationEE_nachAusbau['Diff_EE_zu_Verb_nach_Speicher'].copy()
                    # print(type(temp_Diff_E))
                    temp_Diff_EE = temp_Diff_E.tolist()
                    # print(temp_Diff_EE)
                EE_Simulation_negativGraph = lgk.negativ_Verlauf(temp_Diff_EE,
                                                                 speicherVerlauf=META_negativ_Graph_methode)
                deepestPoints = lgk.deepest_point_negativGraph(EE_Simulation_negativGraph, 20)

            name_for_WKA_expansion = lgk.area_and_WKA_choice(EE_Simulation_negativGraph, temp_DB_WKA,
                                                             deepestPoints[1],
                                                             dataframe_expansion_area['Wetter-ID_' + pot_Vor].tolist(),
                                                             temp_ausgebauteAnlagen,
                                                             dictWKAModell,
                                                             spiecherMethodik=META_negativ_Graph_methode)
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
            'Muss noch überprüft werden'
            # max_Anzahl = lgk.maxAnzahl_WKA(deepestPoints[0], deepestPoints[1], DB_WKA, WKAnameforexpansion,
            # META_ausbaubegrenzungsfaktor)
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'

            try:
                temp_name = name_for_WKA_expansion.split('_')
                temp_ID = temp_name[0]
                temp_Modell = temp_name[1]
                temp_Modell_hight = temp_name[2]
            except:
                print(temp_name)
                continue
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'

            temp_ausgebauteAnlagen[i] = temp_name[0]
            keyfactors_expansion_area = lgk.expansion_WKA(main.META_year, temp_Modell + '_' + temp_Modell_hight, temp_ID,
                                                          dictWKAModell, dataframe_expansion_area,
                                                          windWeatherData, pot_Vor, eisman=main.META_eisman,
                                                          META_first_wind_limit=main.META_first_wind_limit,
                                                          META_sec_wind_limit=main.META_sec_wind_limit,
                                                          META_third_wind_limit=main.META_third_wind_limit,
                                                          META_first_power_limit=main.META_first_power_limit,
                                                          META_sec_power_limit=main.META_sec_power_limit,
                                                          META_third_power_limit=main.META_third_power_limit)

            # KeyFactors
            # 0 Energycurve | 1 column name | 2 count WKA | 3 Power total
            if sum(keyfactors_expansion_area[0]) == 0:
                print('Kein Ausbau mit der Anlage')
                tempausbau_true = False
                continue
            else:
                tempausbau_true = True

            for index, i in enumerate(expansionWind):
                expansionWind[index] = i + keyfactors_expansion_area[0][index]
                if main.META_eisman == True:
                    expansionWind_eisman[index] = expansionWind_eisman[index] + keyfactors_expansion_area[1][index]

            list_key_expansion_wka.append(name_for_WKA_expansion)
            list_name_expansion_wka.append(temp_Modell)
            list_count_expansion_wka.append(keyfactors_expansion_area[2])
            list_count_expansion_power.append(keyfactors_expansion_area[3])
            '''
            finished_filename = exportFolder + 'AusgebauteFlaechen_' + str(main.META_year) + '.csv'
            dataframe_expansion_area.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')'''
            end = time.process_time()
            if pot_Vor == 'Vor':
                temp_area = 'Vorranggebiet'
            elif pot_Vor == 'Pot':
                temp_area = 'Potenzialfläche'
            else:
                temp_area = 'unknown'
            print(temp_area, ':  End: ', i, 'Zeit: ', end - start, 'Name', name_for_WKA_expansion,
                  'Anzahl Neu: ', keyfactors_expansion_area[2], '/ Total: ', sum(list_count_expansion_wka))
            print('Leistung insgesamt zugebaut in MW: ', round(sum(list_count_expansion_power) / 1000,2),
                  'Leistung Neu:  ', round(keyfactors_expansion_area[3],2),
                  'Freie Fläche: ', round((sum(dataframe_expansion_area['nettoFreieFlaeche_Vor'])),3))

        return EE_Anteil
    print(list_count_expansion_wka)
    if main.META_wind == True and main.META_VorFl == True and EE_Anteil < main.META_EE_Anteil:
        if main.META_expansionWind == True:
            temp_DB_WKA = DB_WKA.copy()
            EE_Anteil = expansion_wind('Vor', EE_Anteil, temp_ausbau)
    print(list_count_expansion_wka)
    if main.META_wind == True and main.META_PotFl == True and EE_Anteil < main.META_EE_Anteil:
        if main.META_expansionWind == True:
            print('Start Pot')
            temp_ausgebauteAnlagen = ['test'] * len(expansionPV)
            temp_DB_WKA = DB_WKA.copy()

            EE_Anteil = expansion_wind('Pot', EE_Anteil, temp_ausbau)

    temp_wind = Wind_Gesamt.copy()

    if main.META_wind == True and main.META_expansionWind == True:
        if main.META_VorFl == True or main.META_PotFl == True or sum_expansionPV > 0 or sum_expansionBio > 0:

            EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                       be_planned_wka_power, verbrauch_HH_SH,
                                       expansionWind, expansionPV, expansionBio, key_name='afterREexpansion',
                                       ausbau=temp_ausbau, export=True, eisman=main.META_eisman,
                                       ausbauWindeisman = expansionWind_eisman,
                                       geplanterAusbau=META_be_planned_expansion, biomes=META_biomasse,
                                       wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                       expansionBio=META_expansionBio, speicher=main.META_use_storage)
            EE_Anteil = EE_Analyse[1]
            SimulationEE_after_expansion = EE_Analyse[0].copy()
            print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 6), '%')



    finished_filename = exportFolder + 'AusgebauteFlaechen_' + str(main.META_year) + '.csv'
    dataframe_expansion_area['ID_Weatherstation'] = ['test'] * len(dataframe_expansion_area['Wetter-ID_Pot'])
    for index, i in enumerate(dataframe_expansion_area['Wetter-ID_Pot']):
        if i == 0:
            dataframe_expansion_area['ID_Weatherstation'][index] = 'ignore'
            continue
        dataframe_expansion_area['ID_Weatherstation'][index] = str(i) + '_' + str(dictWeatherID[i]['NameORT'])

    dataframe_expansion_area.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')


    min_current_storage = 0.0
    storage_bevor = len(listStorage)
    if main.META_storage_expansion == True and main.META_use_storage == True:
        print('Speicherausbau')
        EE_anteil_bevor = EE_Anteil
        print('EE Anteil vor Ausbau', EE_anteil_bevor)
        while (min_current_storage <= main.META_storage_safety_padding and EE_Anteil < main.META_EE_Speicher):
            print('------------------------------------------------------')
            print('EE Anteil in Prozent: ', round(EE_Anteil * 100, 3), '%')
            print('EE MUSS in Prozent: ', round(META_EE_Speicher * 100, 3), '%')

            if main.META_storage_before_expansion == False:
                temp_Diff_EE = SimulationEE_after_expansion['Diff_EE_zu_Verb'].tolist()
            else:
                temp_Diff_EE = SimulationEE_after_expansion['Diff_EE_zu_Verb_nach_Speicher'].tolist()
            print('Storage Len: ', len(listStorage))
            if EE_Anteil == EE_anteil_bevor and storage_bevor < len(listStorage):
                print('Speicher AUSBAU macht keinen Sinn mehr')
                break
            lgk.expansion_storage(temp_Diff_EE, META_negativ_Graph_methode, listStorage, main.META_startcapacity,
                                  main.META_Laegerdorf, main.META_compressed_air, main.META_max_compressed_air,
                                  main.META_EE_Speicher)
            print('Storage Len: ', len(listStorage))

            EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                       be_planned_wka_power, verbrauch_HH_SH,
                                       expansionWind, expansionPV, expansionBio, key_name = 'afterStorageExpansion',
                                       ausbau=temp_ausbau, export=False,eisman=main.META_eisman,
                                       ausbauWindeisman = expansionWind_eisman,
                                       geplanterAusbau=main.META_be_planned_expansion, biomes=main.META_biomasse,
                                       wind=main.META_wind, PV=main.META_PV, expansionPV=main.META_expansionPV,
                                       expansionBio=main.META_expansionBio, speicher=main.META_storage_before_expansion)

            EE_export = EE_Analyse[2]
            EE_Anteil = EE_Analyse[1]
            SimulationEE_after_expansion = EE_Analyse[0].copy()
            print('EE Anteil in Prozent: ', round(EE_Anteil * 100, 6), '%')
            temp_min = min(SimulationEE_after_expansion['Diff_EE_zu_Verb_nach_Speicher'])
            print('lowest delta EE to consume: ', round(temp_min, 6))
            min_current_storage = min(SimulationEE_after_expansion['Speicher_voll_Prozent'])
            print('lowest Currentstorage in Prozent: ', round(min_current_storage * 100, 5), '%')

            main.META_Laegerdorf = False
            main.META_compressed_air = False

        print('Speicherausbau fertig')

        SimulationEE_after_expansion.to_csv(EE_export, sep=';', encoding='utf-8-sig', index=False, decimal=',')



    cost_report = lgk.cost_analysis(META_year, exportFolder, dictWKAModell, list_key_expansion_wka,
                                    list_count_expansion_wka, list_count_expansion_power, listStorage,
                                    cost_wind=main.META_expansionWind, cost_storage=main.META_storage_expansion,
                                    export=True)



    def createZIP(folder, filename, compress=zipfile.ZIP_DEFLATED):
        # ZIP Archive Öffnen
        with zipfile.ZipFile(filename + '.zip', 'w', compress) as target:
            for root, dirs, files in os.walk(folder):

                for file in files:
                    if 'export' in file:
                        continue

                    add = os.path.join(root, file)

                    # Datei zum ZIP Archive Hinzufügen
                    target.write(add)

                    print(add + ' wurde Hinzugefügt')


        # ZIP Archive vom Verzeichnis "bilder" erstellen.
    createZIP(export_zip_folder, export_ziel_folder)



    print('Simulation has ended')
    return export_folder_for_gui

'''
if Meta_GUI_OFF == True:
    set_globals()
    re_simulation()
'''