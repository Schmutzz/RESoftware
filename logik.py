import time

import numpy
import pandas as pd
import numpy as np

from database import findoutFiles

"""Erzeugt ein DataFrame oder eine Liste mit fortlaufenden Datum+Uhrzeit"""
from database import dateList_dataFrame as DateList
from datetime import datetime
import geo

'---------------------------------------------------------------------------------------------------------'
'Modellparameter AUSBAUFLÄCHEN'


class StorageModell:

    def __init__(self, modell, location, max_capacity, current_capacity, efficiency, power, invest, operatingk):

        # CAPEX -> Investionskosten
        # OPEX -> Betriebskosten
        self.modell = modell
        self.location = location
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity
        self.efficiency = efficiency
        self.efficiency_input = round(np.sqrt(efficiency), 3)
        self.efficiency_output = round(np.sqrt(efficiency), 3)
        self.power = power
        self.invest = invest
        self.operatingk = operatingk
        self.__startcapacity = current_capacity

    def input_power(self, new_value):

        if self.current_capacity == self.max_capacity:
            return 0, 0
        # Ladeleistung wird positiv gesetzt
        new_value = abs(new_value)
        if new_value >= self.power:
            new_value = self.power

        temp_freie_capa = (self.max_capacity - self.current_capacity)

        if temp_freie_capa < (new_value * self.efficiency_input):
            new_value = (temp_freie_capa / self.efficiency_input)
            self.current_capacity += new_value * self.efficiency_input
            # Ladeleistung auf max Leistung begrenzt
        else:
            self.current_capacity += new_value * self.efficiency_input

        power_effective = new_value * self.efficiency_input
        power_loss = new_value - power_effective

        return power_effective, power_loss

    def output_power(self, newValue):
        # Entladeleistung wird positiv gesetzt
        newValue = abs(newValue)
        if self.current_capacity == 0:
            return 0, 0

        newValue = (newValue / self.efficiency_output) + 1
        if newValue >= self.power:
            newValue = self.power

        temp_freie_capa = self.current_capacity

        # Entladeleistung auf max Leistung begrenzt
        if temp_freie_capa >= newValue:
            self.current_capacity -= newValue
        else:
            newValue = temp_freie_capa
            self.current_capacity -= newValue
        # Effektive ladeleistung mit Wirkungsgrad
        power_effective = newValue * self.efficiency_output
        power_loss = newValue - power_effective

        return power_effective, power_loss

    def get_current_capacity(self):
        x = self.current_capacity
        return x

    def reset_current_capacity(self):
        self.current_capacity = self.__startcapacity


class WKAmodell:

    def __init__(self, modell, ein_ms, nenn_ms, abs_ms, nenn_kW, nabenhoehe, rotor, ausbauRelv, windklasse, invest,
                 betriebk):

        self.modellName = modell
        self.Ein_ms = ein_ms
        self.Nenn_ms = nenn_ms
        self.Abs_ms = abs_ms
        self.Nenn_kW = nenn_kW
        self.Nabenhoehe = nabenhoehe
        self.Rotor = rotor
        self.AusbauRelv = ausbauRelv
        self.Windklasse = windklasse
        self.Invest = invest
        self.Betriebk = betriebk
        self.Flaeche = self.getFlaeche()
        self.__dict = self.filldict()

    def filldict(self):
        temp_dict = {}
        for index, i in enumerate(self.modellName):
            key = i + '_' + str(self.Nabenhoehe[index])
            temp_dict[key] = {'Modell': i,
                              'Ein_ms': self.Ein_ms[index], 'Nenn_ms': self.Nenn_ms[index],
                              'Abs_ms': self.Abs_ms[index], 'Nenn_kW': self.Nenn_kW[index],
                              'Nabenhoehe': self.Nabenhoehe[index], 'Rotor': self.Rotor[index],
                              'AusbauRelv': self.AusbauRelv[index], 'Windklasse': self.Windklasse[index],
                              'Invest': self.Invest[index], 'Betriebk': self.Betriebk[index],
                              'Flaeche': self.Flaeche[index]}
            # print(temp_dict)

        return temp_dict

    def getFlaeche(self):
        x = []
        for i in self.Rotor:
            x.append(round(((15 * np.square(float(i))) / 10000), 2))

        return x

    def getAnzahlWKAmodell(self):
        return len(self.__dict)

    def getdict(self):
        return self.__dict

    def changedict_singel(self, key, type, value):

        self.__dict[key][type] = value

    def getWKAModell(self, key):

        return self.__dict[key]

    def printWKAModelle(self):
        for p_id, p_info in self.__dict.items():
            print("\n WKA ID:", p_id)
            for key in p_info:
                print(key + ':', p_info[key])


class WetterStation:

    def __init__(self, ID, NameORT, state, Messheight, geoBreite, geoLaenge, coords):

        self.NameORT = NameORT
        self.ID = ID
        self.Messheight = Messheight
        self.state = state
        self.geoBreite = geoBreite
        self.geoLaenge = geoLaenge
        self.windklasse = 4
        self.coords = coords
        self.__dict = self.filldict()

    def filldict(self):
        temp_dict = {}
        for index, i in enumerate(self.ID):
            temp_dict[i] = {'NameORT': self.NameORT[index], 'ID': self.ID[index],
                            'Messhight': self.Messheight[index], 'state': self.state[index],
                            'geoBreite': self.geoBreite[index], 'geoLaenge': self.geoLaenge[index],
                            'windklasse': self.windklasse, 'Coords': self.coords[index]}

        return temp_dict

    def getAnzahlWKAmodell(self):
        return len(self.__dict)

    def getdict(self):
        return self.__dict

    def changedict_singel(self, key, type, value):

        self.__dict[key][type] = value

    def getWetterStation(self, key):

        return self.__dict[key]

    def printWetterStation(self):
        for p_id, p_info in self.__dict.items():
            print("\n ID ID:", p_id)
            for key in p_info:
                print(key + ':', p_info[key])


def wea_modell_dictionary_class(WKA_csvFrame, useImport=True):
    if useImport == True:
        try:
            headerlistModell = ['Modell', 'LEISTUNG', 'NABENHOEHE', 'Einschaltgeschwindigkeit m/s',
                                'Nenngeschwindigkeit m/s', 'Abschaltgeschwindigkeit m/s', 'Rotordurchmesser',
                                'Ausbaurelevant',
                                'IEC-WindKlasse', 'Investitionskosten', 'Betriebskosten in Euro/a']

            openfilename3 = 'Datenbank/WEAModell/WEAModell.csv'
            print(openfilename3)
            WKA_csvFrame = pd.read_csv(openfilename3, usecols=headerlistModell, delimiter=';', decimal=',', header=0,
                                       encoding='utf-8')
            # print(df)
        except ValueError:
            print("falsches Format")

    # Erstellen des Dictionary

    for i in range(len(WKA_csvFrame['Modell'])):
        if isinstance(WKA_csvFrame['Modell'][i], str) == False:
            WKA_csvFrame['Modell'][i] = "unbekannt"
        if isinstance(WKA_csvFrame['Einschaltgeschwindigkeit m/s'][i], float) == False and isinstance(
                WKA_csvFrame['Einschaltgeschwindigkeit m/s'][i], int) == False:
            # print(isinstance(df['Einschaltgeschwindigkeit m/s'][i], float))
            # print(df['Einschaltgeschwindigkeit m/s'][i])
            # print(type(df['Einschaltgeschwindigkeit m/s'][i]))
            WKA_csvFrame['Einschaltgeschwindigkeit m/s'][i] = 3
        if isinstance(WKA_csvFrame['Nenngeschwindigkeit m/s'][i], float) == False and isinstance(
                WKA_csvFrame['Nenngeschwindigkeit m/s'][i],
                int) == False:
            WKA_csvFrame['Nenngeschwindigkeit m/s'][i] = 13
        if isinstance(WKA_csvFrame['Abschaltgeschwindigkeit m/s'][i], float) == False and isinstance(
                WKA_csvFrame['Abschaltgeschwindigkeit m/s'][i], int) == False:
            WKA_csvFrame['Abschaltgeschwindigkeit m/s'][i] = 25
        if isinstance(WKA_csvFrame['LEISTUNG'][i], float) == False and isinstance(WKA_csvFrame['LEISTUNG'][i],
                                                                                  int) == False and \
                isinstance(WKA_csvFrame['LEISTUNG'][i], np.int64) == False:
            WKA_csvFrame['LEISTUNG'][i] = 1500

    '------------------------------------------------------------'
    "TECHNISCHE DATEN UM EIN WKA"
    modell = WKA_csvFrame['Modell'].tolist()
    ein_ms = WKA_csvFrame['Einschaltgeschwindigkeit m/s'].tolist()
    nenn_ms = WKA_csvFrame['Nenngeschwindigkeit m/s'].tolist()
    abs_ms = WKA_csvFrame['Abschaltgeschwindigkeit m/s'].tolist()
    leistung = WKA_csvFrame['LEISTUNG'].tolist()
    nabenhoehe = WKA_csvFrame['NABENHOEHE'].tolist()
    rotor = WKA_csvFrame['Rotordurchmesser'].tolist()
    ausbauRelev = WKA_csvFrame['Ausbaurelevant'].tolist()
    windKlasse = WKA_csvFrame['IEC-WindKlasse'].tolist()
    '------------------------------------------------------------'
    "KOSTEN RUND UM EIN WKA"
    invest = WKA_csvFrame['Investitionskosten'].tolist()
    betrieb = WKA_csvFrame['Betriebskosten in Euro/a'].tolist()
    '------------------------------------------------------------'

    peter = WKAmodell(modell, ein_ms, nenn_ms, abs_ms, leistung, nabenhoehe, rotor, ausbauRelev, windKlasse, invest,
                      betrieb)
    # WKAmodell(k, Ein_ms[index], Nenn_ms[index], Abs_ms[index], P_kw[index])

    return peter


def weather_station_dictionary_class(weatherID_csvFrame, useImport=True):
    if useImport == True:
        try:
            headerlistModell = ['Stations_id', 'Messhoehe', 'Stationsname', 'Bundesland', 'geoBreite', 'geoLaenge',
                                'Coords']
            openfilename3 = 'Import/Wetterstationen/StundeWindStationen.csv'
            print(openfilename3)
            weatherID_csvFrame = pd.read_csv(openfilename3, usecols=headerlistModell, delimiter=';', decimal=',',
                                             header=0,
                                             encoding='utf-8')
            # print(df)
        except ValueError:
            print("falsches Format")

    # Erstellen des Dictionary

    for i in range(len(weatherID_csvFrame['Stations_id'])):
        if isinstance(weatherID_csvFrame['Messhoehe'][i], float) == False and \
                isinstance(weatherID_csvFrame['Messhoehe'][i], int) == False:
            try:
                weatherID_csvFrame['Messhoehe'][i] = int(weatherID_csvFrame['Messhoehe'][i])
            except:
                weatherID_csvFrame['Messhoehe'][i] = 9.8
        if isinstance(weatherID_csvFrame['Stations_id'][i], float) == False and \
                isinstance(weatherID_csvFrame['Stations_id'][i], numpy.int64) == False:
            # print(type(df['Stations_id'][i]))
            # print(isinstance(df['Stations_id'][i], float))
            # print(isinstance(df['Stations_id'][i], int))
            weatherID_csvFrame['Stations_id'][i] = '0'
        if isinstance(weatherID_csvFrame['Stationsname'][i], str) == False:
            weatherID_csvFrame['Stationsname'][i] = "unbekannt"
        if isinstance(weatherID_csvFrame['Bundesland'][i], str) == False:
            weatherID_csvFrame['Bundesland'][i] = "unbekannt"

    stations_id = weatherID_csvFrame['Stations_id'].tolist()
    messhoehe = weatherID_csvFrame['Messhoehe'].tolist()
    stationsname = weatherID_csvFrame['Stationsname'].tolist()
    bundesland = weatherID_csvFrame['Bundesland'].tolist()
    geoBreite = weatherID_csvFrame['geoBreite'].tolist()
    geoLaenge = weatherID_csvFrame['geoLaenge'].tolist()
    coords = weatherID_csvFrame['Coords'].tolist()

    # print(Stations_id, Stationsname, Bundesland, Messhoehe)

    peter = WetterStation(stations_id, stationsname, bundesland, messhoehe, geoBreite, geoLaenge, coords)
    # WKAmodell(k, Ein_ms[index], Nenn_ms[index], Abs_ms[index], P_kw[index])

    return peter


