import pandas as pd

import database
import database as db
import geo
import geo as gpd
import internetDownload as itd
import sandbox
import dataPreparation as dataprep
import logik as lgk
import time

META_EE_Anteil = 0.75  # Muss Decimal angegeben werden
META_year = 2019
META_geplanterAusbau = True
META_Biomasse = True
META_expansionBio = 0.12  # in Prozent
META_Wind = True
META_PV= True
META_expansionPV = 0.12  # in Prozent
META_faktorAusbauFlDist = 1.0  # in Kilometer
META_VorFl = False
META_PotFl = False
temp_ausbau = False
META_ausbaubegrenzungsfaktor = 0.5
META_Speicherverlauf = False

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
    openfilename5 = 'Datenbank\ConnectwithID/AusbauStandorte_Coords_final.csv'
    print(openfilename5)
    ausbauStandorte_Coords = pd.read_csv(openfilename5, delimiter=';', decimal='.', encoding='utf-8')
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
    openfilename9 = 'Datenbank\Wetter\WindAnalyse/Windanlyse_' + str(META_year) + '.csv'
    print(openfilename9)
    windanlyse = pd.read_csv(openfilename9, delimiter=';', decimal=',', encoding='latin1')
    '-------------------------------------------------------------------------------------'
    openfilename10 = 'Datenbank\WEAModell/DB_WKA.csv'
    print(openfilename10)
    DB_WKA = pd.read_csv(openfilename10, delimiter=';', decimal=',', encoding='latin1')
    '-------------------------------------------------------------------------------------'
    openfilename11 = 'Datenbank\Erzeugung/Erz_komuliert_Biomasse_' + str(META_year) + '.csv'
    print(openfilename11)
    erz_Bio = pd.read_csv(openfilename11, delimiter=';', decimal=',', encoding='latin1')


except:
    print('falsches Format')

'----------------------------------------------------------------------------------------------------------------------'
"Öffnen der verschiedenen WEA Modelle."
"KEY = MODELL -> Modell Name"
temp_WKA = lgk.WEAmodellDictionary_Class()
dictWKAModell = temp_WKA.getdict()
#print(dictWKAModell)
print(dictWKAModell)
"Öffnen der verschiedenen Wetterstationen."
"KEY = ID -> NUMMER der Wettersation"
temp_WeatherID = lgk.WeatherStationDictionary_Class()
dictWeatherID = temp_WeatherID.getdict()

'----------------------------------------------------------------------------------------------------------------------'
'''Funktionen welche nur einmal Aufgerufen werden. Diese dienen nur zur Datenvorbereitung. 
    Sie haben nichts mit der Datenanlyse zu tun. Die Analyse finden gesondert statt.'''
'----------------------------------------------------------------------------------------------------------------------'
# lgk.DB_WKA(META_year, dictWKAModell, dictWeatherID, windWeatherData)


# dataprep.plannedAreas_toUTM_and_connectWeahterID('Wind', 'SH', windWeatherStation)
# dataprep.erzeugung_plannendAreas(META_year, plannedWKA)
# lgk.erzeugungPerStunde(META_year, 'Wind')
# temp_windlastprofil = lgk.windlastprofil(META_year)
# lgk.standortquality(META_year, windWeatherData, WEAModell)

'______________________________________________________________________________________________________________________'
"In Bearbeitung"
# db.utm_to_gk(2019, 'Wind', 'SH')
# db.utm_to_gk(2019, 'Wind', 'HH')
# db.utm_to_gk(2020, 'Wind', 'SH')
# db.utm_to_gk(2020, 'Wind', 'HH')
# lgk.windlastprofil(2019)
# lgk.windlastprofil(2019)
'______________________________________________________________________________________________________________________'
"KEY FACTORS zum Ausbau -> muss noch angepasst werden"
standortliste_123 = []
list_value = []
standort_main = 0
anzahl_2 = []
leistung_Gesamt = []
name_2 = []

'----------------------------------------------------------------------------------------------------------------------'
"Erste Simulation ohne einen Ausbau durch die Software"
# PV_Gesamt = lgk.erzeugungPerStunde(year, 'PV')
# Wind_Gesamt = lgk.erzeugungPerStunde(year, 'Wind')
del plannedErzeung['Datum']
del PV_Gesamt['Datum']
del erz_Bio['Datum']
del DB_WKA['Datum']
# EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung], axis=1, sort=False)
verbrauch_HH_SH = lgk.verbrauchGesamt(META_year)
temp_wind = Wind_Gesamt.copy()  # ->wird für die Darstellung der Daten benötigt
EE_Analyse = lgk.analyseEE(META_year, temp_wind,PV_Gesamt,erz_Bio,plannedErzeung, verbrauch_HH_SH, export=True,
                               geplanterAusbau=META_geplanterAusbau, Biomasse=META_Biomasse,
                               Wind=META_Wind, PV=META_PV)


SimulationEE_vorAusbau = EE_Analyse[0].copy()
EE_Anteil = EE_Analyse[1]
print(EE_Analyse[1])


'----------------------------------------------------------------------------------------------------------------------'
"Überprüfung weleche Vor/Pot Flächen zur Verfügung stehen. "
verbauteVor = lgk.stand_distance_analyse(META_year, 'Vor', ausbauStandorte_Coords, META_faktorAusbauFlDist,
                                         export=False, geplanterAusbau=META_geplanterAusbau)

