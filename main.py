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

print('Start')
META_EE_Anteil = 0.75  # Muss Decimal angegeben werden
META_year = 2019
META_geplanterAusbau = True
META_biomasse = True
META_expansionBio = 0.02  # in Prozent
META_wind = True
META_PV = True
META_expansionPV = 0.02  # in Prozent
META_faktorAusbauFlDist = 1.0  # in Kilometer
META_VorFl = True  # True -> Ausbauflaeche wird genutzt
META_PotFl = True  # True -> Ausbauflaeche wird genutzt
META_repowering = False  # True -> Anlagen >10 Jahre oder <1500KW Leistung werden abgerissen und neu gebaut (2:1)
temp_ausbau = False
META_ausbaubegrenzungsfaktor = 0.5
META_speicherverlauf = False
META_windanalyse = False
'-----------------------------------------------------------'
'Speicher'
META_startcapacity = 0.0  # Angabe in Prozent wie voll die Speicher im Startpunkt sind
META_speichervorAusbau = True  # True -> vor Ausbau Analyse beachtet Speicher
META_speicherausbau = True  # True -> Speicher werden ausgebaut
META_Laegerdorf = True
META_compressed_air = True
'-----------------------------------------------------------'
'Datenbank'
META_DATA_Inputcsv = 'utf-8'  # wird für das einlesen der Daten verwendet
META_DATA_OUTPUTcsv = 'utf-8-sig'  # wird für das auslesen der Daten verwendet
META_DATA_DBWKAreload = False  # True wenn die DB der WKA Lastgänge erstellt werden soll
META_DATA_plannedAreas_getCoords = False  # True wenn die Ausbauflächen keine Standorte besitzen
#                                           -> Wetterstationen werden ebenfalls hinzugefügt
META_DATA_plannedAreas_getWeather = False  # True wenn die Ausbauflächen keine zugeordnete Wetterstation besitzen
META_DATA_plannedWKAPower = False  # True wenn die Erzeugung ausgerechnet werden muss

'---------------------------------------------------------------------------------------------------------'
'!!!WICHTIGE DATEN!!!' \
'ohne diese Daten kann keine Simulation gestartet werden'
try:
    openfilename = 'Datenbank\Wetter/StundeWindStationen_Coords.csv'
    print(openfilename)
    windWeatherStation = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
except:
    print('falsches Format: ', openfilename)
try:
    openfilename = 'Datenbank\Wetter/StundeSolarStationen_Coords.csv'
    print(openfilename)
    solarWeatherStation = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
except:
    print('falsches Format: ', openfilename)

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
try:
    openfilename = 'Datenbank\Erzeugung/Erz_komuliert_' + str(META_year) + '_PV.csv'
    print(openfilename)
    PV_Gesamt = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
except:
    print('falsches Format: ', openfilename)
try:
    openfilename = 'Datenbank\Erzeugung/Erz_komuliert_' + str(META_year) + '_Wind.csv'
    print(openfilename)
    Wind_Gesamt = pd.read_csv(openfilename, delimiter=';', encoding='utf-8')
except:
    print('falsches Format: ', openfilename)
try:
    openfilename = 'Datenbank\Erzeugung/Erz_komuliert_Biomasse_' + str(META_year) + '.csv'
    print(openfilename)
    erz_Bio = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
except:
    print('falsches Format: ', openfilename)
try:
    openfilename = 'Datenbank\Erzeugung/Erz_komuliert_geplanterAusbau_2019_Wind.csv'
    print(openfilename)
    plannedErzeung = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
except:
    print('falsches Format: ', openfilename)

'---------------------------------------------------------------------------------------------------------'
'ALLGEMEIN AUSBAUFLÄCHEN'

'AusbauFlächen -> freie Pot und Vor Flächen, je nach Entscheidung werden die Daten bearbeitet'
if META_DATA_plannedAreas_getCoords == True:
    try:
        openfilename = 'Datenbank\Ausbauflaechen\AusbauStandorte_gesamt_SH/AlleStandorte.csv'
        print(openfilename)
        ausbauFlaechen = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)
if META_DATA_plannedAreas_getWeather == True and META_DATA_plannedAreas_getCoords == False:
    try:
        openfilename = 'Datenbank\ConnectwithID/AusbauStandorte_Coords.csv'
        print(openfilename)
        ausbauFlaechen = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)
if META_DATA_plannedAreas_getWeather == False and META_DATA_plannedAreas_getCoords == False:
    try:
        openfilename = 'Datenbank\ConnectwithID/AusbauStandorte_Coords_weatherID.csv'
        print(openfilename)
        ausbauFlaechen = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)