'---------------------------------------------------------------------------------------------------------'
'Allgemeine Formeln'


def wind_hochrechnung(wind, naben_height, mess_height):
    hellmann_konst = 0.25
    delte_height = float(naben_height) / float(mess_height)
    wind = wind * (delte_height ** hellmann_konst)
    return wind


def IEC_windklasse(sum_temp_wetter, len_temp_wetter):

    average_wind = sum_temp_wetter / len_temp_wetter

    if average_wind >= 10:
        return 1
    elif average_wind >= 8.5:
        return 2
    elif average_wind >= 7.5:
        return 3
    elif average_wind >= 6.5:
        return 4
    elif average_wind < 6.5:
        return 5
    else:
        print('---------------------------')
        print('Ganz komischer Fehler')
        print('---------------------------')
        return 7



def FORMEL_WKA_Leistung(nenn_ms, ein_ms, leistung_s, moment_ms):
    a = 5

    vp_WP = ein_ms + ((nenn_ms) / 2) + 1
    k = np.log(a / (leistung_s - a)) / (leistung_s * vp_WP * (-1))

    temp_p = (a * leistung_s) / (a + (leistung_s - a) * np.exp(leistung_s * k * moment_ms * (-1)))

    return temp_p


def annualOutput_WKA(year, Ein_ms, Nenn_ms, Abs_ms, leistung_Gesamt, weatherData, nabenhohe, weatherID_hight,
                     windklasse_wka, META_first_wind_limit, META_sec_wind_limit, META_third_wind_limit,
                     META_first_power_limit, META_sec_power_limit, META_third_power_limit, use_wind_IEC = False,
                     eisman=False):

    temp_DatelistPerHoure = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', '60min')

    temp_wetter = wind_hochrechnung(weatherData, nabenhohe, weatherID_hight)
    temp_leistung = [0] * len(temp_DatelistPerHoure)
    temp_leistung_eisman = [0.01] * len(temp_DatelistPerHoure)

    if use_wind_IEC == True:
        temp_IEC_windklasse = IEC_windklasse(sum(temp_wetter), len(temp_wetter))
        if temp_IEC_windklasse < windklasse_wka:
            return temp_leistung

    for index, k in enumerate(temp_wetter):
        temp_leistung_for = 0

        # Fehler raus suchen
        if k < 0:
            temp_leistung_for = 0

        # unter Nennleistung
        elif k >= Ein_ms and k < Nenn_ms:
            x = FORMEL_WKA_Leistung(Nenn_ms, Ein_ms, leistung_Gesamt, k)
            temp_leistung_for = int(x)

        # ueber nennleistung
        elif k >= Nenn_ms and k < Abs_ms:
            temp_leistung_for = int(leistung_Gesamt)

        # außerhalb der Betriebsgeschwindigekeit
        elif k >= Abs_ms or k < Ein_ms:
            temp_leistung_for = 0

        else:
            print("Fehler Berechnung")
            print('Value: ', k)

        temp_leistung_eisman_value = 0

        if eisman == True:
            ref_temp_leistung_for = temp_leistung_for
            if k > META_first_wind_limit and k <= META_sec_wind_limit:
                temp_leistung_for = temp_leistung_for * META_first_power_limit
                temp_leistung_eisman_value = abs(ref_temp_leistung_for-temp_leistung_for)
            elif k > META_sec_wind_limit and k <= META_third_wind_limit:
                temp_leistung_for = temp_leistung_for * META_sec_power_limit
                temp_leistung_eisman_value = abs(ref_temp_leistung_for - temp_leistung_for)
            elif k > META_third_wind_limit:
                temp_leistung_for = temp_leistung_for * META_third_power_limit
                temp_leistung_eisman_value = abs(ref_temp_leistung_for - temp_leistung_for)

        temp_leistung[index] = temp_leistung_for
        temp_leistung_eisman[index] = temp_leistung_eisman_value

    return temp_leistung, temp_leistung_eisman

'---------------------------------------------------------------------------------------------------------'


def generation_wind_energy(year,dictModell,dictWeatherID, source, state, META_first_wind_limit = 0, META_sec_wind_limit= 0,
                           META_third_wind_limit= 0, META_first_power_limit= 0, META_sec_power_limit= 0,
                           META_third_power_limit= 0, eisman = False):

    exportFrame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', '60min')

    filelist = findoutFiles('Datenbank/ConnectwithID/Erzeugung')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(year) in match]
    matchfilelist4 = [match for match in matchfilelist3 if str('geplanterAusbau') not in match]
    print(matchfilelist3)

    try:
        openfilename2 = 'Datenbank/Wetter/' + source + '_Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)
        # print(wetterdaten)
    except ValueError:
        print("erzeugungsdaten_ee_anlagen Falsches Format")

    modellunbekannt = 0
    wetterIDunbekannt = 0
    DB_WKA_name = []
    DB_WKA_power = []
    DB_WKA_eisman = []
    if source == 'Wind':
        try:
            headerlistLokation = ['TYP', 'Modell', 'Wetter-ID', 'LEISTUNG', 'NABENHOEHE']
            openfilename1 = 'Datenbank/ConnectwithID/Erzeugung/' + matchfilelist4[0]
            print(openfilename1)

            lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal=',',
                                         header=0, encoding='utf-8')

            print('-------------------')
            print(len(lokationsdaten))
            print('-------------------')
            lengthLocation = lokationsdaten.__len__()
            lokationsdaten['TYP'] = lokationsdaten['TYP'].replace(np.nan, 'Typ_unbekannt')
            lokationsdaten['Modell'] = lokationsdaten['Modell'].replace(np.nan, 'Modell_unbekannt')
            lokationsdaten['Wetter-ID'] = lokationsdaten['Wetter-ID'].replace(np.nan, 3086)
            lokationsdaten['LEISTUNG'] = lokationsdaten['LEISTUNG'].replace(np.nan, 1000)
            lokationsdaten['NABENHOEHE'] = lokationsdaten['NABENHOEHE'].replace(np.nan, 50)
            print('-------------------')
            print(len(lokationsdaten))
            print('-------------------')
            # print(lokationsdaten)
        except ValueError:
            print("lokationsdaten falsches Format")
        '------------------------------------------------------------------------------------------------------'

        leistung_eisman = [0] * len(wetterdaten)

        for i in range(lengthLocation):
            temp_insertlist = False
            WKAunbekannt = False
            # print(str(lokationsdaten['Wetter-ID'][i]))

            matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                  str(lokationsdaten['Wetter-ID'][i]) in match]
            # print(matcheswetterdaten)
            if len(matcheswetterdaten) != 2:
                print('Fehler Wetterdaten nicht schlimm')
                print(lokationsdaten['Wetter-ID'][i])
                lokationsdaten['Wetter-ID'][i] = 3086
                matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                      str(lokationsdaten['Wetter-ID'][i]) in match]
                wetterIDunbekannt += 1
            temp_db_wka_name = 'Ezg_' + str(lokationsdaten['Modell'][i]) + '_' + str(
                lokationsdaten['NABENHOEHE'][i]) + '_' + str(lokationsdaten['Wetter-ID'][i])



            columnName = str(i) + '_Ezg_' + str(lokationsdaten['Modell'][i]) + '_' + str(
                lokationsdaten['NABENHOEHE'][i]) + '_' + str(lokationsdaten['Wetter-ID'][i])

            temp_modell = str(lokationsdaten['Modell'][i]) + '_' + str(lokationsdaten['NABENHOEHE'][i])

            if temp_db_wka_name in DB_WKA_name:
                # gibt index von WKA
                jindex = DB_WKA_name.index(temp_db_wka_name)
                # befüllt die Frames
                exportFrame[columnName] = DB_WKA_power[jindex]
                for i in range(len(leistung_eisman)):
                    leistung_eisman[i] = leistung_eisman[i] + DB_WKA_eisman[jindex][i]

                # print('Über DB gelöst: ',columnName, 'Index: ', jindex)
                continue


            try:
                Ein_ms = dictModell[temp_modell]['Ein_ms']
            except:
                Ein_ms = 3
                # print("Modell unbekannt")
                WKAunbekannt = True
            try:
                Nenn_ms = dictModell[temp_modell]['Nenn_ms']
            except:
                Nenn_ms = 13
                # print("Modell unbekannt")
                WKAunbekannt = True
            try:
                Abs_ms = dictModell[temp_modell]['Abs_ms']
            except:
                Abs_ms = 25
                WKAunbekannt = True

            if WKAunbekannt == True:
                # print("Modell unbekannt")
                modellunbekannt += 1

            if isinstance(lokationsdaten['LEISTUNG'][i], float) == False and isinstance(
                    lokationsdaten['LEISTUNG'][i], numpy.int64) == False:
                lokationsdaten['LEISTUNG'][i] = 1000
                print('Fehler Leistungsdaten nicht schlimm')
                print(columnName)

            temp_weatherID = lokationsdaten['Wetter-ID'][i]

            if isinstance(dictWeatherID[temp_weatherID]['windklasse'], float) == False and isinstance(
                    dictWeatherID[temp_weatherID]['windklasse'], numpy.int64) == False and isinstance(
                    dictWeatherID[temp_weatherID]['windklasse'], int) == False:
                print(type(dictWeatherID[temp_weatherID]['windklasse']))
                dictWeatherID[temp_weatherID]['windklasse'] = 2
                print('Fehler windklasse nicht schlimm')

            if isinstance(lokationsdaten['NABENHOEHE'][i], float) == False and isinstance(
                    lokationsdaten['NABENHOEHE'][i], numpy.int64) == False and isinstance(
                    lokationsdaten['NABENHOEHE'][i], int) == False:
                print(type(lokationsdaten['NABENHOEHE'][i]))
                lokationsdaten['NABENHOEHE'][i] = 92.4
                print('Fehler NABENHOEHE nicht schlimm')


            '-----------------------------------------------------------------------------------------'
            "mit annualOutput_WKA wird die Jahresleistung für eine WKA mit den Kenndaten berechnet"
            '''(  weatherID_hight,
                     windklasse_wka, META_first_wind_limit, META_sec_wind_limit, META_third_wind_limit,
                     META_first_power_limit, META_sec_power_limit, META_third_power_limit, ignoreWindIEC = False,
                     eisman=False):'''

            leistung = annualOutput_WKA(year, Ein_ms, Nenn_ms, Abs_ms, lokationsdaten['LEISTUNG'][i],
                                        wetterdaten[matcheswetterdaten[0]], lokationsdaten['NABENHOEHE'][i],
                                        dictWeatherID[temp_weatherID]['Messhight'],
                                        dictWeatherID[temp_weatherID]['windklasse'],
                                        META_first_wind_limit=META_first_wind_limit,
                                        META_sec_wind_limit=META_sec_wind_limit,
                                        META_third_wind_limit=META_third_wind_limit,
                                        META_first_power_limit=META_first_power_limit,
                                        META_sec_power_limit=META_sec_power_limit,
                                        META_third_power_limit=META_third_power_limit,
                                        use_wind_IEC=False,
                                        eisman=eisman)

            leistung_wirk = leistung[0]
            leistung_eisman_int = leistung[1]
            # print('---------------')
            # print(sum(leistung_wirk))
            # print(sum(leistung_eisman_int))
            exportFrame[columnName] = leistung_wirk

            for i in range(len(leistung_eisman)):
                leistung_eisman[i] = int(leistung_eisman[i]) + int(leistung_eisman_int[i])

            # print(sum(leistung_eisman))
            DB_WKA_name.append(temp_db_wka_name)
            DB_WKA_power.append(leistung_wirk)
            DB_WKA_eisman.append(leistung_eisman_int)

            print(columnName)

    if eisman == True:
        exportname = 'Datenbank/Erzeugung/Einzel/Erz_' + source + '_' + state + '_' + str(year) + '_eisman' +'.csv'
    else:
        exportname = 'Datenbank/Erzeugung/Einzel/Erz_' + source + '_' + state + '_' + str(year) + '.csv'
    # print(exportFrame)

    exportFrame.to_csv(exportname, sep=';', encoding='utf-8-sig', index=False, decimal=',')
    print("Modell ungekannt Anzahl: ", modellunbekannt)
    print("Wetter-ID ungekannt Anzahl: ", wetterIDunbekannt)
    print("Eingelesene Zeilen", lengthLocation)
    print("Ausgegebene Zeilen", len(exportFrame.columns))

    print('Fertig')
    return leistung_eisman