verbautPot = lgk.stand_distance_analyse(META_year, 'Pot', ausbauStandorte_Coords, META_faktorAusbauFlDist,
                                        export=False, geplanterAusbau=META_geplanterAusbau)
freieFlaeche = lgk.freie_ha_vor(META_year, ausbauStandorte_Coords, verbauteVor, verbautPot)

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
if META_Biomasse == True:
    expansionBio = lgk.percentage_expansion(SimulationEE_vorAusbau['Erz_Biomasse_Gesamt'], META_expansionBio)
if META_PV == True:
    expansionPV = lgk.percentage_expansion(SimulationEE_vorAusbau['Erzeugung_PV'], META_expansionPV)
'______________________________________________________________________________________________________________________'
"Wird nicht mehr benötigt. Die Funktion hat die Anzahl von WKA je Standort berechnet. Funktion muss umgeschrieben werden"
# standort_mitfreierLeistung = lgk.freie_leistung_Vor(META_year, freieFlaeche)
'----------------------------------------------------------------------------------------------------------------------'
"!!!Ausbau WIND STARTET!!!"
temp_ausbau = True
temp_ausgebauteAnlagen = ['test'] * len(expansionPV)
expansionWind = [0] * len(expansionPV)
tempausbauTrue = True

for i in range(len(dictWeatherID)):
    print('Start: ', i)
    start = time.process_time()

    if i == 0:
        temp_wind = Wind_Gesamt.copy()
        EE_Analyse = lgk.analyseEE(META_year, Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung, verbrauch_HH_SH,
                                   expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                   geplanterAusbau=META_geplanterAusbau, Biomasse=META_Biomasse,
                                   Wind=META_Wind, PV=META_PV, expansionPV=META_expansionPV,
                                   expansionBio=META_expansionBio)

        EE_Anteil = EE_Analyse[1]
        print('EE Anteil in Prozent: ', round(EE_Analyse[1]*100,2), '%')
        SimulationEE_nachAusbau = EE_Analyse[0].copy()

    elif i > 0 and tempausbauTrue == True:
        temp_wind = Wind_Gesamt.copy()
        EE_Analyse = lgk.analyseEE(META_year, Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung, verbrauch_HH_SH,
                                   expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=False,
                                   geplanterAusbau=META_geplanterAusbau, Biomasse=META_Biomasse,
                                   Wind=META_Wind, PV=META_PV, expansionPV=META_expansionPV,
                                   expansionBio=META_expansionBio)

        EE_Anteil = EE_Analyse[1]
        print('EE Anteil in Prozent: ', round(EE_Analyse[1]*100,2), '%')
        SimulationEE_nachAusbau = EE_Analyse[0].copy()

    if EE_Anteil >= META_EE_Anteil:
        print(standortliste_123)
        print(EE_Anteil)
        break

    if tempausbauTrue == True:
        temp_Diff_EE = SimulationEE_vorAusbau['Diff_EE_zu_Verb'].copy()
        EE_Simulation_negativGraph = lgk.negativ_Verlauf(temp_Diff_EE, speicherVerlauf=META_Speicherverlauf)
        deepestPoints = lgk.deepest_point_negativGraph(EE_Simulation_negativGraph, 75)

    WKAnameforexpansion = lgk.standort_and_WKA_choice(EE_Simulation_negativGraph, DB_WKA, deepestPoints[1],
                                                      freieFlaeche['Wetter-ID_Vor'].tolist(), temp_ausgebauteAnlagen,
                                                      dictWKAModell, spiecherMethodik=META_Speicherverlauf)
    '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
    'Muss noch überprüft werden'
    #max_Anzahl = lgk.maxAnzahl_WKA(deepestPoints[0], deepestPoints[1], DB_WKA, WKAnameforexpansion,
                                   #META_ausbaubegrenzungsfaktor)
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
    name_2.append(standort[1])
    anzahl_2.append(standort[2])
    leistung_Gesamt.append(standort[3])
    standortliste_123.append(standort[4])
    finished_filename = 'AusgebauteFlaechen_' + str(META_year) + '.csv'
    freieFlaeche.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')
    end = time.process_time()
    print('End: ', i, 'Zeit: ', end - start, 'Name', standort[1], 'Anzahl: ', standort[2])
    print('Leistung insgesamt zugebaut in MW: ', sum(leistung_Gesamt) / 1000, 'Leistung Neu:  ',standort[3],
          'Freie Fläche: ', sum(freieFlaeche['nettoFreieFlaeche_Vor']))


temp_wind = Wind_Gesamt.copy()
EE_Analyse = lgk.analyseEE(META_year, Wind_Gesamt, PV_Gesamt, erz_Bio, plannedErzeung, verbrauch_HH_SH,
                                   expansionWind, expansionPV, expansionBio, ausbau=temp_ausbau, export=True,
                                   geplanterAusbau=META_geplanterAusbau, Biomasse=META_Biomasse,
                                   Wind=META_Wind, PV=META_PV, expansionPV=META_expansionPV,
                                   expansionBio=META_expansionBio)

EE_Anteil = EE_Analyse[1]
print(EE_Analyse[1])
SimulationEE_nachAusbau = EE_Analyse[0].copy()

print('Fertig')
print(standortliste_123)
print(list_value)
print('Fertg')