'Ausbau der bereits geplanten WKA Anlagen'
if META_DATA_plannedWKAPower == False:
    try:
        openfilename = 'Datenbank\ConnectwithID\Erzeugung/WindparksSH_geplanterAusbau_UTM_WeatherID_2019_2020.csv'
        print(openfilename)
        plannedWKA = pd.read_csv(openfilename, delimiter=';', encoding='utf-8', decimal=',', na_values=0)
        plannedWKA = plannedWKA.fillna(0)
    except:
        print('falsches Format: ', openfilename)

'---------------------------------------------------------------------------------------------------------'
'WKA MODELLE'

try:
    openfilename = 'Datenbank\WEAModell/WEAModell.csv'
    print(openfilename)
    WEAModell = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='latin1')
except:
    print('falsches Format: ', openfilename)

if META_DATA_DBWKAreload == False:
    try:
        openfilename = 'Datenbank\WEAModell/DB_WKA.csv'
        print(openfilename)
        DB_WKA = pd.read_csv(openfilename, delimiter=';', decimal=',', encoding='utf-8')
    except:
        print('falsches Format: ', openfilename)
        print('Datenbank konnte nicht geöffnet werden')
        print('Datenbank wird automatisch erzeugt')
        META_DATA_DBWKAreload = True

'----------------------------------------------------------------------------------------------------------------------'
"Öffnen der verschiedenen WEA Modelle."
"KEY = MODELL -> Modell Name"
temp_WKA = lgk.wea_modell_dictionary_class(WEAModell, useImport=False)
dictWKAModell = temp_WKA.getdict()
# temp_WKA.printWKAModelle()
"Öffnen der verschiedenen Wetterstationen."
"KEY = ID -> NUMMER der Wettersation"
temp_WeatherID = lgk.weather_station_dictionary_class(windWeatherStation, useImport=False)
dictWeatherID = temp_WeatherID.getdict()
# temp_WeatherID.printWetterStation()
# print(dictWeatherID)
"Öffnen der verschiedenen Speicher"
listStorage = []
storage = lgk.StorageModell('PumpspeicherKraftwerk', 'Geesthacht', 600000, META_startcapacity * 600000, 0.8, 120000,
                            0.0, 0.08)
listStorage.append(storage)
print(listStorage[-1].modell)

'----------------------------------------------------------------------------------------------------------------------'
'''Funktionen welche nur einmal Aufgerufen werden. Diese dienen nur zur Datenvorbereitung. 
    Sie haben nichts mit der Datenanlyse zu tun. Die Analyse finden gesondert statt.'''

'DatenBank WKA'
if META_DATA_DBWKAreload == True:
    print('DBWKAreload will be regenerated and reloaded')
    WEAModell = lgk.DB_WKA(META_year, dictWKAModell, dictWeatherID, windWeatherData, export=True)
# 'PumpspeicherKraftwerk', 'Geesthacht', 600000, startcapacity*600000, 0.8, 120000, 0.0, 0.08
# dataprep.plannedAreas_toUTM_and_connectWeahterID('Wind', 'SH', windWeatherStation)
# dataprep.erzeugung_plannendAreas(META_year, plannedWKA)
if META_DATA_plannedAreas_getCoords == True:
    print('plannedAreasgetCoords will be regenerated and reloaded')
    ausbauFlaechen = dataprep.plannendAreas_getCoords(ausbauFlaechen, export=True)
    ausbauFlaechen = dataprep.plannedAreas_getWeather(ausbauFlaechen, windWeatherStation, export=True)

if META_DATA_plannedAreas_getWeather == True:
    print('plannedAreas_getWeather will be regenerated and reloaded')
    ausbauFlaechen = dataprep.plannedAreas_getWeather(ausbauFlaechen, windWeatherStation, export=True)

# lgk.erzeugungPerStunde(META_year, 'Wind')
# temp_windlastprofil = lgk.windlastprofil(META_year)
# lgk.standortquality(META_year, windWeatherData, WEAModell)

'______________________________________________________________________________________________________________________'

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
del plannedErzeung['Datum']
del PV_Gesamt['Datum']
del erz_Bio['Datum']
del DB_WKA['Datum']
# EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung], axis=1, sort=False)
verbrauch_HH_SH = lgk.verbrauchGesamt(META_year)
temp_wind = Wind_Gesamt.copy()  # ->wird für die Darstellung der Daten benötigt

EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio, plannedErzeung,
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
verbauteVor = lgk.connect_oldWKA_to_expansionArea(META_year, 'Vor', ausbauFlaechen, META_faktorAusbauFlDist,
                                                  export=False, geplanterAusbau=META_geplanterAusbau)

'''verbautPot = lgk.stand_distance_analyse(META_year, 'Pot', ausbauStandorte_Coords, META_faktorAusbauFlDist,
                                        export=False, geplanterAusbau=META_geplanterAusbau)'''