def generation_PV_energy(year, source, state):
    exportFrame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', '60min')

    filelist = findoutFiles('Datenbank/ConnectwithID/Erzeugung')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(year) in match]
    print(matchfilelist3)

    try:
        openfilename2 = 'Datenbank/Wetter/' + source + '_Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)
        # print(wetterdaten)
    except ValueError:
        print("erzeugungsdaten_ee_anlagen Falsches Format")

    modellunbekannt = 0
    wetterIDunbekannt = 0
    lengthLocation2 = 0

    if source == 'PV':
        try:
            headerlistLokation = ['Leistung', 'Bundesland', 'Wetter-ID']
            openfilename1 = 'Datenbank/ConnectwithID/Erzeugung/' + matchfilelist3[0]
            print(openfilename1)

            lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal=',',
                                         header=0, encoding='utf-8')

            lengthLocation = lokationsdaten.__len__()
            # print(lokationsdaten)
        except ValueError:
            print("falsches Format")

        for i in range(lengthLocation):
            leistung = []
            # print(i)
            # print(str(lokationsdaten['Wetter-ID'][i]))

            matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                  str(lokationsdaten['Wetter-ID'][i]) in match]
            # print(matcheswetterdaten)
            if len(matcheswetterdaten) != 2:
                print('Fehler Wetterdaten')
                break

            columnName = str(i) + '_Ezg_PV' + '_' + str(lokationsdaten['Bundesland'][i]) + '_' + str(
                lokationsdaten['Wetter-ID'][i])

            fkt_Bestrahlung = 492.48
            fkt_Solar = 0.9

            for k in wetterdaten[matcheswetterdaten[0]]:

                if k < 0:
                    leistung.append(0)
                else:
                    # print(lokationsdaten['Bruttoleistung der Einheit'][i])
                    # print(type(lokationsdaten['Bruttoleistung der Einheit'][i]))
                    x = lokationsdaten['Leistung'][i] * (k / fkt_Bestrahlung) * fkt_Solar
                    leistung.append(x)

            # print('Eintrag bei ', i)
            exportFrame[columnName] = leistung
            # print('Eintrag Efolgreich ', i)

    exportname = 'Datenbank/Erzeugung/Einzel/Erz_' + source + '_' + state + '_' + str(year) + '.csv'
    exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')
    print("Modell ungekannt Anzahl: ", modellunbekannt)
    print("Wetter-ID ungekannt Anzahl: ", wetterIDunbekannt)
    print("Eingelesene Zeilen", lengthLocation2)
    print("Ausgegebene Zeilen", len(exportFrame.columns))

    print('Fertig')

def erzeugung_WKA_areawith_weatherID(year, wetterdaten, lokationsdaten, dictModell, dictWeatherID,
                                     META_first_wind_limit=0, META_sec_wind_limit=0,META_third_wind_limit=0,
                                     META_first_power_limit=0,META_sec_power_limit=0,META_third_power_limit=0,
                                     eisman = False, export=False):

    exportFrame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', '60min')

    temp_eisman = [0] * len(exportFrame)
    DB_WKA_name = []
    DB_WKA_power = []
    DB_WKA_eisman = []

    for i in range(len(lokationsdaten)):

        WKAunbekannt = False
        # print(str(lokationsdaten['Wetter-ID'][i]))

        matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                              str(lokationsdaten['Wetter-ID'][i]) in match]
        # print(matcheswetterdaten)
        if len(matcheswetterdaten) != 2:
            print('Fehler Wetterdaten nicht schlimm')
            print('Station: ', lokationsdaten['Wetter-ID'][i])
            lokationsdaten['Wetter-ID'][i] = 3086
            matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                  str(lokationsdaten['Wetter-ID'][i]) in match]

            # wetterIDunbekannt += 1

        columnName = str(i) + '_Ezg_' + str(
            lokationsdaten['Modell'][i]) + '_' + str(lokationsdaten['Wetter-ID'][i])
        temp_wka_name = lokationsdaten['Modell'][i] + '_' + str(lokationsdaten['NABENHOEHE'][i])

        temp_db_wka_name = 'Ezg_' + str(lokationsdaten['Modell'][i]) + '_' + str(
            lokationsdaten['NABENHOEHE'][i]) + '_' + str(lokationsdaten['Wetter-ID'][i])

        if temp_db_wka_name in DB_WKA_name:
            # gibt index von WKA
            jindex = DB_WKA_name.index(temp_db_wka_name)
            # befüllt die Frames
            exportFrame[columnName] = DB_WKA_power[jindex]

            for i in range(len(temp_eisman)):
                temp_eisman[i] = int(DB_WKA_eisman[jindex][i]) + int(temp_eisman[i])

            print('Über DB gelöst: ',columnName, 'Index: ', jindex)
            continue

        try:
            # print(temp_wka_name)
            Ein_ms = dictModell[temp_wka_name]['Ein_ms']

        except:
            Ein_ms = 3
            # print("Modell unbekannt")
            WKAunbekannt = True
        try:
            Nenn_ms = dictModell[temp_wka_name]['Nenn_ms']
        except:
            Nenn_ms = 13
            # print("Modell unbekannt")
            WKAunbekannt = True
        try:
            Abs_ms = dictModell[temp_wka_name]['Abs_ms']
        except:
            Abs_ms = 25
            WKAunbekannt = True

        if WKAunbekannt == True:
            print("Modell unbekannt: ", lokationsdaten['Modell'][i], temp_wka_name)
            # modellunbekannt += 1

        if isinstance(lokationsdaten['LEISTUNG'][i], float) == False and isinstance(
                lokationsdaten['LEISTUNG'][i], numpy.int64) == False:
            lokationsdaten['LEISTUNG'][i] = 3500
            print('Fehler Leistungsdaten nicht schlimm')
            print(columnName)

        '-----------------------------------------------------------------------------------------'
        "mit annualOutput_WKA wird die Jahresleistung für eine WKA mit den Kenndaten berechnet"
        temp_name = matcheswetterdaten[0].split('_')
        temp_weather_ID = int(temp_name[2])
        # print(temp_Modell)
        # print(dictWeatherID[temp_Modell]['Messhight'])
        temp_leistung = annualOutput_WKA(year, Ein_ms, Nenn_ms, Abs_ms, lokationsdaten['LEISTUNG'][i],
                                         wetterdaten[matcheswetterdaten[0]], lokationsdaten['NABENHOEHE'][i],
                                         dictWeatherID[temp_weather_ID]['Messhight'],
                                         dictWeatherID[temp_weather_ID]['windklasse'],
                                         META_first_wind_limit=META_first_wind_limit,
                                         META_sec_wind_limit=META_sec_wind_limit,
                                         META_third_wind_limit=META_third_wind_limit,
                                         META_first_power_limit=META_first_power_limit,
                                         META_sec_power_limit=META_sec_power_limit,
                                         META_third_power_limit=META_third_power_limit,
                                         use_wind_IEC= False, eisman=eisman)

        leistung_wirk = temp_leistung[0]
        leistung_eisman_int = temp_leistung[1]


        exportFrame[columnName] = leistung_wirk

        for i in range(len(temp_eisman)):
            temp_eisman[i] = int(leistung_eisman_int[i]) + int(temp_eisman[i])

        DB_WKA_name.append(temp_db_wka_name)
        DB_WKA_power.append(leistung_wirk)
        DB_WKA_eisman.append(leistung_eisman_int)

        print(columnName)

    if export == True:
        if eisman == False:
            exportname = 'Datenbank/Erzeugung/Erz_geplanterAusbau/Erz_geplanterAusbau_' + str(year) + '.csv'
        if eisman == True:
            eisman_name = 'eisman_' + str(META_first_wind_limit) + '_' + str(
                    META_sec_wind_limit) + '_' + str(META_third_wind_limit) + '_' + str(
                    META_first_power_limit) + '_' + str(META_sec_power_limit) + '_' + str(
                    META_third_power_limit)

            exportname = 'Datenbank/Erzeugung/Erz_geplanterAusbau/Erz_geplanterAusbau_' + str(
                year) + '_' + eisman_name + '.csv'



        exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    return exportFrame, temp_eisman


def erzeugungPerStunde(year, openfilename, source1, weatherIDlist,verlust_eisman = 0, single_ID_export = False, complete_export=True,
                       eisman = False):
    print("Start Erzeugung per Stunde")

    files = findoutFiles('Datenbank/Erzeugung/Einzel')

    matches = [match for match in files if str(year) in match]
    matches = [match for match in matches if str(source1) in match]


    if eisman == False:
        matches = [match for match in matches if str('eisman') not in match]
    if eisman == True:
        matches = [match for match in matches if str('eisman') in match]

    Datumabgleich = DateList('01.01.' + str(year) + ' 00:00',
                             '31.12.' + str(year) + ' 23:00', '60min', list=True)
    lengthmachtes = matches.__len__()

    for i in range(lengthmachtes):
        try:
            openfilename2 = 'Datenbank/Erzeugung/Einzel/' + matches[i]
            print(openfilename2)
            df2 = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)

        except:
            print('FEHLER')

        if i == 0:
            df = df2.copy()
            # print(df)
        if i > 0:
            del df2['Datum']
            # df.merge(right=df2, left_index=True, right_on='Datum')
            df = pd.concat([df, df2], axis=1, sort=False)
            sum_1 = df.sum(axis=1, numeric_only=None)
            # print(sum_1)

    tem_df = df.copy()

    if single_ID_export == True:
        single_export_frame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', '60min')

        for i in weatherIDlist:
            matches = [match for match in tem_df.columns.values.tolist() if str(i) in match]
            columname = str(i) + '_' + str(len(matches))
            temp_list = [0] * len(single_export_frame)
            #print(len(single_export_frame))

            for j in matches:
                #print(len(df[j]))
                temp_list += tem_df[j].astype(int)

            single_export_frame[columname] = temp_list
            #print(single_export_frame)
        exportname = 'Erzeigung_weatherID_'+ str(year) +'.csv'
        single_export_frame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')



    del df['Datum']

    sum_3 = df.sum(axis=1, numeric_only=None)

    # print(sum_3)
    lengthDatum = len(Datumabgleich)
    lentghSum_3 = len(sum_3)
    if lengthDatum != lentghSum_3:
        print('FEHLER')

    Erz_Name = 'Erzeugung_' + str(source1)
    AusgabeFrame = pd.DataFrame(
        {
            'Datum': Datumabgleich,
            Erz_Name: sum_3
        }
    )
    if eisman == True:
        print(type(verlust_eisman))
        print(verlust_eisman)
        AusgabeFrame['verluste_eisman_wind'] = verlust_eisman
    if complete_export == True:

        AusgabeFrame.to_csv(openfilename, sep=';', encoding='utf-8', index=False, decimal=',')

    return AusgabeFrame


def erzeugungPerStunde_singleFrame(year, ErzeugungFrame, temp_exportname,eisman_list = 0,eisman = False, export=False):
    print("Start Erzeugung per Stunde")

    Datumabgleich = DateList('01.01.' + str(year) + ' 00:00',
                             '31.12.' + str(year) + ' 23:00', '60min', list=True)

    del ErzeugungFrame['Datum']
    sum_3 = ErzeugungFrame.sum(axis=1, numeric_only=None)

    # print(sum_3)
    lengthDatum = len(Datumabgleich)
    lentghSum_3 = len(sum_3)
    if lengthDatum != lentghSum_3:
        print('FEHLER')

    Erz_Name = 'Erzeugung_geplanterAusbau_Wind'
    AusgabeFrame = pd.DataFrame(
        {
            'Datum': Datumabgleich,
            Erz_Name: sum_3
        }
    )
    if eisman == True:
        AusgabeFrame['verluste_eisman_geplanterAusbau'] = eisman_list
    if export == True:
        exportname = temp_exportname
        AusgabeFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    return AusgabeFrame


