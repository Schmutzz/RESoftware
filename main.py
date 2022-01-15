import pandas as pd
from pathlib import Path
from datetime import datetime
import database
import database as db
import geo
import geo as gpd
import internetDownload as itd
import sandbox
import dataPreparation as dataprep
import logik as lgk
import time
import matplotlib.pyplot as plt

'''def start_mainDataBase(META_EE_Anteil,META_EE_Speicher ):

    if __name__ == '__main__':'''

print('Start der Simulation')
print('1. Datenlage wird überprüft und ggf. erneuert')

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
'WKA'
global META_wind  # = True
global META_expansionWind  # = True
global META_geplanterAusbau  # = False

global META_faktorAusbauFlDist  # 1.0  # in Kilometer
global META_VorFl  # = True  # True -> Ausbauflaeche wird genutzt
global META_PotFl  # = True  # True -> Ausbauflaeche wird genutzt
global META_repowering  # = False  # True -> Anlagen >10 Jahre oder <1500KW Leistung werden abgerissen und neu gebaut (2:1)

global META_ausbaubegrenzungsfaktor  # = 0.5 #WIRD NOCH BENÖTIGT. MOMENTAN OHNE FUNKTION
global META_negativ_Graph_methode  # = True  # True = Kompch False = Gildenstern
global META_windanalyse  # = False
'Speicher'
global META_startcapacity  # = 0.8  # Angabe in Prozent wie voll die Speicher im Startpunkt sind
global META_strorage_safty_compansion  # = 1.20  # Wieviel safty Speicher ausgebaut werden soll zusätzlich

global META_speichervorAusbau  # = True  # True -> vor Ausbau Analyse beachtet Speicher
global META_speicherausbau  # = True  # True -> Speicher werden ausgebaut
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