freieFlaeche = lgk.freie_ha_vor(META_year, exportFolder, ausbauFlaechen, verbauteVor, export=True)

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
                                       plannedErzeung, verbrauch_HH_SH,
                                       expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                       geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                       wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                       expansionBio=META_expansionBio)

            EE_Anteil = EE_Analyse[1]
            print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
            SimulationEE_nachAusbau = EE_Analyse[0].copy()

        elif i > 0 and tempausbauTrue == True:
            temp_wind = Wind_Gesamt.copy()
            EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio,
                                       plannedErzeung, verbrauch_HH_SH,
                                       expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                       geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                       wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                       expansionBio=META_expansionBio)

            EE_Anteil = EE_Analyse[1]
            print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
            SimulationEE_nachAusbau = EE_Analyse[0].copy()

        if EE_Anteil >= META_EE_Anteil:
            print('FERTIG EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
            break

        if tempausbauTrue == True:
            temp_Diff_EE = SimulationEE_vorAusbau['Diff_EE_zu_Verb'].copy()
            EE_Simulation_negativGraph = lgk.negativ_Verlauf(temp_Diff_EE, speicherVerlauf=META_speicherverlauf)
            deepestPoints = lgk.deepest_point_negativGraph(EE_Simulation_negativGraph, 20)

        WKAnameforexpansion = lgk.standort_and_WKA_choice(EE_Simulation_negativGraph, temp_DB_WKA, deepestPoints[1],
                                                          freieFlaeche['Wetter-ID_Vor'].tolist(),
                                                          temp_ausgebauteAnlagen,
                                                          dictWKAModell, spiecherMethodik=META_speicherverlauf)
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
        print('VORRANGGEBIET:  End: ', i, 'Zeit: ', end - start, 'Name', WKAnameforexpansion, 'Anzahl: ', standort[2])
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
            EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, temp_wind, PV_Gesamt, erz_Bio, plannedErzeung,
                                       verbrauch_HH_SH,
                                       expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                       geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                       wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                       expansionBio=META_expansionBio)

            EE_Anteil = EE_Analyse[1]
            print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
            SimulationEE_nachAusbau = EE_Analyse[0].copy()

        elif i > 0 and tempausbauTrue == True:
            temp_wind = Wind_Gesamt.copy()
            EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung,
                                       verbrauch_HH_SH,
                                       expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                       geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                                       wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                                       expansionBio=META_expansionBio)

            EE_Anteil = EE_Analyse[1]
            print('EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
            SimulationEE_nachAusbau = EE_Analyse[0].copy()

        if EE_Anteil >= META_EE_Anteil:
            print('FERTIG EE Anteil in Prozent: ', round(EE_Analyse[1] * 100, 2), '%')
            break

        if tempausbauTrue == True:
            temp_Diff_EE = SimulationEE_vorAusbau['Diff_EE_zu_Verb'].copy()
            EE_Simulation_negativGraph = lgk.negativ_Verlauf(temp_Diff_EE, speicherVerlauf=META_speicherverlauf)
            deepestPoints = lgk.deepest_point_negativGraph(EE_Simulation_negativGraph, 20)

        WKAnameforexpansion = lgk.standort_and_WKA_choice(EE_Simulation_negativGraph, temp_DB_WKA, deepestPoints[1],
                                                          freieFlaeche['Wetter-ID_Pot'].tolist(),
                                                          temp_ausgebauteAnlagen,
                                                          dictWKAModell, spiecherMethodik=META_speicherverlauf)
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
        print('POTENTZIALGEBIET End: ', i, 'Zeit: ', end - start, 'Name', WKAnameforexpansion, 'Anzahl: ', standort[2])
        print('Leistung insgesamt zugebaut in MW: ', sum(leistung_Gesamt) / 1000, 'Leistung Neu:  ', standort[3],
              'Freie Fläche: ', sum(freieFlaeche['nettoFreieFlaeche_Pot']))

temp_wind = Wind_Gesamt.copy()
EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung,
                           verbrauch_HH_SH,
                           expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=True,
                           geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                           wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                           expansionBio=META_expansionBio)

if META_speicherausbau == True:

    listStorage.append(lgk.expansion_storage(temp_Diff_EE, META_speicherverlauf, listStorage, META_startcapacity,
                      META_Laegerdorf, META_compressed_air))
    print('Storage Len: ',len(listStorage))
    EE_Analyse = lgk.analyseEE(META_year, exportFolder, listStorage, Wind_Gesamt, PV_Gesamt, erz_Bio,
                               plannedErzeung, verbrauch_HH_SH,
                               expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=True,
                               geplanterAusbau=META_geplanterAusbau, biomes=META_biomasse,
                               wind=META_wind, PV=META_PV, expansionPV=META_expansionPV,
                               expansionBio=META_expansionBio)




EE_Anteil = EE_Analyse[1]
print(EE_Analyse[1])
print('Fertig')
print(standortliste_123)
print(list_value)
print('Fertg')