def verbrauchGesamt(year, export=False):
    files = findoutFiles('Datenbank/Verbrauch/Einzeln')

    matches = [match for match in files if str(year) in match]

    Datumabgleich = DateList('01.01.' + str(year) + ' 00:00',
                             '31.12.' + str(year) + ' 23:00', '60min', list=True)

    try:
        openfilename = 'Datenbank/Verbrauch/Einzeln/' + matches[0]
        print(openfilename)
        df = pd.read_csv(openfilename, encoding='utf-8', delimiter=';', decimal=',', header=0)
        # print(df.index)
    except:
        print('falsches Format: ', openfilename)
        raise RuntimeError('Programmabbruch da der Verbrauch nicht eingelesen werden konnten')

    del df['Datum']

    sum_G = df.sum(axis=1, numeric_only=None)
    sum_HH = df['HH_NETZ_Hamburg']
    del df['HH_NETZ_Hamburg']
    sum_SH = df.sum(axis=1, numeric_only=None)

    AusgabeFrame = pd.DataFrame(
        {
            'Datum': Datumabgleich,
            'Verbrauch_Gesamt': sum_G,
            'Verbrauch_HH': sum_HH,
            'Verbrauch_SH': sum_SH,
        }
    )

    if export == True:
        exportname = "Datenbank/Verbrauch/Verbrauch_komuliert_" + str(year) + ".csv"
        AusgabeFrame.to_csv(exportname, sep=';', encoding='utf-8-sig', index=False, decimal=',')
        print('Fertig')

    return AusgabeFrame


def analyseEE(year, exportfolder, listSpeicher=0, EE_Erz=0, PV_Gesamt=0, erz_Bio=0, plannedErzeung=0, verbrauch=0,
              ausbauWind=0,
              ausbauWindeisman=0, ausbauPV=0, ausbauBio=0, key_name = 'leer', ausbau=False,
              export=False, geplanterAusbau=True, biomes=True, wind=True, PV=True,
              expansionPV=0, expansionBio=0, speicher=False, eisman = False):

    # print(FrameVerbrauch)
    # print(FrameErzeung)
    # print(EE_Erz)
    temp_EE_Erz = [0] * len(verbrauch['Verbrauch_Gesamt'])
    if eisman == True:
        temp_eisman = [0] * len(verbrauch['Verbrauch_Gesamt'])
    if eisman == False:
        '''del EE_Erz['verluste_eisman_wind']
        del plannedErzeung['verluste_eisman_geplanterAusbau']'''
    # Wird für Darstellungszwecke genutzt
    '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
    # Wind
    if wind == True:
        EE_Erz['Erzeugung_Wind_Gesamt'] = EE_Erz['Erzeugung_Wind'].copy()
        temp_EE_Erz += EE_Erz['Erzeugung_Wind']
        if eisman == True:
            temp_eisman += EE_Erz['verluste_eisman_wind']
    if wind == False:
        del EE_Erz['Erzeugung_Wind']
    # Wind Ausbau geplant
    if geplanterAusbau == True:
        EE_Erz['Erz_geplAusbau_Wind'] = plannedErzeung['Erzeugung_geplanterAusbau_Wind'].copy()
        EE_Erz['Erzeugung_Wind_Gesamt'] += plannedErzeung['Erzeugung_geplanterAusbau_Wind']
        temp_EE_Erz += EE_Erz['Erz_geplAusbau_Wind']
        if eisman == True:
            EE_Erz['verluste_eisman_geplanterAusbau'] = plannedErzeung['verluste_eisman_geplanterAusbau'].copy()
            temp_eisman += EE_Erz['verluste_eisman_geplanterAusbau']
    if geplanterAusbau == False:
        # print('del EE_Erz["Erz_geplAusbau_Wind"]')
        '''del EE_Erz['Erz_geplAusbau_Wind']'''
    # Wind Ausbau Software
    if ausbau == True and sum(ausbauWind) > 0:
        EE_Erz['REE_Wind'] = ausbauWind
        EE_Erz['Erzeugung_Wind_Gesamt'] += ausbauWind
        temp_EE_Erz += EE_Erz['REE_Wind']
    if ausbau == True and sum(ausbauWindeisman) > 0 and eisman == True:
        EE_Erz['REE_Wind_eisman_verluste'] = ausbauWindeisman
        temp_eisman += EE_Erz['REE_Wind_eisman_verluste']
    '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
    # PV
    if PV == True:
        EE_Erz['Erz_PV_Gesamt'] = PV_Gesamt
        EE_Erz['Erz_PV'] = PV_Gesamt
        temp_EE_Erz += EE_Erz['Erz_PV']

    # PV Ausbau Software
    if ausbau == True and sum(ausbauPV) > 0:
        print('New Energysum PV GWh: ', sum(ausbauPV)/1000000)
        EE_Erz['Erz_PV_Gesamt'] += ausbauPV
        EE_Erz['REE_PV'] = ausbauPV
        temp_EE_Erz += EE_Erz['REE_PV']

    '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
    # Biomasse
    if biomes == True:
        EE_Erz['Erz_Biomasse_Gesamt'] = erz_Bio
        EE_Erz['Erz_Biomasse'] = erz_Bio
        temp_EE_Erz += EE_Erz['Erz_Biomasse']

    # Biomasse Ausbau Software
    if ausbau == True and sum(ausbauBio) > 0:
        print('New Energysum Bio GWh: ', sum(ausbauBio) / 1000000)
        EE_Erz['REE_Biomasse'] = ausbauBio
        EE_Erz['Erz_Biomasse_Gesamt'] += EE_Erz['REE_Biomasse']
        temp_EE_Erz += EE_Erz['REE_Biomasse'].tolist()

    EE_Erz['Erzeugung_Gesamt'] = temp_EE_Erz

    if eisman == True:
        EE_Erz['verluste_eisman_Gesamt'] = temp_eisman

    EE_Erz['Diff_Erz_zu_Verbrauch'] = EE_Erz['Erzeugung_Gesamt'] - verbrauch['Verbrauch_Gesamt']
    temp_Diff_EE_zu_Verb = EE_Erz['Diff_Erz_zu_Verbrauch'].tolist().copy()
    temp_len_speicherList = len(listSpeicher)

    if speicher == True and temp_len_speicherList > 0:


        EE_Erz['Speicherkapazität'] = [0.0] * len(temp_EE_Erz)
        EE_Erz['Speicherstatus'] = [0.0] * len(temp_EE_Erz)
        EE_Erz['Speicher_voll_Prozent'] = [0.0] * len(temp_EE_Erz)
        EE_Erz['Ein(+)-/ Ausspeisung(-)'] = [0.0] * len(temp_EE_Erz)
        EE_Erz['Speicherverluste'] = [0.0] * len(temp_EE_Erz)

        for i in range(temp_len_speicherList):

            EE_Erz['Speicherkapazität'] += listSpeicher[i].max_capacity
            listSpeicher[i].reset_current_capacity()

        for jndex, j in enumerate(temp_Diff_EE_zu_Verb):
            # Für jeden Bilanz Wert
            if j <= 0.0:
                # Wenn zu wenig Energie im Netz ist
                for k in range(temp_len_speicherList):
                    # Für jeden Speicher Output
                    temp_power = listSpeicher[k].output_power(temp_Diff_EE_zu_Verb[jndex])
                    temp_Diff_EE_zu_Verb[jndex] += temp_power[0]
                    EE_Erz['Speicherstatus'][jndex] += listSpeicher[k].get_current_capacity()
                    EE_Erz['Ein(+)-/ Ausspeisung(-)'][jndex] -= temp_power[0]
                    EE_Erz['Speicherverluste'][jndex] += temp_power[1]
                    EE_Erz['Speicher_voll_Prozent'][jndex] = EE_Erz['Speicherstatus'][jndex] / \
                                                             EE_Erz['Speicherkapazität'][jndex]
            elif j > 0.0:
                # Wenn zu viel Energie im Netz ist
                for k in range(temp_len_speicherList):
                    # Für jeden Speicher Input
                    temp_power = listSpeicher[k].input_power(temp_Diff_EE_zu_Verb[jndex])
                    temp_Diff_EE_zu_Verb[jndex] -= temp_power[0] + temp_power[1]
                    EE_Erz['Speicherstatus'][jndex] += listSpeicher[k].get_current_capacity()
                    EE_Erz['Ein(+)-/ Ausspeisung(-)'][jndex] += temp_power[0]
                    EE_Erz['Speicherverluste'][jndex] += temp_power[1]
                    EE_Erz['Speicher_voll_Prozent'][jndex] = EE_Erz['Speicherstatus'][jndex] / \
                                                             EE_Erz['Speicherkapazität'][jndex]
        EE_Erz['Erzeugung_mit_Speicher'] = EE_Erz['Erzeugung_Gesamt'] - EE_Erz['Ein(+)-/ Ausspeisung(-)']
        EE_Erz['Diff_Erz_zu_Verb_mit_Speicher'] = temp_Diff_EE_zu_Verb

    # Erzeugung Gesamt | Ein-/ Ausspeisung     | Verbrauch
    # 1000             -    (+500)                    / 500        Input Speicher
    # 250              +    (-250)                    / 500     Output Speicher

    EE_Erz['Verbrauch_Gesamt'] = verbrauch['Verbrauch_HH'] + verbrauch['Verbrauch_SH']

    EE_Erz['Verbrauch_HH'] = verbrauch['Verbrauch_HH']
    EE_Erz['Verbrauch_SH'] = verbrauch['Verbrauch_SH']
    if speicher == False:
        EE_Erz['EE_Anteil'] = EE_Erz['Erzeugung_Gesamt'] / verbrauch['Verbrauch_Gesamt']
    else:
        EE_Erz['EE_Anteil'] = (EE_Erz['Erzeugung_Gesamt'] - EE_Erz['Ein(+)-/ Ausspeisung(-)']) / verbrauch[
            'Verbrauch_Gesamt']

    liste_100 = []
    liste_75 = []
    liste_60 = []
    liste_50 = []
    liste_45 = []
    liste_k45 = []

    for i in EE_Erz['EE_Anteil']:

        if i >= 1.0:
            liste_100.append(True)
            liste_75.append(True)
            liste_60.append(True)
            liste_50.append(True)
            liste_45.append(True)
            liste_k45.append(True)
            continue
        if i >= 0.75:
            liste_100.append(False)
            liste_75.append(True)
            liste_60.append(True)
            liste_50.append(True)
            liste_45.append(True)
            liste_k45.append(True)
            continue
        if i >= 0.6:
            liste_100.append(False)
            liste_75.append(False)
            liste_60.append(True)
            liste_50.append(True)
            liste_45.append(True)
            liste_k45.append(True)
            continue
        if i >= 0.5:
            liste_100.append(False)
            liste_75.append(False)
            liste_60.append(False)
            liste_50.append(True)
            liste_45.append(True)
            liste_k45.append(True)
            continue
        if i >= 0.45:
            liste_100.append(False)
            liste_75.append(False)
            liste_60.append(False)
            liste_50.append(False)
            liste_45.append(True)
            liste_k45.append(True)
            continue
        if i < 0.45:
            liste_100.append(False)
            liste_75.append(False)
            liste_60.append(False)
            liste_50.append(False)
            liste_45.append(False)
            liste_k45.append(True)
            continue

    EE_Erz['EE>100%'] = liste_100
    EE_Erz['EE>75%'] = liste_75
    EE_Erz['EE>60%'] = liste_60
    EE_Erz['EE>50%'] = liste_50
    EE_Erz['EE>45%'] = liste_45
    EE_Erz['EE<45%'] = liste_k45
    uhrzeit = datetime.now().strftime('%H-%M')
    exportname = 0
    EE_Anteil = sum(liste_100) / sum(liste_k45)
    temp_EEAnteil = EE_Anteil * 100
    exportname = exportfolder + 'REE_' + str(key_name) + '_' + str(int(temp_EEAnteil)) + '_' + str(year) + '_' + str(
        uhrzeit) + '.csv'
    if export == True:
        print(exportname)
        EE_Erz.to_csv(exportname, sep=';', encoding='utf-8-sig', index=False, decimal=',')

    return EE_Erz, EE_Anteil , exportname