def testabcboje():

    '- - - - - - - - - - - - - - - - - - - -'
    'Wert nicht wichtig für die GUI'
    temp_ausbau = False  #

    '- - - - - - - - - - - - - - - - - - - -'
    'General'
    META_DATA_Inputcsv = 'utf-8'  # wird für das einlesen der Daten verwendet
    META_DATA_OUTPUTcsv = 'utf-8-sig'  # wird für das auslesen der Daten verwendet

    '---------------------------------------------------------------------------------------------------------'
    '!!!WICHTIGE DATEN!!!' \
    'ohne diese Daten kann keine Simulation gestartet werden'
    print(META_EE_Anteil)
    print(META_EE_Speicher)
    print(META_year)
    try:
        openfilename = 'Datenbank\Wetter/StundeWindStationen_Coords.csv'
        print(openfilename)
        windWeatherStation = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)
        raise RuntimeError('Programmabbruch da die Wetterstationen für Wind nicht eingelesen werden konnten')

    try:
        openfilename = 'Datenbank\Wetter/StundeSolarStationen_Coords.csv'
        print(openfilename)
        solarWeatherStation = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)
        raise RuntimeError('Programmabbruch da die Wetterstationen für Solar nicht eingelesen werden konnten')

    try:
        openfilename = 'Datenbank\WEAModell/WEAModell.csv'
        print(openfilename)
        WEAModell = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='latin1')
    except:
        print('falsches Format: ', openfilename)
        raise RuntimeError('Programmabbruch da die Modelle der WEA nicht eingelesen werden konnten')

    '---------------------------------------------------------------------------------------------------------'
    'Verbrauch'
    if META_DATA_verbrauch_komuliert == False:
        try:
            openfilename = "Datenbank\Verbrauch\Verbrauch_komuliert_" + str(META_year) + ".csv"
            print(openfilename)
            verbrauch_HH_SH = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            META_DATA_verbrauch_komuliert = True

    '---------------------------------------------------------------------------------------------------------'
    'WETTER'
    try:
        openfilename = 'Datenbank\Wetter/Wind_Wetterdaten_' + str(META_year) + '.csv'
        print(openfilename)
        windWeatherData = pd.read_csv(openfilename, delimiter=';', decimal=',', header=0, encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)

    try:
        openfilename = 'Datenbank\Wetter/PV_Wetterdaten_' + str(META_year) + '.csv'
        print(openfilename)
        solarWeatherData = pd.read_csv(openfilename, delimiter=';', decimal=',', header=0, encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)

    '---------------------------------------------------------------------------------------------------------'
    'ERZEUGUNG'

    'GESAMT PV'
    if META_PV == True:
        try:
            openfilename = 'Datenbank\Erzeugung/Erz_komuliert_' + str(META_year) + '_PV.csv'
            print(openfilename)
            PV_Gesamt = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            META_DATA_pv_power = True

    'GESAMT BIOMASSE'
    if META_biomasse == True:
        try:
            openfilename = 'Datenbank\Erzeugung/Erz_komuliert_Biomasse_' + str(META_year) + '.csv'
            print(openfilename)
            erz_Bio = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            raise RuntimeError('Programmabbruch da Jahresverlauf der Biomasse nicht eingelesen werden konnten')

    'GESAMT WIND'
    if META_wind == True:
        try:
            openfilename = 'Datenbank\Erzeugung/Erz_komuliert_' + str(META_year) + '_Wind.csv'
            print(openfilename)
            Wind_Gesamt = pd.read_csv(openfilename, delimiter=';', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            META_DATA_wind_power = True

    'GESAMT bereits geplanter Ausbau'
    if META_DATA_generate_windenergy_plannendareas == False:
        try:
            openfilename = 'Datenbank\Erzeugung/Erz_komuliert_geplanterAusbau_' + str(META_year) + '_Wind.csv'
            print(openfilename)
            be_planned_wka_power = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            META_DATA_generate_windenergy_plannendareas = True

    # theoretisch geprüft 14.01 AW
    '---------------------------------------------------------------------------------------------------------'
    'ALLGEMEIN AUSBAUFLÄCHEN'

    'AusbauFlächen -> freie Pot und Vor Flächen, je nach Entscheidung werden die Daten bearbeitet'
    if META_wind == True:
        'Area with coords and weather ID'
        if META_DATA_plannedAreas_potVor_getWeather == False and META_DATA_plannedAreas_potVor_getCoords == False:
            try:
                openfilename = 'Datenbank\ConnectwithID/AusbauStandorte_Coords_weatherID.csv'
                print(openfilename)
                expansion_area_wind_vorpot = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                META_DATA_plannedAreas_potVor_getWeather == True
        'Area with coords but without weather ID'
        if META_DATA_plannedAreas_potVor_getWeather == True and META_DATA_plannedAreas_potVor_getCoords == False:
            try:
                openfilename = 'Datenbank\ConnectwithID/AusbauStandorte_Coords.csv'
                print(openfilename)
                expansion_area_wind_vorpot = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                META_DATA_plannedAreas_potVor_getCoords = True

        'Area without coords and weather ID'
        if META_DATA_plannedAreas_potVor_getWeather == True and META_DATA_plannedAreas_potVor_getCoords == True:
            try:
                openfilename = 'Datenbank\Ausbauflaechen\AusbauStandorte_gesamt_SH/AlleStandorte.csv'
                print(openfilename)
                expansion_area_wind_vorpot = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
            except:
                print('falsches Format: ', openfilename)
                raise RuntimeError('Programmabbruch da die Vorrang- und Potentialflächen nicht eingelesen werden konnten')

    #theoretisch geprüft 14.01 AW

    'Ausbau der bereits geplanten WKA Anlagen'
    if META_geplanterAusbau == True:
        'Area with coords and weather ID'
        if META_DATA_be_plannedWKA_getCoords == False and META_DATA_be_plannedWKA_getWeatherID == False:
            try:
                openfilename = 'Datenbank\ConnectwithID\Erzeugung/WindparksSH_geplanterAusbau_UTM_WeatherID_2019_2020.csv'
                print(openfilename)
                plannedWKA_areas = pd.read_csv(openfilename, delimiter=';', encoding='utf-8', decimal=',', na_values=0)
                plannedWKA_areas = plannedWKA_areas.fillna(0)
            except:
                print('falsches Format: ', openfilename)
                META_DATA_be_plannedWKA_getCoords == True
        'Area with coords but without weather ID'
        if META_DATA_be_plannedWKA_getCoords == False and META_DATA_be_plannedWKA_getWeatherID == True:
            try:
                openfilename = 'Datenbank\ConnectwithID\Erzeugung/WindparksSH_WetterID_2019_UTM'
                print(openfilename)
                plannedWKA_areas = pd.read_csv(openfilename, delimiter=';', encoding='utf-8', decimal=',', na_values=0)
                plannedWKA_areas = plannedWKA_areas.fillna(0)
            except:
                print('falsches Format: ', openfilename)
                META_DATA_be_plannedWKA_getCoords == True
                META_DATA_be_plannedWKA_getWeatherID = True
        'Area without coords and weather ID'
        if META_DATA_be_plannedWKA_getCoords == True and META_DATA_be_plannedWKA_getWeatherID == True:
            try:
                openfilename = 'Datenbank\ConnectwithID\Erzeugung/WindparksSH_geplanterAusbau.csv'
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
    print(temp_WeatherID.printWetterStation())
    "Öffnen der verschiedenen Speicher"
    if META_speichervorAusbau == True:
        listStorage = []
        storage = lgk.StorageModell('PumpspeicherKraftwerk', 'Geesthacht', 600000, META_startcapacity * 600000, 0.8, 120000,
                                0.0, 0.08)
        listStorage.append(storage)
        print('Storage is allocated', listStorage[-1].modell)

    '----------------------------------------------------------------------------------------------------------------------'
    '''Funktionen welche nur einmal Aufgerufen werden. Diese dienen nur zur Datenvorbereitung. 
        Sie haben nichts mit der Datenanlyse zu tun. Die Analyse finden gesondert statt.'''
    'Verbrauch HH und SH'
    if META_DATA_verbrauch_komuliert == True:
        print('verbrauchGesamt reload will be regenerated and reloaded')
        verbrauch_HH_SH = lgk.verbrauchGesamt(META_year)
    '-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -'
    'expansion area Vor and Pot'
    if META_wind == True:
        'Ausbauflaechen get Coords and get Weather ID'
        if META_DATA_plannedAreas_potVor_getCoords == True:
            print('plannedAreasgetCoords will be regenerated and reloaded')
            expansion_area_wind_vorpot = dataprep.plannendAreas_getCoords(expansion_area_wind_vorpot, export=True)
            expansion_area_wind_vorpot = dataprep.plannedAreas_getWeather(expansion_area_wind_vorpot, windWeatherStation,
                                                                          export=True)
        'Ausbauflaechen with Coords get Weather ID'
        if META_DATA_plannedAreas_potVor_getWeather == True:
            print('plannedAreas_getWeather will be regenerated and reloaded')
            expansion_area_wind_vorpot = dataprep.plannedAreas_getWeather(expansion_area_wind_vorpot, windWeatherStation,
                                                                          export=True)

    'be plannend area without Coords and without weather ID'
    if META_geplanterAusbau ==True:
        if META_DATA_be_plannedWKA_getCoords == True and META_DATA_be_plannedWKA_getWeatherID == True:
            print('plannedAreasgetCoords will be regenerated and reloaded')
            temp_exportname = 'Datenbank\ConnectwithID\Erzeugung/WindparksSH_geplanterAusbau_UTM_WeatherID_2019_2020.csv'
            plannedWKA_areas = db.utm_to_gk(META_year, temp_exportname, plannedWKA_areas)
            plannedWKA_areas = dataprep.plannedWKA_toUTM_and_connectWeahterID(windWeatherStation, plannedWKA_areas)
            META_DATA_generate_windenergy_plannendareas = True
        'be plannend area with Coords but without weather ID'
        if META_DATA_be_plannedWKA_getWeatherID == True and META_DATA_be_plannedWKA_getCoords == False:
            plannedWKA_areas = dataprep.plannedWKA_toUTM_and_connectWeahterID(windWeatherStation, plannedWKA_areas)
            META_DATA_generate_windenergy_plannendareas = True
        'be plannend area with Coords but without weather ID'
        if META_DATA_generate_windenergy_plannendareas == True:
            be_planned_wka_power = lgk.erzeugung_WKA_areawith_weatherID(META_year, windWeatherData, plannedWKA_areas,
                                                                        dictWKAModell,
                                                                        dictWeatherID, export=True)
            'Summe der einzelnen WKA Anlagen'
            temp_exportname = 'Datenbank\Erzeugung/Erz_komuliert_geplanterAusbau_' + str(META_year) + '_Wind.csv'
            be_planned_wka_power = lgk.erzeugungPerStunde_singleFrame(META_year, be_planned_wka_power, temp_exportname,
                                                                      export=True)
    'ERZEUGUNG NEU BERECHNEN'

    if META_DATA_pv_power == True and META_PV == True:
        # STATIONEN VORHER NOCH GEPRÜFT WERDEN
        lgk.erzeugungsdaten_ee_anlagen(META_year, 'PV', 'HH')
        lgk.erzeugungsdaten_ee_anlagen(META_year, 'PV', 'SH')
        PV_Gesamt = lgk.erzeugungPerStunde(META_year, 'PV')
    if META_DATA_wind_power == True and META_wind == True:
        # STATIONEN VORHER NOCH ÜBERPRÜFEN
        lgk.erzeugungsdaten_ee_anlagen(META_year, 'PV', 'HH')
        lgk.erzeugungsdaten_ee_anlagen(META_year, 'PV', 'SH')
        Wind_Gesamt = lgk.erzeugungPerStunde(META_year, 'Wind')



    '----------------------------------------------------------------------------------------------------------------------'
    if META_DATA_DBWKAreload == False:
        try:
            openfilename = 'Datenbank\WEAModell/DB_WKA_' + str(META_year) + '_' +  str(META_DATA_DB_min_hight)+ '.csv'
            print(openfilename)
            DB_WKA = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
        except:
            print('falsches Format: ', openfilename)
            print('Datenbank konnte nicht geöffnet werden')
            print('Datenbank wird automatisch erzeugt')
            META_DATA_DBWKAreload = True
    'DatenBank WKA'
    if META_DATA_DBWKAreload == True:
        print('DBWKA reload will be regenerated and reloaded')
        DB_WKA = lgk.DB_WKA(META_year, dictWKAModell, dictWeatherID, windWeatherData, META_DATA_DB_min_hight, export=True)

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
    exportFolder = 'REE_AnalyseCompleted/REE_AnalyseJahr_' + str(META_year) + '_' + str(uhrzeit) + '/'
    path = Path(exportFolder)
    path.mkdir(parents=True, exist_ok=True)
    '----------------------------------------------------------------------------------------------------------------------'
    'Muss noch überarbeitet werden'
    standortliste_123 = []
    list_value = []
    standort_main = 0
    anzahl_2 = []
    leistung_Gesamt = []
    name_2 = []
    '----------------------------------------------------------------------------------------------------------------------'
    '--------------------------------------------!-!-!SIMULATIONSSTART!-!-!------------------------------------------------'
    '----------------------------------------------------------------------------------------------------------------------'

    "Erste Simulation ohne einen Ausbau durch die Software"
    "In Bearbeitung"
    if META_windanalyse == True:
        try:
            openfilename = 'Datenbank\Wetter\WindAnalyse/Windanlyse_' + str(META_year) + '.csv'
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
    del be_planned_wka_power['Datum']
    del PV_Gesamt['Datum']
    del erz_Bio['Datum']
    del DB_WKA['Datum']
    # EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung], axis=1, sort=False)

    temp_wind = Wind_Gesamt.copy()  # ->wird für die Darstellung der Daten benötigt

    EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio, be_planned_wka_power,
                               verbrauch_HH_SH, ausbau=False, export=True,
                               geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                               wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                               expansionBio=META_expansionBio, speicher=META_speichervorAusbau)

    SimulationEE_vorAusbau = EE_Analyse[0].copy()
    EE_Anteil = EE_Analyse[1]
    print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')

    '----------------------------------------------------------------------------------------------------------------------'
    "Überprüfung weleche Vor/Pot Flächen zur Verfügung stehen. "
    # Daten müssen nicht in den Export ORDNER!!!
    verbauteVor = lgk.connect_oldWKA_to_expansionArea(META_year, 'Vor', expansion_area_wind_vorpot, META_faktorAusbauFlDist,
                                                      export=False, geplanterAusbau=META_geplanterAusbau)

    '''verbautPot = lgk.stand_distance_analyse(META_year, 'Pot', ausbauStandorte_Coords, META_faktorAusbauFlDist,
                                            export=False, geplanterAusbau=META_geplanterAusbau)'''
    freieFlaeche = lgk.freie_ha_vor(META_year, exportFolder, expansion_area_wind_vorpot, verbauteVor, export=True)

    freieFlaeche['Modell_Vor'] = ['unebkannt/nicht vorhanden'] * len(freieFlaeche['ID'])
    freieFlaeche['Anzahl_Vor'] = [0] * len(freieFlaeche['ID'])
    freieFlaeche['Leistung_Vor'] = [0] * len(freieFlaeche['ID'])
    freieFlaeche['InvestKosten_Vor'] = [0] * len(freieFlaeche['ID'])
    freieFlaeche['BetriebsKosten_Vor'] = [0] * len(freieFlaeche['ID'])
    freieFlaeche['Modell_Pot'] = ['unebkannt/nicht vorhanden'] * len(freieFlaeche['ID'])
    freieFlaeche['Anzahl_Pot'] = [0] * len(freieFlaeche['ID'])
    freieFlaeche['Leistung_Pot'] = [0] * len(freieFlaeche['ID'])
    freieFlaeche['InvestKosten_Pot'] = [0] * len(freieFlaeche['ID'])
    freieFlaeche['BetriebsKosten_Pot'] = [0] * len(freieFlaeche['ID'])

    "Nun ist bekannt welche Potenzial Flächen und Welche Vorrangflächen frei Verfügbar sind."
    '______________________________________________________________________________________________________________________'
    "ProzentualerAusbau BIOMASSE/PV"
    expansionBio = 0
    expansionPV = 0
    if META_biomasse == True:
        expansionBio = lgk.percentage_expansion(SimulationEE_vorAusbau['Erz_Biomasse_Gesamt'], META_expansionBio)
    if META_PV == True:
        expansionPV = lgk.percentage_expansion(SimulationEE_vorAusbau['Erzeugung_PV'], META_expansionPV)
    if META_wind == True:
        expansionWind = [1] * len(expansionPV)
    '______________________________________________________________________________________________________________________'
    "!!!Ausbau WIND STARTET!!!"
    temp_ausbau = True
    temp_ausgebauteAnlagen = ['test'] * len(expansionPV)
    expansionWind = [1] * len(expansionPV)
    tempausbauTrue = True

    if META_wind == True and META_VorFl == True and EE_Anteil < META_EE_Anteil:
        temp_ausgebauteAnlagen = ['test'] * len(expansionPV)
        temp_DB_WKA = DB_WKA.copy()
        for i in range(len(dictWeatherID)):
            print('Start: ', i)
            start = time.process_time()

            if i == 0:
                temp_wind = Wind_Gesamt.copy()
                EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                           be_planned_wka_power, verbrauch_HH_SH,
                                           expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                           geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                           wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                           expansionBio=META_expansionBio, speicher=META_speichervorAusbau)

                EE_Anteil = EE_Analyse[1]
                print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                SimulationEE_nachAusbau = EE_Analyse[0].copy()

            elif i > 0 and tempausbauTrue == True:
                temp_wind = Wind_Gesamt.copy()
                EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                           be_planned_wka_power, verbrauch_HH_SH,
                                           expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                           geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                           wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                           expansionBio=META_expansionBio, speicher=META_speichervorAusbau)

                EE_Anteil = EE_Analyse[1]
                print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                SimulationEE_nachAusbau = EE_Analyse[0].copy()

            if EE_Anteil >= META_EE_Anteil:
                print('FERTIG EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                break

            if tempausbauTrue == True:
                if META_speichervorAusbau == False:
                    temp_Diff_EE = SimulationEE_nachAusbau['Diff_EE_zu_Verb'].copy()
                else:
                    temp_Diff_E = SimulationEE_nachAusbau['Diff_EE_zu_Verb_nach_Speicher'].copy()
                    print(type(temp_Diff_E))
                    temp_Diff_EE = temp_Diff_E.tolist()
                    # print(temp_Diff_EE)
                EE_Simulation_negativGraph = lgk.negativ_Verlauf(temp_Diff_EE, speicherVerlauf=META_negativ_Graph_methode)
                deepestPoints = lgk.deepest_point_negativGraph(EE_Simulation_negativGraph, 20)

            WKAnameforexpansion = lgk.standort_and_WKA_choice(EE_Simulation_negativGraph, temp_DB_WKA, deepestPoints[1],
                                                              freieFlaeche['Wetter-ID_Vor'].tolist(),
                                                              temp_ausgebauteAnlagen,
                                                              dictWKAModell, spiecherMethodik=META_negativ_Graph_methode)
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
            'Muss noch überprüft werden'
            # max_Anzahl = lgk.maxAnzahl_WKA(deepestPoints[0], deepestPoints[1], DB_WKA, WKAnameforexpansion,
            # META_ausbaubegrenzungsfaktor)
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
            list_value.append(WKAnameforexpansion)
            try:
                temp_name = WKAnameforexpansion.split('_')
                temp_ID = temp_name[0]
                temp_Modell = temp_name[1]
                temp_Modell_hight = temp_name[2]
            except:
                print(temp_name)
                continue
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
            # print(Windlastprofil)
            # lgk.Windlastprofil(2020)
            temp_ausgebauteAnlagen[i] = temp_name[0]
            standort = lgk.Ausbau_WKA(temp_Modell + '_' + temp_Modell_hight, temp_ID, dictWKAModell, freieFlaeche,
                                      windWeatherData, 'Vor')
            # print(sum(standort[0]))
            # print(len(standort[0]))
            # print(type(standort[0]))
            if sum(standort[0]) == 0:
                print('Kein Ausbau mit der Anlage')
                tempausbauTrue = False
                continue
            else:
                tempausbauTrue = True

            for index, i in enumerate(expansionWind):
                expansionWind[index] = i + standort[0][index]
            # print(sum(expansionWind))
            # print(len(expansionWind))
            # print(type(expansionWind))
            name_2.append(WKAnameforexpansion)
            anzahl_2.append(standort[2])
            leistung_Gesamt.append(standort[3])
            standortliste_123.append(standort[4])
            finished_filename = exportFolder + 'AusgebauteFlaechen_' + str(META_year) + '.csv'
            freieFlaeche.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')
            end = time.process_time()
            print('VORRANGGEBIET:  End: ', i, 'Zeit: ', end - start, 'Name', WKAnameforexpansion,
                  'Anzahl Neu: ', standort[2], '/ Total: ', sum(anzahl_2))
            print('Leistung insgesamt zugebaut in MW: ', sum(leistung_Gesamt) / 1000, 'Leistung Neu:  ', standort[3],
                  'Freie Fläche: ', sum(freieFlaeche['nettoFreieFlaeche_Vor']))

    if META_wind == True and META_PotFl == True and EE_Anteil < META_EE_Anteil:
        temp_ausgebauteAnlagen = ['test'] * len(expansionPV)
        temp_DB_WKA = DB_WKA.copy()
        for i in range(len(dictWeatherID)):
            print('Start: ', i)
            start = time.process_time()

            if i == 0:
                temp_wind = Wind_Gesamt.copy()
                EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                           be_planned_wka_power,
                                           verbrauch_HH_SH,
                                           expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                           geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                           wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                           expansionBio=META_expansionBio, speicher=META_speichervorAusbau)

                EE_Anteil = EE_Analyse[1]
                print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                SimulationEE_nachAusbau = EE_Analyse[0].copy()

            elif i > 0 and tempausbauTrue == True:
                temp_wind = Wind_Gesamt.copy()
                EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, Wind_Gesamt, PV_Gesamt, erz_Bio,
                                           be_planned_wka_power,
                                           verbrauch_HH_SH,
                                           expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                           geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                           wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                           expansionBio=META_expansionBio, speicher=META_speichervorAusbau)

                EE_Anteil = EE_Analyse[1]
                print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                SimulationEE_nachAusbau = EE_Analyse[0].copy()

            if EE_Anteil >= META_EE_Anteil:
                print('FERTIG EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
                break

            if tempausbauTrue == True:
                if META_speichervorAusbau == False:
                    temp_Diff_EE = SimulationEE_nachAusbau['Diff_EE_zu_Verb'].copy()
                else:
                    temp_Diff_EE = SimulationEE_nachAusbau['Diff_EE_zu_Verb_nach_Speicher'].copy()

                EE_Simulation_negativGraph = lgk.negativ_Verlauf(temp_Diff_EE, speicherVerlauf=META_negativ_Graph_methode)
                deepestPoints = lgk.deepest_point_negativGraph(EE_Simulation_negativGraph, 20)

            WKAnameforexpansion = lgk.standort_and_WKA_choice(EE_Simulation_negativGraph, temp_DB_WKA, deepestPoints[1],
                                                              freieFlaeche['Wetter-ID_Pot'].tolist(),
                                                              temp_ausgebauteAnlagen,
                                                              dictWKAModell, spiecherMethodik=META_negativ_Graph_methode)
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
            'Muss noch überprüft werden'
            # max_Anzahl = lgk.maxAnzahl_WKA(deepestPoints[0], deepestPoints[1], DB_WKA, WKAnameforexpansion,
            # META_ausbaubegrenzungsfaktor)
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
            list_value.append(WKAnameforexpansion)
            try:
                temp_name = WKAnameforexpansion.split('_')
                temp_ID = temp_name[0]
                temp_Modell = temp_name[1]
                temp_Modell_hight = temp_name[2]
            except:
                print(temp_name)
                continue
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
            # print(Windlastprofil)
            # lgk.Windlastprofil(2020)
            temp_ausgebauteAnlagen[i] = temp_name[0]
            standort = lgk.Ausbau_WKA(temp_Modell + '_' + temp_Modell_hight, temp_ID, dictWKAModell, freieFlaeche,
                                      windWeatherData, 'Pot')
            # print(sum(standort[0]))
            # print(len(standort[0]))
            # print(type(standort[0]))
            if sum(standort[0]) == 0:
                print('Kein Ausbau mit der Anlage')
                tempausbauTrue = False
                continue
            else:
                tempausbauTrue = True

            for index, i in enumerate(expansionWind):
                expansionWind[index] = i + standort[0][index]
            # print(sum(expansionWind))
            # print(len(expansionWind))
            # print(type(expansionWind))
            name_2.append(WKAnameforexpansion)
            anzahl_2.append(standort[2])
            leistung_Gesamt.append(standort[3])
            standortliste_123.append(standort[4])
            finished_filename = exportFolder + 'AusgebauteFlaechen_' + str(META_year) + '.csv'
            freieFlaeche.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')
            end = time.process_time()
            print('POTENTZIALGEBIET End: ', i, 'Zeit: ', end - start, 'Name', WKAnameforexpansion,
                  'Anzahl Neu: ', standort[2], '/ Total', sum(anzahl_2))
            print('Leistung insgesamt zugebaut in MW: ', sum(leistung_Gesamt) / 1000, 'Leistung Neu:  ', standort[3],
                  'Freie Fläche: ', sum(freieFlaeche['nettoFreieFlaeche_Pot']))

    temp_wind = Wind_Gesamt.copy()
    EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio, be_planned_wka_power,
                               verbrauch_HH_SH,
                               expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=True,
                               geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                               wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                               expansionBio=META_expansionBio, speicher=META_speichervorAusbau)

    SimulationEE_nachAusbau = EE_Analyse[0].copy()

    if META_speicherausbau == True:

        while (EE_Anteil < META_EE_Speicher):
            print('EE Anteil in Prozent: ', round(EE_Anteil * 100, 3), '%')
            print('EE MUSS in Prozent: ', round(META_EE_Speicher * 100, 3), '%')

            if META_speichervorAusbau == False:
                temp_Diff_EE = SimulationEE_nachAusbau['Diff_EE_zu_Verb'].tolist()
            else:
                temp_Diff_EE = SimulationEE_nachAusbau['Diff_EE_zu_Verb_nach_Speicher'].tolist()
            print('Storage Len: ', len(listStorage))

            lgk.expansion_storage(temp_Diff_EE, META_negativ_Graph_methode, listStorage, META_startcapacity,
                                  META_Laegerdorf, META_compressed_air, META_strorage_safty_compansion,
                                  META_max_compressed_air)
            print('Storage Len: ', len(listStorage))
            EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                       be_planned_wka_power, verbrauch_HH_SH,
                                       expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=True,
                                       geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                       wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                       expansionBio=META_expansionBio, speicher=META_speichervorAusbau)

            EE_Anteil = EE_Analyse[1]
            SimulationEE_nachAusbau = EE_Analyse[0].copy()
            print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 6), '%')
            temp_min = min(SimulationEE_nachAusbau['Diff_EE_zu_Verb_nach_Speicher'])
            print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 6), '%')
            temp_min = min(SimulationEE_nachAusbau['Speicher_voll_Prozent'])

            print('Tiefester Speicherstand in Prozent: ', round(temp_min * 100, 6), '%')

            META_Laegerdorf = False
            META_compressed_air = False

        # Speicher fehlt in analyseEE!

    print('- - - - - - - - - - - - - - - - - - - - - - - - - ')
    print('EE Anteil FERTIG in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
    print('- - - - - - - - - - - - - - - - - - - - - - - - - ')
