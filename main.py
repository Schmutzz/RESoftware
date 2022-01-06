import pandas as pd
import database as db
import geo
import geo as gpd
import internetDownload as itd
import sandbox
import dataPreparation as dataprep
import logik as lgk
import time

META_year = 2019
META_geplanterAusbau = False
META_faktorAusbauFlDist = 1.1

try:
    openfilename1 = 'Datenbank\Wetter/StundeWindStationen_Coords.csv'
    print(openfilename1)
    windWeatherStation = pd.read_csv(openfilename1, delimiter=';', encoding='utf-8-sig')
    '-------------------------------------------------------------------------------------'
    openfilename2 = 'Datenbank\ConnectwithID\Erzeugung/WindparksSH_geplanterAusbau_UTM_WeatherID_2019_2020.csv'
    print(openfilename2)
    plannedWKA = pd.read_csv(openfilename2, delimiter=';', encoding='utf-8-sig', decimal=',', na_values=0)
    plannedWKA = plannedWKA.fillna(0)
    '-------------------------------------------------------------------------------------'
    openfilename3 = 'Datenbank\Erzeugung/Erz_komuliert_' + str(META_year) + '_PV.csv'
    print(openfilename3)
    PV_Gesamt = pd.read_csv(openfilename3, delimiter=';', decimal=',', encoding='utf-8-sig')
    '-------------------------------------------------------------------------------------'
    openfilename4 = 'Datenbank\Erzeugung/Erz_komuliert_' + str(META_year) + '_Wind.csv'
    print(openfilename4)
    Wind_Gesamt = pd.read_csv(openfilename4, delimiter=';', encoding='utf-8-sig')
    '-------------------------------------------------------------------------------------'
    openfilename5 = 'Datenbank\ConnectwithID/AlleStandorte_Coords_final.csv'
    print(openfilename5)
    alleStandorte_Coords = pd.read_csv(openfilename5, delimiter=';', decimal='.', encoding='utf-8')
    '-------------------------------------------------------------------------------------'
    openfilename6 = 'Datenbank\Wetter/Wind_Wetterdaten_' + str(META_year) + '.csv'
    print(openfilename6)
    windWeatherData = pd.read_csv(openfilename6, delimiter=';', decimal=',', header=0)
    '-------------------------------------------------------------------------------------'
    openfilename7 = 'Datenbank\Erzeugung/Erz_komuliert_geplanterAusbau_2019_Wind.csv'
    print(openfilename7)
    plannedErzeung = pd.read_csv(openfilename7, delimiter=';', decimal=',', encoding='utf-8')
    '-------------------------------------------------------------------------------------'
    openfilename8 = 'Datenbank\WEAModell/WEAModell.csv'
    print(openfilename8)
    WEAModell = pd.read_csv(openfilename8, delimiter=';', decimal=',', encoding='latin1')
    '-------------------------------------------------------------------------------------'
    openfilename8 = 'Datenbank\Wetter\WindAnalyse/Windanlyse_' + str(META_year) + '.csv'
    print(openfilename8)
    windanlyse = pd.read_csv(openfilename8, delimiter=';', decimal=',', encoding='latin1')


except:
    print('falsches Format')


'----------------------------------------------------------------------------------------------------------------------'
'''Funktionen welche nur einmal Aufgerufen werden. Diese dienen nur zur Datenvorbereitung. 
    Sie haben nichts mit der Datenanlyse zu tun. Die Analyse finden gesondert statt.'''
'----------------------------------------------------------------------------------------------------------------------'
print(windWeatherData)
# dataprep.plannedAreas_toUTM_and_connectWeahterID('Wind', 'SH', windWeatherStation)
# dataprep.erzeugung_plannendAreas(META_year, plannedWKA)
# lgk.erzeugungPerStunde(META_year, 'Wind')
#temp_windlastprofil = lgk.windlastprofil(META_year)
lgk.standortquality(META_year, windWeatherData, WEAModell)

'______________________________________________________________________________________________________________________'
"In Bearbeitung"
# db.utm_to_gk(2019, 'Wind', 'SH')
# db.utm_to_gk(2019, 'Wind', 'HH')
# db.utm_to_gk(2020, 'Wind', 'SH')
# db.utm_to_gk(2020, 'Wind', 'HH')
# lgk.windlastprofil(2019)
# lgk.windlastprofil(2019)
'______________________________________________________________________________________________________________________'
standortliste_123 = []
list_value = []
standort_main = 0
anzahl_2 = []
leistung_Gesamt = []
name_2 = []


def status_befor_expansion(year, export):
    # PV_Gesamt = lgk.erzeugungPerStunde(year, 'PV')
    # Wind_Gesamt = lgk.erzeugungPerStunde(year, 'Wind')
    del plannedErzeung['Datum']
    del PV_Gesamt['Datum']
    if META_geplanterAusbau == True:
        EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt, plannedErzeung], axis=1, sort=False)
    else:
        EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt], axis=1, sort=False)
    verbrauch_HH_SH = lgk.verbrauchGesamt(year)
    EE_Analyse = lgk.analyseEE(year, EE_Erz_Wind_Gesamt, verbrauch_HH_SH, export=export,
                               geplanterAusbau=META_geplanterAusbau)

    return EE_Analyse, verbrauch_HH_SH


'----------------------------------------------------------------------------------------------------------------------'

EE = status_befor_expansion(META_year, True)
verbrauch_HH_SH = EE[1]

verbauteVor = lgk.stand_distance_analyse(META_year, 'Vor', alleStandorte_Coords, META_faktorAusbauFlDist, export=False)
verbautPot = lgk.stand_distance_analyse(META_year, 'Pot', alleStandorte_Coords, META_faktorAusbauFlDist, export=False)
freieFlaeche = lgk.freie_ha_vor(META_year, alleStandorte_Coords, verbauteVor, verbautPot)

"Nun ist bekannt welche Potenzial Flächen und Welche Vorrangflächen frei Verfügbar sind."
'______________________________________________________________________________________________________________________'

standort_mitfreierLeistung = lgk.freie_leistung_Vor(META_year, freieFlaeche)

'----------------------------------------------------------------------------------------------------------------------'
for i in range(500):
    print('Start: ', i)
    start = time.process_time()

    if i == 0:

        EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt], axis=1, sort=False)
        EE_Analyse = lgk.analyseEE(META_year, EE_Erz_Wind_Gesamt, verbrauch_HH_SH, export=True)


    else:
        EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt], axis=1, sort=False)
        EE_Analyse = lgk.analyseEE(META_year, EE_Erz_Wind_Gesamt, verbrauch_HH_SH)

    value = lgk.ausbau(META_year, EE_Analyse, standort_mitfreierLeistung)

    if value >= 0:
        print(standortliste_123)
        print(value)

        break

    list_value.append(value)
    # print(Windlastprofil)
    # lgk.Windlastprofil(2020)

    standort = lgk.windenergie(standort_mitfreierLeistung, standort_main)
    Wind_Gesamt['Erzeugung_Wind'] += standort[0]
    standortliste_123.append(standort[5])
    anzahl_2.append(standort[3])
    leistung_Gesamt.append(standort[4])
    name_2.append(standort[1])
    standort_main = int(standort[2])
    end = time.process_time()
    print('End: ', i, 'Zeit: ', end - start, 'Leistung MW', sum(standort[0]) / 1000)

finished_filename = 'FERTIG.csv'
EE_Analyse.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')

print('Fertig')
print(standortliste_123)
print(list_value)
print('Fertg')