def analyseAusbauFl():
    print('Start mit Analyse')
    filelist = findoutFiles('Datenbank/Ausbauflaechen/AusbauStandorte_gesamt_SH')
    matchfilelist = [match for match in filelist if 'AlleStandorte' in match]
    try:
        openfilename1 = 'Datenbank/Ausbauflaechen/AusbauStandorte_gesamt_SH/' + matchfilelist[0]
        print(openfilename1)

        lokdaten = pd.read_csv(openfilename1, delimiter=';', decimal=',',
                               header=0, encoding='utf-8')

        lengthLokationsdaten = lokdaten.__len__()
        # print(lokdaten)
    except ValueError:
        print("falsches Format")
    lokdaten['haVor'] = lokdaten['haVor'].astype(float)
    potValue_mitWKA = lokdaten[lokdaten["WKAPot"] == 'WKA in Betrieb'].sum()["haPot"]
    vorValue_mitWKA = lokdaten[lokdaten["WKAVor"] == 'WKA in Betrieb'].sum()["haVor"]
    potAnz_mitWKA = lokdaten[lokdaten["WKAPot"] == 'WKA in Betrieb'].count()["haPot"]
    vorAnz_mitWKA = lokdaten[lokdaten["WKAVor"] == 'WKA in Betrieb'].count()["haVor"]
    potValue_ohneWKA = lokdaten[lokdaten["WKAPot"] == '-'].sum()["haPot"]
    vorValue_ohneWKA = lokdaten[lokdaten["WKAVor"] == '-'].sum()["haVor"]
    potAnz_ohneWKA = lokdaten[lokdaten["WKAPot"] == '-'].count()["haPot"]
    vorAnz_ohneWKA = lokdaten[lokdaten["WKAVor"] == '-'].count()["haVor"]

    print('MIT WKA ANLAGEN BEREITS AUF DER FLÄCHE')
    print('Potential Fläche: ', potValue_mitWKA)
    print('Vorrang Fläche: ', vorValue_mitWKA)
    print('Anzahl PotentialFl: ', potAnz_mitWKA)
    print('Anzahl Vorrang: ', vorAnz_mitWKA)
    print('OHNE WKA ANLAGEN BEREITS AUF DER FLÄCHE')
    print('Potential Fläche: ', potValue_ohneWKA)
    print('Vorrang Fläche: ', vorValue_ohneWKA)
    print('Anzahl PotentialFl: ', potAnz_ohneWKA)
    print('Anzahl Vorrang: ', vorAnz_ohneWKA)


def windlastprofil(year, exportfolder, export=True):
    print("Start WindLastProfil")

    try:
        openfilename2 = 'Datenbank/Wetter/Wind_Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)
        # print(wetterdaten)
    except ValueError:
        print("falsches Format")

    mWd = [match for match in wetterdaten.columns.values.tolist() if
           str('m/s') in match]

    WindAnalyseSchritte = []

    for i in range(36):
        WindAnalyseSchritte.append(i)
        # WindAnalyseSchritte.append(i+schritt)

    del WindAnalyseSchritte[0:1]

    AnalyseProfilbz = []
    for i in WindAnalyseSchritte:
        AnalyseProfilbz.append('von_' + str(i - 1) + '_bis_' + str(i) + '_ms')

    # print(WindAnalyseSchritte)
    # print(AnalyseProfilbz)

    'Header Names für die Auswertung'
    exportFrame = pd.DataFrame(
        {'AnalyseProfil': AnalyseProfilbz
         }
    )

    # print(exportFrame)

    for i in range(len(mWd)):

        # print(wetterdaten[mWd[i]])

        listparameter = [0] * len(WindAnalyseSchritte)

        for j in wetterdaten[mWd[i]]:

            for index, k in enumerate(WindAnalyseSchritte):

                if index > k:
                    print('Stop')
                if float(j) > float(index) and float(j) <= float(k):
                    listparameter[index] += 1

        name = mWd[i]
        exportFrame[name] = listparameter

    exportFrame.set_index('AnalyseProfil', inplace=True)
    # print(exportFrame)
    # exportFrame2 = exportFrame.T
    # print(exportFrame2)
    # exportFrame2.loc['AnalyseProfil',:] = AnalyseProfilbz
    if export == True:
        exportname2 = exportfolder + str(year) + '.csv'
        exportFrame.to_csv(exportname2, sep=';', encoding='utf-8-sig', index=True, decimal=',')

    return exportFrame


def windlastprofil_einzel(windWeatherlist):
    WindAnalyseSchritte = []

    for i in range(36):
        WindAnalyseSchritte.append(i)
        # WindAnalyseSchritte.append(i+schritt)

    del WindAnalyseSchritte[0:1]

    listparameter = [0] * len(WindAnalyseSchritte)

    for j in windWeatherlist:
        # print(len(temp_wather))
        treffer = False
        for index, k in enumerate(WindAnalyseSchritte):
            # print(float(j), float(k))
            if index > k:
                print('Stop')

            if float(j) == 0.0:
                listparameter[0] += 1
                treffer = True
                break

            elif float(j) > float(index) and float(j) <= float(k):
                listparameter[index] += 1
                treffer = True
                break

            elif float(j) > 35.0:
                listparameter[34] += 1
                treffer = True
                break

        if treffer == False:
            print(j)

            # print(listparameter[index])
    # print(sum(listparameter))
    return listparameter


def stand_distance_analyse_alt(year, standorte):
    filelist = findoutFiles('Datenbank/ConnectwithID/Erzeugung')
    matches1 = [match for match in filelist if str(year) in match]
    matches1 = [match for match in matches1 if 'SH' in match]
    matches1 = [match for match in matches1 if 'UTM' in match]

    try:
        openfilename1 = 'Datenbank/ConnectwithID/Erzeugung/' + matches1[0]
        print(openfilename1)

        WKA = pd.read_csv(openfilename1, delimiter=';', decimal=',', encoding='utf-8')

    except:
        print('falsches Format')

    list = []
    listnames = []

    testTuper = ('0', '0')
    for index, i in enumerate(WKA['Coords UTM']):
        tempList = []
        temp_wka = geo.editCoords(i)

        for kindex, j in enumerate(standorte['Coords Vor']):

            temp_ausbau = geo.editCoords(j)
            if temp_ausbau != testTuper and standorte['WKAVor'][kindex] == 'WKA in Betrieb':
                tempList.append(geo.distance(temp_wka, temp_ausbau))

        list.append(tempList)

    p = 1
    for index, i in enumerate(standorte['ID']):
        temp_ausbau = geo.editCoords(standorte['Coords Vor'][index])

        if temp_ausbau != testTuper and standorte['WKAVor'][index] == 'WKA in Betrieb':
            columnName = str(p) + '_' + i
            p += 1
            listnames.append(columnName)

    # del exportFrame['Datum']
    # print(exportFrame)

    exportFrame = pd.DataFrame(np.c_[list], columns=listnames)
    exportFrame.insert(loc=0, column='Typ', value=WKA['TYP'])
    finished_filename = 'KurzAnschauen.csv'

    exportFrame.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='UTF-8')


def connect_oldWKA_to_expansionArea(year, Vor_Pot, standorte, faktorAusbaufl, export=True, geplanterAusbau=True):
    filelist = findoutFiles('Datenbank/ConnectwithID/Erzeugung')
    matches1 = [match for match in filelist if str(year) in match]
    matches1 = [match for match in matches1 if 'SH' in match]
    matches1 = [match for match in matches1 if 'UTM' in match]
    if geplanterAusbau == True:
        matches1 = [match for match in matches1 if 'WindparksSH_geplanterAusbau_UTM_WeatherID_2019_2020' not in match]

    temp_first = False
    listnames = 0
    listFl = 0
    anzahl = 0
    for i in matches1:

        try:
            openfilename1 = 'Datenbank/ConnectwithID/Erzeugung/' + i
            print(openfilename1)

            WKA = pd.read_csv(openfilename1, delimiter=';', decimal=',', encoding='utf-8')
            WKA = WKA.fillna(0)

        except:
            raise RuntimeError('Berechnete Erzeugung kann nicht geladen werden')

        WKA['Anlageauf_Vor_Verbaut'] = [False] * len(WKA['Coords UTM'])

        if temp_first == False:
            testTuple = ('0', '0')
            listnames = []
            p = 1
            "For Schleifen macht aus [] ein ()"
            for qindex, i in enumerate(standorte['ID']):
                temp_ausbau = geo.editCoords(standorte['Coords ' + Vor_Pot][qindex])

                if temp_ausbau != testTuple and standorte['WKA' + Vor_Pot][qindex] == 'WKA in Betrieb':
                    p += 1
                    listnames.append(i)

            temp_first = True

            listFl = [0] * len(listnames)
            anzahl = [0] * len(listnames)

        standortindex = 0

        for index, i in enumerate(standorte['Coords ' + Vor_Pot]):

            temp_ausbau = geo.editCoords(i)
            if temp_ausbau != testTuple and standorte['WKA' + Vor_Pot][index] == 'WKA in Betrieb':

                for kindex, j in enumerate(WKA['Coords UTM']):

                    if WKA['Anlageauf_Vor_Verbaut'][kindex] == True:
                        continue

                    temp_wka = geo.editCoords(j)
                    distance = geo.distance(temp_wka, temp_ausbau)

                    if distance <= faktorAusbaufl:
                        listFl[standortindex] += int((15 * np.square(float(WKA['ROTORDURCHMESSER'][kindex]))) / 10000)
                        anzahl[standortindex] += 1
                        WKA['Anlageauf_Vor_Verbaut'][kindex] = True
                        # print(listFl[standortindex], standorte['ha'+Vor_Pot][index])

                        if listFl[standortindex] >= standorte['ha' + Vor_Pot][index]:
                            break

                listFl[standortindex] = round(listFl[standortindex], 3)
                standortindex += 1

        # print(listFl)

    exportFrame = pd.DataFrame(np.c_[listnames, listFl, anzahl], columns=['ID', 'Flaeche_' + Vor_Pot, 'Anzahl WEAs'])

    if export == True:
        finished_filename = 'Datenbank/Ausbauflaechen/VerbauteFlaechen_radius_' + str(faktorAusbaufl) + '_' + str(
            year) + '.csv'
        exportFrame.to_csv(finished_filename, sep=';', index=False, decimal=',')

    return exportFrame


def freie_ha_vor(year, exportFolder, standorte, belgegteha_Vor, export=True):
    print('Start freie_ha_Vor')

    # print(standorte)
    # print(belgegteha)

    temp_freiVor = []
    temp_belegtVor = []
    temp_anzahl = []
    for index, i in enumerate(standorte['haVor']):
        x = 0
        y = 0
        z = 0
        for kindex, j in enumerate(belgegteha_Vor['Flaeche_Vor']):

            if belgegteha_Vor['ID'][kindex] == standorte['ID'][index]:
                # print(belgegteha['ID'][kindex], standorte['ID'][index])
                # print(i, j)
                x = (float(i) - float(j))
                if x < 0:
                    x = 0
                y = float(j)
                z = belgegteha_Vor['Anzahl WEAs'][kindex]
        # print(standorte['haVor'][index], standorte['WKAVor'][index] )
        if int(standorte['haVor'][index]) > 0 and standorte['WKAVor'][index] == '-':
            x = standorte['haVor'][index]

        temp_freiVor.append(abs(x))
        temp_belegtVor.append(y)
        temp_anzahl.append(z)
    # print(temp_freiVor)

    standorte['Anzahl WEAs_Vor'] = temp_anzahl
    standorte['besetze Flaeche_Vor'] = temp_belegtVor
    standorte['nettoFreieFlaeche_Vor'] = temp_freiVor
    standorte['Anzahl WEAs_Pot'] = [0] * len(temp_anzahl)
    standorte['nettoFreieFlaeche_Pot'] = [0] * len(temp_anzahl)
    standorte['besetze Flaeche_Pot'] = standorte['haPot']
    for index,i in enumerate(standorte['haPot']):

        x = i - standorte['besetze Flaeche_Vor'][index]

        if x > 0:
            standorte['nettoFreieFlaeche_Pot'][index] = x
        else:
           continue

    temp_anzahl = [0] * standorte['Anzahl WEAs_Vor']

    if export == True:
        finished_filename = exportFolder + 'FreieFlaechen_vorAusbau' + str(year) + '.csv'
        standorte.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')
    print('Ende freie_ha_pot')
    return standorte


def area_and_WKA_choice(negativGraph, DB_WKA, deepestPointsIndex, ausbauFlWeatherIDList, temp_ausgebauteAnlagen,
                        dict_WKA, spiecherMethodik=True):
    temp_newValue = False
    print('Start Analyse Ausbau')
    # print(EE_Analyse)
    copy_negativGraph = negativGraph.copy()
    max_boje_value = 0
    # Addition der Tiefsten Punkte
    for i in DB_WKA:
        temp_name = i.split('_')
        temp_ID = temp_name[0]
        if temp_ID not in str(ausbauFlWeatherIDList):
            del DB_WKA[i]
            continue
        if temp_ID in str(temp_ausgebauteAnlagen):
            del DB_WKA[i]
            continue

    temp_len = len(DB_WKA.columns.values.tolist())

    if temp_len < 20:
        print('Stop')

    for k in deepestPointsIndex:
        max_boje_value += copy_negativGraph[k]

    max_boje_value = 0
    WKAnameforexpansion = 'unbekannt'

    print('DB_WKA Len: ', len(DB_WKA.columns.values.tolist()))

    for i in DB_WKA:

        temp_name = i.split('_')
        temp_Modell = temp_name[1]
        temp_Modell_hight = temp_name[2]


        copy_negativGraph = negativGraph.copy()
        relevant_PowerWKA = 0

        if spiecherMethodik == True:
            for jndex in deepestPointsIndex:
                relevant_PowerWKA += DB_WKA[i][jndex]

        if spiecherMethodik == False:
            relevant_PowerWKA = DB_WKA[i] + copy_negativGraph
            relevant_PowerWKA = negativ_Verlauf(relevant_PowerWKA, speicherVerlauf=False)
            relevant_PowerWKA = abs(sum(copy_negativGraph)) - abs(sum(relevant_PowerWKA))


        temp_FlproPower = relevant_PowerWKA / dict_WKA[temp_Modell + '_' + temp_Modell_hight]['Flaeche']

        if temp_FlproPower > max_boje_value:
            max_boje_value = temp_FlproPower
            WKAnameforexpansion = i
            temp_newValue = True

    if temp_newValue == False:
        print(WKAnameforexpansion)

    return WKAnameforexpansion


def maxAnzahl_WKA(deepestPointValues, deepestPointsIndex, DB_WKA, modellName, ausbaubegrenzungsfaktor):
    start_deepestPointValues = sum(deepestPointValues)

    # Funktioniert noch nicht.
    # Muss angepasst werden!!!

    max_Anzahl = 1
    # Erhöhe solange die WKA anzahl, bis ein Ausbau der WKA vom erstausbau 80% ausmacht.
    # Erstausbau 800 kw/h -> mit einer Anlage
    # Zwischenstand 600kw/h -> im Schnitt je Anlage -> 75%(ausbaubegrenzungsfaktor) -> OK
    # weiterer Zwischenstand 580kw/h - 72,5% -> nicht ok, Anzahl stoppen.
    erstAusbau_WKA = 0
    # Ausbau einer WKA
    for index, i in enumerate(deepestPointsIndex):
        erstAusbau_WKA += (DB_WKA[modellName][i] * max_Anzahl)
    print(max_Anzahl)

    return max_Anzahl

    # while start_SumNegativGraph*
    # Muss später noch gemacht werden


def expansion_WKA(year,WKAKey, weatherID, WKADict, standort, windWetterdaten, Vor_Pot,META_first_wind_limit=0,
                    META_sec_wind_limit=0,META_third_wind_limit=0,META_first_power_limit=0,
                    META_sec_power_limit=0, META_third_power_limit=0,eisman=False):
    "Kenn ick"

    'Technische daten WKA'
    Ein_ms = WKADict[WKAKey]['Ein_ms']
    Nenn_ms = WKADict[WKAKey]['Nenn_ms']
    Abs_ms = WKADict[WKAKey]['Abs_ms']
    leistung_einzel = WKADict[WKAKey]['Nenn_kW']
    nabenhohe = WKADict[WKAKey]['Nabenhoehe']

    anzahl_2 = 0
    leistung_gesamt = 0
    temp_leistung = [0] * len(windWetterdaten['Wind_m/s_788'])
    temp_verlust = [0] * len(windWetterdaten['Wind_m/s_788'])
    matchfilelist = 0
    columnFrame = windWetterdaten.columns.values.tolist()
    columnName = ''

    for mndex, m in enumerate(standort['Wetter-ID_' + Vor_Pot]):

        if m != int(weatherID):
            # print(m, weatherID)
            continue

        if standort['nettoFreieFlaeche_' + Vor_Pot][mndex] < 0:
            continue

        WeaModell_fl = ((15 * np.square(float(WKADict[WKAKey]['Rotor']))) / 10000)
        standort['Anzahl_' + Vor_Pot][mndex] = int(standort['nettoFreieFlaeche_' + Vor_Pot][mndex] / WeaModell_fl)
        anzahl_2 += standort['Anzahl_' + Vor_Pot][mndex]
        leistung_wka = leistung_einzel * standort['Anzahl_' + Vor_Pot][mndex]

        if leistung_wka == 0 or leistung_wka == 123:
            continue

        standort['nettoFreieFlaeche_' + Vor_Pot][mndex] -= round((WeaModell_fl * standort['Anzahl_' + Vor_Pot][mndex]), 2)
        standort['Modell_' + Vor_Pot][mndex] = WKADict[WKAKey]['Modell']
        standort['Leistung_inMW_' + Vor_Pot][mndex] = round((leistung_wka/1000), 2)
        tempsum = (standort['Anzahl_'+Vor_Pot][mndex]*WKADict[WKAKey]['Invest'])/1000000
        standort['InvestKosten_inMio_' + Vor_Pot][mndex] = round(tempsum, 2)
        tempsum = (standort['Anzahl_'+Vor_Pot][mndex]*WKADict[WKAKey]['Betriebk'])/1000000
        standort['BetriebsKosten_inMio_' + Vor_Pot][mndex] = round(tempsum, 2)

        columnName = str(m) + '_Ezg_' + str(WKADict[WKAKey]['Modell'])

        matchfilelist = [match for match in columnFrame if weatherID in match]
        lengthlist = len(matchfilelist)

        if lengthlist != 2:
            matchfilelist.append('Wind_m/s_788')

        temp_wetter = wind_hochrechnung(windWetterdaten[matchfilelist[0]], nabenhohe, 10)
        temp_IEC_windklasse = IEC_windklasse(sum(temp_wetter), len(temp_wetter))

        if temp_IEC_windklasse < WKADict[WKAKey]['Windklasse']:
            continue

        temp_leistung_single = annualOutput_WKA(year, Ein_ms, Nenn_ms, Abs_ms, leistung_wka,
                                         windWetterdaten[matchfilelist[0]], nabenhohe,
                                         10,
                                         WKADict[WKAKey]['Windklasse'],
                                         META_first_wind_limit=META_first_wind_limit,
                                         META_sec_wind_limit=META_sec_wind_limit,
                                         META_third_wind_limit=META_third_wind_limit,
                                         META_first_power_limit=META_first_power_limit,
                                         META_sec_power_limit=META_sec_power_limit,
                                         META_third_power_limit=META_third_power_limit,
                                         use_wind_IEC=True, eisman=eisman)



        temp_wirk = temp_leistung_single[0]
        temp_verlust_single = temp_leistung_single[1]


        for i in range(len(temp_leistung)):
            temp_leistung[i] = temp_leistung[i] + temp_wirk[i]
            temp_verlust[i] = temp_verlust[i] + temp_verlust_single[i]

        leistung_gesamt += leistung_wka

    leistung_single = annualOutput_WKA(year, Ein_ms, Nenn_ms, Abs_ms, leistung_einzel,
                                            windWetterdaten[matchfilelist[0]], nabenhohe,
                                            10,
                                            WKADict[WKAKey]['Windklasse'],
                                            META_first_wind_limit=META_first_wind_limit,
                                            META_sec_wind_limit=META_sec_wind_limit,
                                            META_third_wind_limit=META_third_wind_limit,
                                            META_first_power_limit=META_first_power_limit,
                                            META_sec_power_limit=META_sec_power_limit,
                                            META_third_power_limit=META_third_power_limit,
                                            use_wind_IEC=True, eisman=eisman)

    print('Energy im Jahr in GW',sum(temp_leistung)/1000000, 'Anzahl :',anzahl_2, 'Leistung: ', leistung_gesamt)
    print('Energy verluste: ',sum(temp_verlust))
    return temp_leistung, columnName, anzahl_2, leistung_gesamt, temp_verlust, leistung_single[0], leistung_single[1]


def standortquality(year, wetterdaten, WKAanlagen):
    print('Start', year)
    temp_Header = wetterdaten.columns.values.tolist()
    exportFrame = pd.DataFrame(columns=['Name', 'Jahresleistung', 'ReferenzEnergieErtrag', 'Standortquality'])
    temp_name = []
    temp_Jahresleistung = []
    temp_ReferenzEnergieErtrag = []
    temp_Standortquality = []

    WKAunbekannt = False

    for i, value in enumerate(WKAanlagen['Modell']):
        print(i, value)
        if WKAanlagen['Referenzertrag [kWh]'][i] == 0:
            continue

        try:
            Ein_ms = WKAanlagen['Einschaltgeschwindigkeit m/s'][i]
        except:
            Ein_ms = 3
            # print("Modell unbekannt")
            WKAunbekannt = True
        try:
            Nenn_ms = WKAanlagen['Nenngeschwindigkeit m/s'][i]
        except:
            Nenn_ms = 13
            # print("Modell unbekannt")
            WKAunbekannt = True
        try:
            Abs_ms = WKAanlagen['Abschaltgeschwindigkeit m/s'][i]
        except:
            Abs_ms = 25
            WKAunbekannt = True

        if WKAunbekannt == True:
            print("Modell unbekannt")
            # modellunbekannt += 1

        if isinstance(WKAanlagen['LEISTUNG'][i], float) == False and isinstance(
                WKAanlagen['LEISTUNG'][i], numpy.int64) == False:
            WKAanlagen['LEISTUNG'][i] = 1000
            print('Fehler Leistungsdaten nicht schlimm')
        # print(WKAanlagen['NABENHOEHE'])

        mWd = [match for match in wetterdaten.columns.values.tolist() if
               str('m/s') in match]

        temp_nabe = WKAanlagen['NABENHOEHE'][i]
        for j in range(len(mWd)):

            temp_wind = wind_hochrechnung(wetterdaten[mWd[j]], temp_nabe, 10)

            windlastprofil = windlastprofil_einzel(temp_wind)

            temp_leistung = 0

            for qindex, k in enumerate(windlastprofil):
                qpindex = 1
                qpindex += qindex

                # Fehler raus suchen
                if qpindex < 0:
                    temp_leistung += 0

                # unter Nennleistung
                elif qpindex >= Ein_ms and qpindex < Nenn_ms:
                    x = FORMEL_WKA_Leistung(Nenn_ms, Ein_ms, WKAanlagen['LEISTUNG'][i], qpindex)
                    # print('moment_ms',k ,'Leistung', lokationsdaten['LEISTUNG'][i], 'Erzeigung', x )
                    # print(k ,lokationsdaten['LEISTUNG'][i], x)
                    temp_x = k * int(x)
                    temp_leistung = temp_leistung + temp_x
                # ueber nennleistung
                elif qpindex >= Nenn_ms and qpindex < Abs_ms:
                    temp_x = k * int(WKAanlagen['LEISTUNG'][i])
                    temp_leistung = temp_leistung + temp_x

                # außerhalb der Betriebsgeschwindigekeit
                elif qpindex >= Abs_ms or qpindex < Ein_ms:
                    temp_leistung += 0

                else:
                    print("Fehler")
                    temp_leistung += 0

            name = str(WKAanlagen['Modell'][i] + '_' + str(WKAanlagen['NABENHOEHE'][i]) + '_' + mWd[j])

            temp_name.append(name)
            temp_Jahresleistung.append(temp_leistung)
            # print(WKAanlagen['Referenzertrag [kWh]'][i])
            temp_ReferenzEnergieErtrag.append(WKAanlagen['Referenzertrag [kWh]'][i])
            # print(temp_leistung, WKAanlagen['Referenzertrag [kWh]'][i])
            if WKAanlagen['Referenzertrag [kWh]'][i] != 0:
                temp_Standortquality.append(temp_leistung / WKAanlagen['Referenzertrag [kWh]'][i])
            else:
                temp_Standortquality.append(0)

    exportFrame['Name'] = temp_name
    exportFrame['Jahresleistung'] = temp_Jahresleistung
    exportFrame['ReferenzEnergieErtrag'] = temp_ReferenzEnergieErtrag
    exportFrame['Standortquality'] = temp_Standortquality

    exportname2 = 'Standortquality.csv'
    exportFrame.to_csv(exportname2, sep=';', encoding='utf-8', index=True, decimal=',')

    return exportFrame


def DB_WKA(year, dictModell, dictWeatherID, wetterdaten, min_hight, META_first_wind_limit=0,
           META_sec_wind_limit=0 ,META_third_wind_limit=0, META_first_power_limit=0,META_sec_power_limit=0,
           META_third_power_limit=0, eisman= False ,export=True,):
    print('DB_WKA', str(year))

    date_perHoure = DateList('01.01.' + str(year) + ' 00:00',
                             '31.12.' + str(year) + ' 23:00', '60min', list=False)
    wetterstationen = 0
    WKA_True_Gesamt = 0
    WKA_False_Gesamt = 0
    for index in dictWeatherID:
        WKA_True = 0
        WKA_False_wind = 0
        WKA_False_ausbauRele = 0
        "Für alle Wetterstationen"
        matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                              str(dictWeatherID[index]['ID']) in match]
        if len(matcheswetterdaten) != 2:
            print('Fehler Wetterdaten nicht schlimm:', index)
            continue

        wetterstationen += 1
        for jndex in dictModell:
            "Für alle Modelle"
            name = str(dictWeatherID[index]['ID']) + '_' + jndex
            if dictModell[jndex]['AusbauRelv'] == 0:
                WKA_False_Gesamt += 1
                WKA_False_ausbauRele += 1
                continue
            if min_hight >= dictModell[jndex]['Nabenhoehe']:
                WKA_False_Gesamt += 1
                WKA_False_ausbauRele += 1
                continue
            # print(index, jndex)
            leistung = annualOutput_WKA(year, dictModell[jndex]['Ein_ms'], dictModell[jndex]['Nenn_ms'],
                                        dictModell[jndex]['Abs_ms'], dictModell[jndex]['Nenn_kW'],
                                        wetterdaten[matcheswetterdaten[0]], dictModell[jndex]['Nabenhoehe'],
                                        float(dictWeatherID[index]['Messhight']), dictModell[jndex]['Windklasse'],
                                        META_first_wind_limit=META_first_wind_limit,
                                        META_sec_wind_limit=META_sec_wind_limit,
                                        META_third_wind_limit=META_third_wind_limit,
                                        META_first_power_limit=META_first_power_limit,
                                        META_sec_power_limit=META_sec_power_limit,
                                        META_third_power_limit=META_third_power_limit,
                                        use_wind_IEC=True, eisman=eisman)

            leistung_wirk = leistung[0]

            if leistung_wirk == 0:
                WKA_False_wind += 1
                WKA_False_Gesamt += 1
                continue
            WKA_True_Gesamt += 1
            WKA_True += 1
            date_perHoure[name] = leistung_wirk

        print('Wetterstation:', str(dictWeatherID[index]['ID']), 'WKA Erfolgreich: ', WKA_True, '/', WKA_True_Gesamt)
        print('WKA nicht gleaden Gesamt: ', WKA_False_wind + WKA_False_ausbauRele, '/', WKA_False_Gesamt,
              'Davon zu kleine Windklasse: ', WKA_False_wind, 'nicht AusbauRelevant: ', WKA_False_ausbauRele)
    if export == True:
        if eisman == True:
            eisman_name = 'eisman_' + str(META_first_wind_limit) + '_' + str(
                META_sec_wind_limit) + '_' + str(META_third_wind_limit) + '_' + str(
                META_first_power_limit) + '_' + str(META_sec_power_limit) + '_' + str(
                META_third_power_limit)

            openfilename = 'Datenbank/WEAModell/DB_WKA_' + str(year) + '_' + str(min_hight) + '_' + str(
                eisman_name) + '.csv'
        if eisman == False:
            openfilename = 'Datenbank/WEAModell/DB_WKA_' + str(year) + '_' + str(min_hight) + '.csv'

        date_perHoure.to_csv(openfilename, sep=';', encoding='utf-8-sig', index=False, decimal=',')

    return date_perHoure


def negativ_Verlauf(SimuEE_Diff, speicherVerlauf=True):
    # print('Start negativ_Verlauf')
    "Es werden alle Positiven Werte des Verlaufs abgschnitten, sodass nurnoch die ein negativer graph uebrig bleibt"
    # temp_SimuEE_Diff = [0] * len(SimuEE_Diff)

    if speicherVerlauf == True:
        for index, i in enumerate(SimuEE_Diff):
            # Wird für die Mathematische Berechnung benötigt
            if index == 0:
                SimuEE_Diff[index] = 0
                continue
            # Wert kleiner Null ->
            if i + SimuEE_Diff[index - 1] < 0:
                SimuEE_Diff[index] = i + SimuEE_Diff[index - 1]
            if i + SimuEE_Diff[index - 1] > 0:
                SimuEE_Diff[index] = 0

    if speicherVerlauf == False:
        for index, i in enumerate(SimuEE_Diff):
            if i > 0:
                SimuEE_Diff[index] = 0

    return SimuEE_Diff


def percentage_expansion(source_list, percentage):
    temp_sourcelist = source_list * percentage

    return temp_sourcelist.tolist()


def deepest_point_negativGraph(negativGraph, anzahl=100):
    temp_value = anzahl * [0]
    temp_index = anzahl * [0]
    if isinstance(negativGraph, list) == True:
        temp_negativGraph = negativGraph.copy()
    else:
        temp_negativGraph = negativGraph.tolist().copy()

    temp_timesteps = len(temp_negativGraph)

    for jndex, j in enumerate(temp_value):
        temp_value[jndex] = min(temp_negativGraph)
        # print(temp_value[jndex])
        temp_index[jndex] = temp_negativGraph.index(temp_value[jndex])
        temp_negativGraph[temp_index[jndex]] = 0

        if temp_index[jndex] > 31:
            x = temp_index[jndex] - 30
        else:
            x = 1
        if temp_index[jndex] < temp_timesteps - 31:
            y = temp_index[jndex] + 30
        else:
            y = temp_timesteps - 1
        temp_zero = [0] * (y - x)
        temp_negativGraph[x:y] = temp_zero

    # print(temp_value)
    # print(temp_index)

    return temp_value, temp_index


def expansion_storage(temp_Diff_EE, META_speicherverlauf, listStorage, META_startcapacity, META_Laegerdorf,
                      META_compressed_air, META_max_compressed_air, EE_max_Speicher):
    print("start Speicherausbau")
    EE_Simulation_negativGraph = negativ_Verlauf(temp_Diff_EE, speicherVerlauf=META_speicherverlauf)

    deepestPoint = min(EE_Simulation_negativGraph)
    deepestPoint = abs(deepestPoint)
    deepestPoint = deepestPoint
    print('Storage Len: ', len(listStorage))
    print('Benötigte Kapazität in GWh: ', deepestPoint / 1000000)
    if META_Laegerdorf == True:
        storage = StorageModell('PumpspeicherKraftwerk-Lägerdorf', 'Lägerdorf', 1700000, META_startcapacity * 1700000,
                                0.8, 70000, 60.0, 0.08)

        print('PumpspeicherKraftwerk "Lägerdorf" wurde eingerichtet mit:')
        print('Kapazität in GW: ', storage.max_capacity / 1000000, 'Leistung in GW: ', storage.power / 1000000)
        listStorage.append(storage)
        deepestPoint -= 1700000

        print('Storage Len: ', len(listStorage))
        print('Benötigte Kapazität in GWh: ', deepestPoint / 1000000)

    if META_compressed_air == True:
        if deepestPoint > META_max_compressed_air:
            deepestPoint = META_max_compressed_air
        else:
            if EE_max_Speicher != 1:
                deepestPoint = deepestPoint * abs(1-EE_max_Speicher)



        storage = StorageModell('Druckluftspeicher', 'SH', deepestPoint, META_startcapacity * deepestPoint, 0.57,
                                deepestPoint / 5, 60, 0.1)
        print('Druckluftspeicher wurde eingerichtet mit:')
        print('Kapazität in GWh: ', storage.max_capacity / 1000000, 'Leistung in GW: ', storage.power / 1000000)
        listStorage.append(storage)

    elif listStorage[-1].modell == 'Druckluftspeicher':
        old_capacity = listStorage[-1].max_capacity
        old_capacity += 10000000

        if old_capacity > META_max_compressed_air:
            old_capacity = META_max_compressed_air




        listStorage[-1].max_capacity = old_capacity
        listStorage[-1].power = (old_capacity / 5)

        print('Druckspeicher wird erweitert um: ', 5000000/ 1000000,'GWh')
        print('Kapazität in GWh: ', listStorage[-1].max_capacity / 1000000, 'Leistung in GW: ',
              listStorage[-1].power / 1000000)

    # print('Storage Len: ', len(listStorage))

    return

def cost_analysis(year,exportfolder,dictWKA, list_key_expansion_wka, list_count_expansion_wka,
                  list_count_expansion_power, listStorage, cost_wind = True, cost_storage = False, export = True):


    roundnumber = 2
    temp_len_wind = len(list_key_expansion_wka)
    temp_len_storage = len(listStorage)
    temp_len_gesamt = temp_len_wind + temp_len_storage + 1
    cost_model = []

    cost_counter_wka = []

    cost_height = []
    cost_power = []

    cost_single_invest = []
    cost_single_betrieb = []
    cost_invest = []
    cost_betrieb = []
    invest_wka_gesamt = 0
    op_wka_gesamt = 0
    invest_storage_gesamt = 0
    op_storage_gesamt = 0

    if cost_wind == True and temp_len_wind > 0:

        for index, i in enumerate(list_key_expansion_wka):
            print('Wind: ', index)
            temp_name = i.split('_')
            temp_Modell = temp_name[1]
            temp_Modell_hight = temp_name[2]

            if temp_Modell not in cost_model:
                cost_model.append(temp_Modell)
                cost_height.append(float(temp_Modell_hight))
                cost_counter_wka.append(list_count_expansion_wka[index])
                temp_cost = round((dictWKA[temp_Modell + '_' + temp_Modell_hight]['Invest'] / 1000000),
                                                  roundnumber)
                cost_single_invest.append(temp_cost)
                temp_cost = round(
                    (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Betriebk'] / 1000000),
                    roundnumber)
                cost_single_betrieb.append(temp_cost)
                cost_power.append(list_count_expansion_power[index] / 1000)
                temp_invest = round(
                    (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Invest'] * list_count_expansion_wka[index]),
                    roundnumber)
                cost_invest.append(temp_invest / 1000000)
                temp_betrieb = round(
                    (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Betriebk'] * list_count_expansion_wka[index]),
                    roundnumber)
                cost_betrieb.append(temp_betrieb / 1000000)
            else:
                kindex = cost_model.index(temp_Modell)
                if float(temp_Modell_hight) == cost_height[kindex]:
                    cost_counter_wka[kindex] += list_count_expansion_wka[index]
                    temp_cost = round((dictWKA[temp_Modell + '_' + temp_Modell_hight]['Invest'] / 1000000),
                                      roundnumber)
                    cost_single_invest[kindex] += temp_cost
                    temp_cost = round(
                        (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Betriebk'] / 1000000),
                        roundnumber)
                    cost_single_betrieb[kindex] += temp_cost
                    cost_power[kindex] += list_count_expansion_power[index] / 1000
                    temp_invest = round(
                        (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Invest'] * list_count_expansion_wka[index]),
                        roundnumber)
                    cost_invest[kindex] += (temp_invest / 1000000)
                    temp_betrieb = round(
                        (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Betriebk'] * list_count_expansion_wka[index]),
                        roundnumber)
                    cost_betrieb[kindex] += (temp_betrieb / 1000000)
                else:
                    cost_model.append(temp_Modell)
                    cost_height.append(float(temp_Modell_hight))
                    cost_counter_wka.append(list_count_expansion_wka[index])
                    temp_cost = round((dictWKA[temp_Modell + '_' + temp_Modell_hight]['Invest'] / 1000000),
                                      roundnumber)
                    cost_single_invest.append(temp_cost)
                    temp_cost = round(
                        (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Betriebk'] / 1000000),
                        roundnumber)
                    cost_single_betrieb.append(temp_cost)
                    cost_power.append(list_count_expansion_power[index] / 1000)
                    temp_invest = round(
                        (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Invest'] * list_count_expansion_wka[index]),
                        roundnumber)
                    cost_invest.append(temp_invest / 1000000)
                    temp_betrieb = round(
                        (dictWKA[temp_Modell + '_' + temp_Modell_hight]['Betriebk'] * list_count_expansion_wka[index]),
                        roundnumber)
                    cost_betrieb.append(temp_betrieb / 1000000)

        cost_model.append('Summe in Mrd')

        temp_sum = sum(cost_counter_wka)
        cost_counter_wka.append(temp_sum)
        cost_height.append('-')
        temp_sum = sum(cost_power)
        cost_power.append(temp_sum)
        cost_single_invest.append('-')
        cost_single_betrieb.append('-')
        temp_sum = round((sum(cost_invest) / 1000), roundnumber)
        cost_invest.append(temp_sum)
        invest_wka_gesamt =temp_sum
        temp_sum = round((sum(cost_betrieb) / 1000), roundnumber)
        cost_betrieb.append(temp_sum)
        op_wka_gesamt = temp_sum

        export_wka = pd.DataFrame(
            {'Model': cost_model,
             'Number of Models': cost_counter_wka,
             'Model Hub Hight': cost_height,
             'Installed Power in MW': cost_power,
             'Invest in Mio per Model': cost_single_invest,
             'Operating per Year in Mio per Model': cost_single_betrieb,
             'Investment Costs in Mio': cost_invest,
             'Operating Costs per Year in Mio': cost_betrieb
             }
        )


        if export == True:
            exportname2 = exportfolder + 'CostReport_wka_' + str(year) + '.csv'
            export_wka.to_csv(exportname2, index=False, sep=';', encoding='utf-8-sig', decimal=',')

    cost_model = []
    cost_power = []
    cost_capacity = []
    cost_single_invest = []
    cost_single_betrieb = []
    cost_invest = []
    cost_betrieb = []


    if cost_storage == True and temp_len_storage > 0:

        for i in range(len(listStorage)):

            print('Storgae: ',i)

            if listStorage[i].modell not in cost_model:

                cost_model.append(listStorage[i].modell)

                cost_power.append(round((listStorage[i].power/1000), roundnumber))
                cost_capacity.append(round((listStorage[i].max_capacity/1000000), roundnumber))

                cost_single_invest.append(round((listStorage[i].invest), roundnumber))
                cost_single_betrieb.append(round((listStorage[i].operatingk), roundnumber))
                temp_invest = round(((listStorage[i].max_capacity * listStorage[i].invest)/1000000), roundnumber)
                cost_invest.append(temp_invest)
                temp_betrieb = round(((listStorage[i].max_capacity * listStorage[i].operatingk)/1000000), roundnumber)
                cost_betrieb.append(temp_betrieb)


        cost_model.append('Summe in Mrd')
        temp_sum = sum(cost_power)
        cost_power.append(temp_sum)
        temp_sum = sum(cost_capacity)
        cost_capacity.append(temp_sum)
        cost_single_invest.append('-')
        cost_single_betrieb.append('-')
        temp_sum = round((sum(cost_invest) / 1000), roundnumber)
        cost_invest.append(temp_sum)
        invest_storage_gesamt = temp_sum

        temp_sum = round((sum(cost_betrieb) / 1000), roundnumber)
        cost_betrieb.append(temp_sum)
        op_storage_gesamt = temp_sum
        export_storage = pd.DataFrame(
            {'Model': cost_model,
             'Installed Power in MW': cost_power,
             'Installed Capacity in GWh': cost_capacity,
             'Invest in €/kWh per Model': cost_single_invest,
             'Operating in €/kWh per Model': cost_single_betrieb,
             'Investment Costs in Mio': cost_invest,
             'Operatig Costs per Year in Mio': cost_betrieb
             }
        )


        if export == True:
            exportname2 = exportfolder + 'CostReport_storage_' + str(year) + '.csv'
            export_storage.to_csv(exportname2, index=False, sep=';', encoding='utf-8-sig', decimal=',')


    cost_model = []
    cost_invest = []
    cost_betrieb = []

    try:
        cost_model.append('Wind expansion')
        cost_invest.append(invest_wka_gesamt)
        cost_betrieb.append(op_wka_gesamt)
    except:
        print('No Wind was expanded')
        cost_model.append('Wind expansion')
        cost_invest.append(0)
        cost_betrieb.append(0)
    try:
        cost_model.append('Storage expansion')
        cost_invest.append(invest_storage_gesamt)
        cost_betrieb.append(op_storage_gesamt)
    except:
        print('No Storage was expanded')
        cost_model.append('Storage expansion')
        cost_invest.append(0)
        cost_betrieb.append(0)
    try:
        cost_model.append('Summe in Mrd')
        temp_sum = sum(cost_invest)
        cost_invest.append(temp_sum)
        temp_sum = sum(cost_betrieb)
        cost_betrieb.append(temp_sum)
    except:
        print('No Wind and Storage was expanded')


    export_frame = pd.DataFrame(
        {'Modell': cost_model,
         'Investment Costs in Mrd': cost_invest,
         'Operatig Costs per Year in Mrd': cost_betrieb
         }
    )


    if export == True:

        exportname2 = exportfolder + 'CostReport_gesamt_' + str(year) + '.csv'
        export_frame.to_csv(exportname2, index = False, sep=';', encoding='utf-8-sig', decimal=',')

    return export_frame


def data_report(year,data_frame,exportfolder,name , export= True):

    titel = ['Sum in TWh', 'min in MW', 'max in MW', 'Average in MW', ]

    header = ['Erzeugung_Wind', 'verluste_eisman_wind', 'Erz_geplAusbau_Wind',
              'verluste_eisman_geplanterAusbau',
              'REE_Wind', 'REE_Wind_eisman_verluste','Erzeugung_Wind_Gesamt','verluste_eisman_Gesamt',
              'Erz_PV_Gesamt', 'Erz_Biomasse_Gesamt',
              'Erzeugung_Gesamt', 'Diff_Erz_zu_Verbrauch',
              'Speicherverluste', 'Diff_Erz_zu_Verb_mit_Speicher', 'Verbrauch_Gesamt', 'Verbrauch_HH', 'Verbrauch_SH']

    header_Final = ['Existing Wind', 'Eisman Existing Wind', 'Planned Wind', 'Eisman Planned Wind','Expanded Wind',
                    'Eisman expanded Wind', 'Wind combined', 'Eisman Wind combined', 'PV', 'Biomass',
                    'RE combined', 'Difference', 'Storage loss',
                    'Difference (RE+Storage)',
                    'Consumption combined', 'Consumption HH', 'Consumption SH']

    value_header_Final = 0

    exportFrame = pd.DataFrame(
        {'Titel': titel
         }
    )

    TW = 1000000000
    GW = 1000000
    MW = 1000
    roundnumber = 3
    'Wind bestehend'
    for i in header:
        test = []
        try:
            temp_columname = i

            test.append(float(round((sum(data_frame[temp_columname]) / TW), roundnumber)))
            test.append(float(round((min(data_frame[temp_columname] / MW)), roundnumber)))
            test.append(float(round((max(data_frame[temp_columname]) / MW), roundnumber)))
            temp_average = (sum(data_frame[temp_columname]) / len(data_frame[temp_columname]))
            test.append(float(round((temp_average / MW), roundnumber)))

            exportFrame[header_Final[value_header_Final]] = test
            value_header_Final += 1
        except:
            value_header_Final += 1
            print(i, 'is not a header in Datasheet:', name)

    if export == True:

        exportname2 = exportfolder + 'DataReport_'+ name + '_' + str(year) + '.csv'
        exportFrame.to_csv(exportname2, index = False, sep=';', encoding='utf-8-sig', decimal=',')
        print(exportname2)
    return exportFrame

def month_report(year,data_frame,exportfolder,keyname,EE_Erz,speicher_use = False, export= True):

    header_erz = ['Erzeugung_Wind_Gesamt', 'Erz_PV_Gesamt', 'Erz_Biomasse_Gesamt',
              'Erzeugung_Gesamt', 'verluste_eisman_Gesamt']

    header_final = ['Wind (TWh)', 'PV (TWh)', 'Biomass (TWh)', 'Combined RE (TWh)', 'Eisman loss (TWh)',
                    'Storage feed in (TWh)', 'Storage feed out (TWh)', 'Consumption (TWh)',
                    'Deficit/Conventional (TWh)']
    value_header_final = 0
    speicher = ['Ein(+)-/ Ausspeisung(-)']

    header_verbauch = ['Verbrauch_Gesamt']
    if speicher_use == True:
        header_verbauch.append('Diff_Erz_zu_Verb_mit_Speicher')
    else:
        header_verbauch.append('Diff_Erz_zu_Verbrauch')

    ee_100 = 'EE>100%'
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December', 'Year']
    TW = 1000000000
    GW = 1000000
    MW = 1000

    export_frame = pd.DataFrame(
        {'Month': month_name
         }
    )
    # workflow for header ERZ
    MessDateType = '%d.%m.%Y %H:%M'
    data_frame['Datum'] = pd.to_datetime(data_frame['Datum'])

    for j in header_erz:

        temp_values = [0] * 13
        try:
            for index, i in enumerate(months):


                for kndex, k in enumerate(data_frame['Datum']):

                    if k.month == i:
                        temp_values[index] = temp_values[index] + (data_frame[j][kndex]/TW)

            print(j, ' Found and in Dataframe')
            temp_sum = sum(temp_values)
            temp_values[12] = temp_sum
            export_frame[header_final[value_header_final]] = temp_values
            value_header_final += 1
        except:
            value_header_final += 1
            print(j, 'not found')
            continue


    #workflow for storage

    for j in speicher:

        temp_values_positiv = [0] * 13
        temp_values_negativ = [0] * 13
        try:
            for index, i in enumerate(months):

                for kndex, k in enumerate(data_frame['Datum']):

                    if k.month == i:
                        if data_frame[j][kndex] > 0:
                            temp_values_positiv[index] = temp_values_positiv[index] + (data_frame[j][kndex]/TW)
                        else:
                            temp_values_negativ[index] = temp_values_negativ[index] + abs((data_frame[j][kndex]/TW))

            temp_sum = sum(temp_values_positiv)
            temp_values_positiv[12] = temp_sum
            temp_sum = sum(temp_values_negativ)
            temp_values_negativ[12] = temp_sum
            print(j, ' Found and in Dataframe')
            export_frame[header_final[value_header_final]] = temp_values_positiv
            value_header_final += 1

            export_frame[header_final[value_header_final]] = temp_values_negativ
            value_header_final += 1
        except:
            value_header_final += 1
            value_header_final += 1
            print(j, 'not found')
            continue

    # workflow for header_verbauch

    for j in header_verbauch:

        temp_values = [0] * 13
        try:
            for index, i in enumerate(months):


                for kndex, k in enumerate(data_frame['Datum']):

                    if k.month == i:
                        if j == 'Diff_Erz_zu_Verbrauch' or j == 'Diff_Erz_zu_Verb_mit_Speicher':
                            if data_frame[j][kndex] < 0:
                                temp_values[index] = temp_values[index] + abs((data_frame[j][kndex]/TW))

                        else:
                            # print(data_frame['Datum'][kndex])
                            temp_values[index] = temp_values[index] + (data_frame[j][kndex]/TW)




            temp_sum = sum(temp_values)
            temp_values[12] = abs(temp_sum)
            print(j, ' Found and in Dataframe')
            export_frame[header_final[value_header_final]] = temp_values
            value_header_final += 1
        except:
            print(j, 'not found')
            continue

    #workflow for EE Enteil in Prozent

    temp_values = [0] * 13
    temp_conter_day_per_month = [0] * 13
    for index, i in enumerate(months):

        for kndex, k in enumerate(data_frame['Datum']):

            if k.month == i:
                temp_conter_day_per_month[index] = temp_conter_day_per_month[index] + 1
                if data_frame[ee_100][kndex] == True:

                    temp_values[index] = temp_values[index] + 1




    # workflow for EE Enteil in Prozent
    temp_values_over_border = ['test'] * 13

    for index, i in enumerate(months):

        temp_percent = temp_values[index] / temp_conter_day_per_month[index]
        if temp_percent >= EE_Erz:
            temp_values_over_border[index] = 'yes'
        else:
            temp_values_over_border[index] = 'no'



    temp_sum = sum(temp_values)
    temp_values[12] = temp_sum
    export_frame['Hours 100%'] = temp_values
    temp_sum2 = temp_sum/sum(temp_conter_day_per_month)

    if temp_sum2 >= EE_Erz:
        temp_sum2 = temp_sum2 * 100
        temp_sum2 = round(temp_sum2, 2)
        name = str('yes (' + str(temp_sum2) + '%)')
        temp_values_over_border[12] = name
    else:
        temp_sum2 = temp_sum2 * 100
        temp_sum2 = round(temp_sum2, 2)
        name = str('no (' + str(temp_sum2) + '%)')
        temp_values_over_border[12] = name

    export_frame[str(int(EE_Erz*100)) + '% reached'] = temp_values_over_border

    export_frame = export_frame.round(3)

    if export == True:

        exportname2 = exportfolder + 'monthReport_'+ keyname + '_' + str(year) + '.csv'
        export_frame.to_csv(exportname2, index = False, sep=';', encoding='utf-8-sig', decimal=',')
        print(exportname2)

    return export_frame






