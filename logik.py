import time

import numpy
import pandas as pd
import numpy as np

from database import findoutFiles
"""Erzeugt ein DataFrame oder eine Liste mit fortlaufenden Datum+Uhrzeit"""
from database import dateList_dataFrame as DateList
from datetime import datetime
from geopy import distance
import geo


class WKAmodell:

    def __init__(self, Modell, Ein_ms, Nenn_ms, Abs_ms, Nenn_kW):

        self.modellName = Modell
        self.Ein_ms = Ein_ms
        self.Nenn_ms = Nenn_ms
        self.Abs_ms = Abs_ms
        self.Nenn_kW = Nenn_kW
        self.__dict = self.filldict()



    def filldict(self):
        temp_dict = {}
        for index, i in enumerate(self.modellName):
            temp_dict[i] = {'Ein_ms': self.Ein_ms[index], 'Nenn_ms': self.Nenn_ms[index],
                            'Abs_ms': self.Abs_ms[index], 'Nenn_kW': self.Nenn_kW[index]}
            #print(temp_dict)

        return temp_dict

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
                print(key + ':' , p_info[key])

class WetterStation:

    def __init__(self,ID ,NameORT, state, Messhight):

        self.NameORT = NameORT
        self.ID = ID
        self.Messhight = Messhight
        self.state = state
        self.__dict = self.filldict()

    def filldict(self):
        temp_dict = {}
        for index, i in enumerate(self.ID):
            temp_dict[i] = {'NameORT': self.NameORT[index], 'ID': self.ID[index],
                            'Messhight': self.Messhight[index], 'state': self.state[index]}
            #print(temp_dict)

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
                print(key + ':' , p_info[key])

def wind_hochrechnung(wind, naben_hight, mess_hight):

    hellmann_konst = 0.25
    delte_hight = naben_hight/mess_hight
    wind = wind * (delte_hight ** hellmann_konst)
    return wind

def WEAmodellDictionary():
    try:
        headerlistModell = ['Modell', 'Einschaltgeschwindigkeit m/s', 'Nenngeschwindigkeit m/s',
                            'Abschaltgeschwindigkeit m/s']
        openfilename3 = 'Datenbank\WEAModell/WEAModell.csv'
        #print(openfilename3)
        df = pd.read_csv(openfilename3, usecols=headerlistModell, delimiter=';', decimal=',', header=0,
                                  encoding='latin1')
        #print(df)
    except ValueError:
        print("falsches Format")

    #Erstellen des Dictionary
    dict = {}

    modell = df['Modell'].tolist()
    Ein_ms = df['Einschaltgeschwindigkeit m/s'].tolist()
    Nenn_ms = df['Nenngeschwindigkeit m/s'].tolist()
    Abs_ms = df['Abschaltgeschwindigkeit m/s'].tolist()


    for index, i in enumerate(modell):
        dict[modell[index]] = [Ein_ms[index], Nenn_ms[index], Abs_ms[index]]

    return dict

def WEAmodellDictionary_Class():
    try:
        headerlistModell = ['Modell','Leistung', 'Einschaltgeschwindigkeit m/s', 'Nenngeschwindigkeit m/s',
                            'Abschaltgeschwindigkeit m/s']
        openfilename3 = 'Datenbank\WEAModell/WEAModell.csv'
        print(openfilename3)
        df = pd.read_csv(openfilename3, usecols=headerlistModell, delimiter=';', decimal=',', header=0,
                                  encoding='latin1')
        print(df)
    except ValueError:
        print("falsches Format")

    #Erstellen des Dictionary


    for i in range(len(df['Modell'])):
        if isinstance(df['Modell'][i], str) == False:
            df['Modell'][i] = "unbekannt"
        if isinstance(df['Einschaltgeschwindigkeit m/s'][i], float) == False and isinstance(df['Einschaltgeschwindigkeit m/s'][i], int) == False:
            print(isinstance(df['Einschaltgeschwindigkeit m/s'][i], float))
            print(df['Einschaltgeschwindigkeit m/s'][i])
            print(type(df['Einschaltgeschwindigkeit m/s'][i]))
            df['Einschaltgeschwindigkeit m/s'][i] = 3
        if isinstance(df['Nenngeschwindigkeit m/s'][i], float) == False and isinstance(df['Nenngeschwindigkeit m/s'][i], int) == False:
            df['Nenngeschwindigkeit m/s'][i] = 13
        if isinstance(df['Abschaltgeschwindigkeit m/s'][i], float) == False and isinstance(df['Abschaltgeschwindigkeit m/s'][i], int) == False:
            df['Abschaltgeschwindigkeit m/s'][i] = 25
        if isinstance(df['Leistung'][i], float) == False and isinstance(df['Leistung'][i], int) == False:
            df['Leistung'][i] = int(1500)

    Modell = df['Modell'].tolist()
    Ein_ms = df['Einschaltgeschwindigkeit m/s'].tolist()
    Nenn_ms = df['Nenngeschwindigkeit m/s'].tolist()
    Abs_ms = df['Abschaltgeschwindigkeit m/s'].tolist()
    P_kw = df['Leistung'].tolist()

    peter = WKAmodell(Modell, Ein_ms, Nenn_ms, Abs_ms, P_kw)
   #WKAmodell(k, Ein_ms[index], Nenn_ms[index], Abs_ms[index], P_kw[index])

    return peter

def WeatherStationDictionary_Class():
    try:
        headerlistModell = ['Stations_id','Messhoehe', 'Stationsname', 'Bundesland']
        openfilename3 = 'Import\Wetterstationen/StundeWindStationen.csv'
        print(openfilename3)
        df = pd.read_csv(openfilename3, usecols=headerlistModell, delimiter=';', decimal=',', header=0,
                                  encoding='latin1')
        print(df)
    except ValueError:
        print("falsches Format")

    #Erstellen des Dictionary


    for i in range(len(df['Stations_id'])):
        if isinstance(df['Messhoehe'][i], float) == False and isinstance(df['Messhoehe'][i], int) == False:
            df['Messhoehe'][i] = 9999
        if isinstance(df['Stations_id'][i], float) == False and isinstance(df['Stations_id'][i], numpy.int64) == False:
            print(type(df['Stations_id'][i]))
            print(isinstance(df['Stations_id'][i], float))
            print(isinstance(df['Stations_id'][i], int))
            df['Stations_id'][i] = '0'
        if isinstance(df['Stationsname'][i], str) == False:
            df['Stationsname'][i] = "unbekannt"
        if isinstance(df['Bundesland'][i], str) == False:
            df['Bundesland'][i] = "unbekannt"


    Stations_id = df['Stations_id'].tolist()
    Messhoehe = df['Messhoehe'].tolist()
    Stationsname = df['Stationsname'].tolist()
    Bundesland = df['Bundesland'].tolist()

    #print(Stations_id, Stationsname, Bundesland, Messhoehe)

    peter = WetterStation(Stations_id,Stationsname,Bundesland,Messhoehe )
   #WKAmodell(k, Ein_ms[index], Nenn_ms[index], Abs_ms[index], P_kw[index])

    return peter

def erzeugungsdatenEEAnlagen(year, source, state ):

    exportFrame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00','60min')


    filelist = findoutFiles('Datenbank\ConnectwithID\Erzeugung')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(year) in match]
    print(matchfilelist3)


    try:
        openfilename2 = 'Datenbank\Wetter/'+ source +'_Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)
        #print(wetterdaten)
    except ValueError:
        print("falsches Format")

    modellunbekannt = 0
    wetterIDunbekannt = 0
    lengthLocation2 = 0
    if source == 'Wind':
        try:
            headerlistLokation = ['TYP', 'Modell', 'Wetter-ID','LEISTUNG', 'NABENHOEHE' ]
            openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matchfilelist3[0]
            print(openfilename1)

            lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal='.',
                                         header=0, encoding='latin1')

            lengthLocation = lokationsdaten.__len__()
            lengthLocation2 = lengthLocation
            #print(lokationsdaten)
        except ValueError:
            print("falsches Format")
        '------------------------------------------------------------------------------------------------------'
        temp_wea = WEAmodellDictionary_Class()
        dictModell = temp_wea.getdict()
        temp_WeatherID = WeatherStationDictionary_Class()
        dictWeatherID = temp_WeatherID.getdict()


        for i in range(lengthLocation):

            leistung = []
            WKAunbekannt = False
            #print(str(lokationsdaten['Wetter-ID'][i]))

            matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                  str(lokationsdaten['Wetter-ID'][i]) in match]
            #print(matcheswetterdaten)
            if len(matcheswetterdaten) != 2:
                print('Fehler Wetterdaten nicht schlimm')
                print(lokationsdaten['Wetter-ID'][i])
                lokationsdaten['Wetter-ID'][i] = 3086
                matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                      str(lokationsdaten['Wetter-ID'][i]) in match]
                wetterIDunbekannt += 1


            columnName = str(i) + '_Ezg_' + str(lokationsdaten['TYP'][i]) + '_' + str(
                lokationsdaten['Modell'][i]) + '_' + str(lokationsdaten['Wetter-ID'][i])

            try:
                Ein_ms = dictModell[lokationsdaten['Modell'][i]]['Ein_ms']
            except:
                Ein_ms = 3
                #print("Modell unbekannt")
                WKAunbekannt = True
            try:
                Nenn_ms = dictModell[lokationsdaten['Modell'][i]]['Nenn_ms']
            except:
                Nenn_ms = 13
                #print("Modell unbekannt")
                WKAunbekannt = True
            try:
                Abs_ms = dictModell[lokationsdaten['Modell'][i]]['Abs_ms']
            except:
                Abs_ms = 25
                WKAunbekannt = True

            if WKAunbekannt == True:
                #print("Modell unbekannt")
                modellunbekannt += 1

            if isinstance(lokationsdaten['LEISTUNG'][i], float) == False and isinstance(
                    lokationsdaten['LEISTUNG'][i], numpy.int64) == False:

                lokationsdaten['LEISTUNG'][i] = 1000
                print('Fehler Leistungsdaten nicht schlimm')
                print(columnName)


            temp_wetter = wetterdaten[matcheswetterdaten[0]]

            temp_wetter = wind_hochrechnung(wetterdaten[matcheswetterdaten[0]], lokationsdaten['NABENHOEHE'][i],
                                            dictWeatherID[lokationsdaten['Wetter-ID'][i]]['Messhight'])
            for qindex, k in enumerate(temp_wetter):


                #Fehler raus suchen
                if k < 0:
                    leistung.append(int(0))

                # unter Nennleistung
                elif k >= Ein_ms and k < Nenn_ms:
                    x = FORMEL_WKA_Leistung(Nenn_ms, Ein_ms, lokationsdaten['LEISTUNG'][i], k)
                    #print('moment_ms',k ,'Leistung', lokationsdaten['LEISTUNG'][i], 'Erzeigung', x )
                    #print(k ,lokationsdaten['LEISTUNG'][i], x)
                    leistung.append(int(x))
                # ueber nennleistung
                elif k >= Nenn_ms and k < Abs_ms:
                    leistung.append(int(lokationsdaten['LEISTUNG'][i]))

                # außerhalb der Betriebsgeschwindigekeit
                elif k >= Abs_ms or k < Ein_ms:
                    leistung.append(int(0))


                else:
                    print("Fehler")
                    leistung.append(int(0))

                if qindex == 7765:
                    print(k, wetterdaten['Datum'][qindex], leistung[-1])

            #print('Eintrag bei ', i)

            exportFrame[columnName] = leistung
            print(columnName)

    '-----------------------------------------------------------------------------------------------------------'

    if source == 'PV':
        try:
            headerlistLokation = ['Leistung','Bundesland', 'Wetter-ID']
            openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matchfilelist3[0]
            print(openfilename1)

            lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal=',',
                                         header=0, encoding='latin1')

            lengthLocation = lokationsdaten.__len__()
            #print(lokationsdaten)
        except ValueError:
            print("falsches Format")

        for i in range(lengthLocation):
            leistung = []
            #print(i)
            #print(str(lokationsdaten['Wetter-ID'][i]))

            matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                  str(lokationsdaten['Wetter-ID'][i]) in match]
            #print(matcheswetterdaten)
            if len(matcheswetterdaten) != 2:
                print('Fehler Wetterdaten')
                break


            columnName = str(i) + '_Ezg_PV' + '_'+str(lokationsdaten['Bundesland'][i])+ '_'+ str(lokationsdaten['Wetter-ID'][i])

            fkt_Bestrahlung = 492.48
            fkt_Solar = 0.9

            for k in wetterdaten[matcheswetterdaten[0]]:

                if k < 0:
                    leistung.append(0)
                else:
                    #print(lokationsdaten['Bruttoleistung der Einheit'][i])
                    #print(type(lokationsdaten['Bruttoleistung der Einheit'][i]))
                    x = lokationsdaten['Leistung'][i] * (k/fkt_Bestrahlung)*fkt_Solar
                    leistung.append(x)

            #print('Eintrag bei ', i)
            exportFrame[columnName] = leistung
            #print('Eintrag Efolgreich ', i)


    #print(exportFrame)
    exportname = 'Datenbank\Erzeugung\Einzel/Erz_'+ source +'_' + state +'_' + str(year) + '.csv'
    exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')
    print("Modell ungekannt Anzahl: ", modellunbekannt)
    print("Wetter-ID ungekannt Anzahl: ", wetterIDunbekannt)
    print("Eingelesene Zeilen", lengthLocation2)
    print("Ausgegebene Zeilen", len(exportFrame.columns))

    print('Fertig')

def erzeugungEEAnlage_singleFrame(wetterdaten, lokationsdaten,year, export = False):

    exportFrame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', '60min')
    temp_wea = WEAmodellDictionary_Class()
    dictModell = temp_wea.getdict()
    temp_WeatherID = WeatherStationDictionary_Class()
    dictWeatherID = temp_WeatherID.getdict()


    for i in range(len(lokationsdaten)):


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

            #wetterIDunbekannt += 1

        columnName = str(i) + '_Ezg_' + str(lokationsdaten['TYP'][i]) + '_' + str(
            lokationsdaten['Modell'][i]) + '_' + str(lokationsdaten['Wetter-ID'][i])

        try:
            Ein_ms = dictModell[lokationsdaten['Modell'][i]]['Ein_ms']
        except:
            Ein_ms = 3
            # print("Modell unbekannt")
            WKAunbekannt = True
        try:
            Nenn_ms = dictModell[lokationsdaten['Modell'][i]]['Nenn_ms']
        except:
            Nenn_ms = 13
            # print("Modell unbekannt")
            WKAunbekannt = True
        try:
            Abs_ms = dictModell[lokationsdaten['Modell'][i]]['Abs_ms']
        except:
            Abs_ms = 25
            WKAunbekannt = True

        if WKAunbekannt == True:
            print("Modell unbekannt")
            #modellunbekannt += 1

        if isinstance(lokationsdaten['LEISTUNG'][i], float) == False and isinstance(
                lokationsdaten['LEISTUNG'][i], numpy.int64) == False:
            lokationsdaten['LEISTUNG'][i] = 1000
            print('Fehler Leistungsdaten nicht schlimm')
            print(columnName)

        #temp_wetter = wetterdaten[matcheswetterdaten[0]]

        temp_wetter = wind_hochrechnung(wetterdaten[matcheswetterdaten[0]], float(lokationsdaten['NABENHOEHE'][i]),
                                        dictWeatherID[lokationsdaten['Wetter-ID'][i]]['Messhight'])
        temp_leistung = [0] * len(temp_wetter)

        for qindex, k in enumerate(temp_wetter):

            # Fehler raus suchen
            if k < 0:
                temp_leistung[qindex] = 0

            # unter Nennleistung
            elif k >= Ein_ms and k < Nenn_ms:
                x = FORMEL_WKA_Leistung(Nenn_ms, Ein_ms, lokationsdaten['LEISTUNG'][i], k)
                # print('moment_ms',k ,'Leistung', lokationsdaten['LEISTUNG'][i], 'Erzeigung', x )
                # print(k ,lokationsdaten['LEISTUNG'][i], x)
                temp_leistung[qindex] = int(x)
            # ueber nennleistung
            elif k >= Nenn_ms and k < Abs_ms:
                temp_leistung[qindex] = int(lokationsdaten['LEISTUNG'][i])

            # außerhalb der Betriebsgeschwindigekeit
            elif k >= Abs_ms or k < Ein_ms:
                temp_leistung[qindex] = 0


            else:
                print("Fehler")
                temp_leistung[k] = 0



        # print('Eintrag bei ', i)

        exportFrame[columnName] = temp_leistung
        print(columnName)
    if export == True:
        exportname = 'Datenbank\Erzeugung\Erz_geplanterAusbau/Erz_geplanterAusbau_' + str(year) + '.csv'
        exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    return exportFrame

def erzeugungPerStunde(year, source1):

    print("Start Erzeugung per Stunde")

    files = findoutFiles('Datenbank\Erzeugung/Einzel')

    matches = [match for match in files if str(year) in match]
    matches = [match for match in matches if str(source1) in match]

    Datumabgleich = DateList('01.01.' + str(year)+ ' 00:00',
                                        '31.12.' + str(year) + ' 23:00', '60min', list=True)
    lengthmachtes = matches.__len__()


    for i in range(lengthmachtes):
        try:
            openfilename2 = 'Datenbank\Erzeugung/Einzel/' + matches[i]
            print(openfilename2)
            df2 = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)

        except:
            print('FEHLER')

        if i == 0:
            df = df2.copy()
            #print(df)
        if i > 0:
            del df2['Datum']
            #df.merge(right=df2, left_index=True, right_on='Datum')
            df = pd.concat([df, df2], axis=1, sort=False)
            sum_1 = df.sum(axis=1, numeric_only=None)
            #print(sum_1)


    del df['Datum']
    sum_3 = df.sum(axis=1, numeric_only=None)

    #print(sum_3)
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

    exportname = 'Datenbank\Erzeugung/Erz_komuliert_' + str(year) +'_'+ source1 +'.csv'
    AusgabeFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    return AusgabeFrame

def erzeugungPerStunde_singleFrame(year, ErzeugungFrame, export = False):

    print("Start Erzeugung per Stunde")

    Datumabgleich = DateList('01.01.' + str(year)+ ' 00:00',
                                        '31.12.' + str(year) + ' 23:00', '60min', list=True)

    del ErzeugungFrame['Datum']
    sum_3 = ErzeugungFrame.sum(axis=1, numeric_only=None)

    #print(sum_3)
    lengthDatum = len(Datumabgleich)
    lentghSum_3 = len(sum_3)
    if lengthDatum != lentghSum_3:
        print('FEHLER')

    Erz_Name = 'Erzeugung_geplanterAusbau_' + str('Wind')
    AusgabeFrame = pd.DataFrame(
        {
            'Datum': Datumabgleich,
            Erz_Name: sum_3
        }
    )
    if export == True:
        exportname = 'Datenbank\Erzeugung/Erz_komuliert_geplanterAusbau_' + str(year) +'_Wind.csv'
        AusgabeFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    return AusgabeFrame

def verbrauchGesamt(year):

    files = findoutFiles('Datenbank\Verbrauch\Einzeln')

    matches = [match for match in files if str(year) in match]

    Datumabgleich = DateList('01.01.' + str(year) + ' 00:00',
                             '31.12.' + str(year) + ' 23:00', '60min', list=True)

    try:
        openfilename = 'Datenbank\Verbrauch\Einzeln/' + matches[0]
        print(openfilename)
        df = pd.read_csv(openfilename, encoding='latin1' ,delimiter=';', decimal=',', header=0)
        #print(df.index)
    except:
        print('FEHLER')

    del df['Datum']

    sum_G = df.sum(axis=1, numeric_only=None)
    sum_HH = df['HH_NETZ_Hamburg']
    del df['HH_NETZ_Hamburg']
    sum_SH = df.sum(axis=1, numeric_only=None)
    lentghSum_3 = len(sum_G)
    #print(sum_G)

    AusgabeFrame = pd.DataFrame(
        {
            'Datum': Datumabgleich,
            'Verbrauch_Gesamt': sum_G,
            'Verbrauch_HH': sum_HH,
            'Verbrauch_SH': sum_SH,
        }
    )

    exportname = "Datenbank\Verbrauch\Verbrauch_komuliert_"+ str(year) + ".csv"
    AusgabeFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')
    print('Fertig')

    return AusgabeFrame

def analyseEE(year, EE_Erz, verbrauch, export= False, geplanterAusbau = True ):

    temp_list = [328000]*len(EE_Erz['Erzeugung_Wind'])
    EE_Erz['Erzeugung_Biogas'] = temp_list
    #print(FrameVerbrauch)
    #print(FrameErzeung)
    if geplanterAusbau == True:
        EE_Erz['Erzeugung_Gesamt'] = EE_Erz['Erzeugung_Wind'] + EE_Erz['Erzeugung_PV'] + EE_Erz[
            'Erzeugung_geplanterAusbau_Wind'] + EE_Erz['Erzeugung_Biogas']
    else:
        EE_Erz['Erzeugung_Gesamt'] = EE_Erz['Erzeugung_Wind'] + EE_Erz['Erzeugung_PV'] + EE_Erz['Erzeugung_Biogas']

    EE_Erz['Diff_EE_zu_Verb'] = EE_Erz['Erzeugung_Gesamt'] - verbrauch['Verbrauch_Gesamt']
    EE_Erz['Verbrauch_Gesamt'] = verbrauch['Verbrauch_HH'] + verbrauch['Verbrauch_SH']

    EE_Erz['Verbrauch_HH'] = verbrauch['Verbrauch_HH']
    EE_Erz['Verbrauch_SH'] = verbrauch['Verbrauch_SH']


    EE_Erz['EE_Anteil'] = EE_Erz['Erzeugung_Gesamt']/verbrauch['Verbrauch_Gesamt']
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
    uhrzeit = datetime.now().strftime('%Y%m%d_%H-%M')

    if export == True:
        exportname = 'GruenEnergie_' + str(year) + '_' + str(uhrzeit) + '.csv'
        print(exportname)
        EE_Erz.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    return EE_Erz

def analyseAusbauFl():
    print('Start mit Analyse')
    filelist = findoutFiles('Datenbank\Ausbauflaechen\AusbauStandorte_gesamt_SH')
    matchfilelist = [match for match in filelist if 'AlleStandorte' in match]
    try:
        openfilename1 = 'Datenbank\Ausbauflaechen\AusbauStandorte_gesamt_SH/' + matchfilelist[0]
        print(openfilename1)

        lokdaten = pd.read_csv(openfilename1, delimiter=';', decimal=',',
                                     header=0, encoding='latin1')

        lengthLokationsdaten = lokdaten.__len__()
        #print(lokdaten)
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

def windlastprofil(year):
    print("Start WindLastProfil")

    try:
        openfilename2 = 'Datenbank\Wetter/Wind_Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)
        #print(wetterdaten)
    except ValueError:
        print("falsches Format")

    mWd = [match for match in wetterdaten.columns.values.tolist() if
                          str('m/s') in match]

    WindAnalyseSchritte = []

    for i in range(36):
        WindAnalyseSchritte.append(i)
        #WindAnalyseSchritte.append(i+schritt)

    del WindAnalyseSchritte[0:1]

    AnalyseProfilbz = []
    for i in WindAnalyseSchritte:
        AnalyseProfilbz.append('von_'+str(i-1)+'_bis_'+str(i)+'_ms')

    #print(WindAnalyseSchritte)
    #print(AnalyseProfilbz)


    'Header Names für die Auswertung'
    exportFrame = pd.DataFrame(
        {'AnalyseProfil': AnalyseProfilbz
         }
    )

    #print(exportFrame)

    for i in range(len(mWd)):

        #print(wetterdaten[mWd[i]])


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
    #print(exportFrame)
    #exportFrame2 = exportFrame.T
    #print(exportFrame2)
    #exportFrame2.loc['AnalyseProfil',:] = AnalyseProfilbz

    exportname2 = 'Datenbank\Wetter\WindAnalyse/Windanlyse_' + str(year) + '.csv'
    exportFrame.to_csv(exportname2, sep=';', encoding='utf-8', index=True , decimal=',')

    print('Ende')
    return exportFrame

def windlastprofil_einzel(windWeatherlist):
    WindAnalyseSchritte = []

    for i in range(36):
        WindAnalyseSchritte.append(i)
        #WindAnalyseSchritte.append(i+schritt)

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
    #print(sum(listparameter))
    return listparameter

def stand_distance_analyse_alt(year,standorte):

    filelist = findoutFiles('Datenbank\ConnectwithID\Erzeugung')
    matches1 = [match for match in filelist if str(year) in match]
    matches1 = [match for match in matches1 if 'SH' in match]
    matches1 = [match for match in matches1 if 'UTM' in match]

    try:
        openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matches1[0]
        print(openfilename1)

        WKA = pd.read_csv(openfilename1, delimiter=';', decimal=',', encoding='latin1')

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
            columnName = str(p)+'_'+ i
            p += 1
            listnames.append(columnName)




    #del exportFrame['Datum']
    #print(exportFrame)

    exportFrame = pd.DataFrame(np.c_[list], columns=listnames)
    exportFrame.insert(loc=0, column='Typ', value=WKA['TYP'])
    finished_filename = 'KurzAnschauen.csv'

    exportFrame.to_csv(finished_filename, sep=';',decimal=',', index=False, encoding='UTF-8')

def stand_distance_analyse(year,Vor_Pot, standorte, faktorAusbaufl, export = True):
    filelist = findoutFiles('Datenbank\ConnectwithID\Erzeugung')
    matches1 = [match for match in filelist if str(year) in match]
    matches1 = [match for match in matches1 if 'SH' in match]
    matches1 = [match for match in matches1 if 'UTM' in match]
    temp_first = False
    for i in matches1:

        try:
            openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + i
            print(openfilename1)

            WKA = pd.read_csv(openfilename1, delimiter=';', decimal=',', encoding='latin1')
            WKA = WKA.fillna(0)

        except:
            print('falsches Format')
        if temp_first == False:
            testTuple = ('0', '0')
            listnames = []
            p = 1
            for qindex, i in enumerate(standorte['ID']):
                temp_ausbau = geo.editCoords(standorte['Coords '+Vor_Pot][qindex])

                if temp_ausbau != testTuple and standorte['WKA'+Vor_Pot][qindex] == 'WKA in Betrieb':
                    p += 1
                    listnames.append(i)

            temp_first = True

            listFl = [0] * len(listnames)
            anzahl = [0] * len(listnames)

        standortindex = 0

        for index, i in enumerate(standorte['Coords '+Vor_Pot]):

            temp_ausbau = geo.editCoords(i)
            if temp_ausbau != testTuple and standorte['WKA'+Vor_Pot][index] == 'WKA in Betrieb':

                for kindex, j in enumerate(WKA['Coords UTM']):

                    temp_wka = geo.editCoords(j)
                    distance = geo.distance(temp_wka, temp_ausbau)

                    if distance <= faktorAusbaufl:
                        listFl[standortindex] += int((15 * np.square(float(WKA['ROTORDURCHMESSER'][kindex]))) / 10000)
                        anzahl[standortindex] += 1

                listFl[standortindex] += round(listFl[standortindex], 3)
                listFl[standortindex] += float(listFl[standortindex])
                standortindex += 1

        print(listFl)


    exportFrame = pd.DataFrame(np.c_[listnames, listFl, anzahl], columns=['ID', 'Flaeche_'+Vor_Pot, 'Anzahl WEAs'])

    if export == True:

        finished_filename = 'Datenbank\Ausbauflaechen/VerbauteFlaechen_radius_'+str(faktorAusbaufl)+'_'+str(year)+'.csv'
        exportFrame.to_csv(finished_filename, sep=';', index=False, decimal=',')

    return exportFrame

def freie_ha_vor(year, standorte, belgegteha_Vor, belgegteha_Pot):
    print('Start freie_ha_Vor')

    #print(standorte)
    #print(belgegteha)

    temp_freiVor = []
    temp_belegtVor = []
    temp_anzahl = []
    for index, i in enumerate(standorte['haVor']):
        x = 0
        y = 0
        z = 0
        for kindex, j in enumerate(belgegteha_Vor['Flaeche_Vor']):

            if belgegteha_Vor['ID'][kindex] == standorte['ID'][index]:
                #print(belgegteha['ID'][kindex], standorte['ID'][index])
                #print(i, j)
                x = (float(i)-float(j))
                y = float(j)
                z = belgegteha_Vor['Anzahl WEAs'][kindex]
        #print(standorte['haVor'][index], standorte['WKAVor'][index] )
        if int(standorte['haVor'][index]) > 0 and standorte['WKAVor'][index] == '-':
            x = standorte['haVor'][index]

        temp_freiVor.append(x)
        temp_belegtVor.append(y)
        temp_anzahl.append(z)
    #print(temp_freiVor)

    standorte['Anzahl WEAs_Vor'] = temp_anzahl
    standorte['besetze Flaeche_Vor'] = temp_belegtVor
    standorte['nettoFreieFlaeche_Vor'] = temp_freiVor

    temp_freiVor = []
    temp_belegtVor = []
    temp_anzahl = []
    for index, i in enumerate(standorte['haPot']):
        x = 0
        y = 0
        z = 0
        for kindex, j in enumerate(belgegteha_Pot['Flaeche_Pot']):

            if belgegteha_Pot['ID'][kindex] == standorte['ID'][index]:
                #print(belgegteha['ID'][kindex], standorte['ID'][index])
                #print(i, j)
                x = (float(i)-float(j))
                y = float(j)
                z = belgegteha_Pot['Anzahl WEAs'][kindex]
        #print(standorte['haVor'][index], standorte['WKAVor'][index] )
        if int(standorte['haPot'][index]) > 0 and standorte['WKAPot'][index] == '-':
            x = standorte['haPot'][index]

        temp_freiVor.append(x)
        temp_belegtVor.append(y)
        temp_anzahl.append(z)
    #print(temp_freiVor)
    standorte['Anzahl WEAs_Pot'] = temp_anzahl
    standorte['besetze Flaeche_Pot'] = temp_belegtVor
    standorte['nettoFreieFlaeche_Pot'] = temp_freiVor


    # exportFrame.insert(loc=0, column='Typ', value=WKA['TYP'])
    finished_filename = 'KurzAnschauen_'+str(year)+'.csv'

    standorte.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')
    #print(standorte)
    return standorte


    print('Ende freie_ha_pot')

def freie_leistung_Vor(year, standort):
    print('Start freie_leistung_Vor')
    WeaModell_fl_name = 'Enercon E-82/3000'
    WeaModell_fl_leistung = 3000
    WeaModell_fl = ((15 * np.square(float(82)))/10000)
    temp_anzahl = []
    temp_leistung = []
    temp_fl = []

    for index, i in enumerate(standort['freieVor in Vor']):

        if i > 0:
            anzahl = i/WeaModell_fl
            leistung = int(anzahl) * WeaModell_fl_leistung
            temp_anzahl.append(int(anzahl))
            temp_leistung.append(leistung)
            temp_fl.append(WeaModell_fl)
        else:
            temp_anzahl.append(0)
            temp_leistung.append(0)
            temp_fl.append(0)

    standort[WeaModell_fl_name] = temp_fl
    standort['temp_anzahl'] = temp_anzahl
    standort['temp_leistung'] = temp_leistung

    print('freie_leistung_pot')
    return standort

def ausbau(year, EE_Analyse, Standort):
    print('Start Analyse Ausbau')
    #print(EE_Analyse)
    trueHours = 0
    for i in EE_Analyse['EE>100%']:
        if i == 'True':
            trueHours += 1


    b = EE_Analyse.sort_values(by=['Diff_EE_zu_Verb'], ascending=False)
    qindex = int(8760 * 0.75)
    value = 0
    if qindex >= trueHours:
        for index, i in enumerate(b['Diff_EE_zu_Verb']):
            if index == qindex:
                value = i

    print(value)

    #b.to_csv('kurzzz.csv', sep=';',decimal=',', index=False, encoding='utf-8-sig')
    #print(b['Diff_EE_zu_Verb'][qindex])
    #print(b)
    print('Ende Anlyse Ausbau')

    return value


def windenergie(standort,standort_main):

    try:
        openfilename1 = 'Datenbank\Wetter/Wind_Wetterdaten_2019.csv'
        #print(openfilename1)

        Wetterdaten = pd.read_csv(openfilename1, delimiter=';', decimal=',',
                                     header=0, encoding='latin1')

        #lengthLokationsdaten = lokdaten.__len__()
        #print(lokdaten)

    except ValueError:
        print("falsches Format")

    #print(Wetterdaten)
    #print(standort)



    name = 'Enercon E-82/3000'
    Ein_ms = 3
    Nenn_ms = 16
    Abs_ms = 34
    leistung_einzel = 3000
    nabenhohe = 82
    weatherID = '1200'
    standortbesetzt = standort_main
    anzahl_2 = 0
    name_2 = ''
    leistung_Gesamt = 123
    temp_leistung = [0] * 8760

    cloumFrame = Wetterdaten.columns.values.tolist()


    for qindex, i in enumerate(standort['temp_anzahl']):
        if i > 0 and qindex > standortbesetzt:
            anzahl_2 = i
            leistung_Gesamt = leistung_einzel * i
            weatherID = str(standort['Wetter-ID_Head'][qindex])
            name_2 = str(standort['ID'][qindex])
            standortbesetzt = qindex
            break
    columnName = str(qindex) + '_Ezg_' + '_' + str(name_2)

    if leistung_Gesamt == 123:
        print('Keine Anlage Verfügbar')
        return temp_leistung, columnName, standortbesetzt, anzahl_2, leistung_Gesamt, name_2

    matchfilelist = [match for match in cloumFrame if weatherID in match]
    lengthlist = len(matchfilelist)

    if lengthlist != 2:
        matchfilelist.append('Wind_m/s_788')

    temp_wetter = Wetterdaten[matchfilelist[0]]
    temp_wetter = wind_hochrechnung(Wetterdaten[matchfilelist[0]], nabenhohe, 10)

    for index, k in enumerate(temp_wetter):

        # Fehler raus suchen
        if k < 0:
            temp_leistung[index] = 0

        # unter Nennleistung
        elif k >= Ein_ms and k < Nenn_ms:
            x = FORMEL_WKA_Leistung(Nenn_ms, Ein_ms, leistung_Gesamt, k)
            temp_leistung[index] = int(x)

        # ueber nennleistung
        elif k >= Nenn_ms and k < Abs_ms:
            temp_leistung[index] = int(leistung_Gesamt)

        # außerhalb der Betriebsgeschwindigekeit
        elif k >= Abs_ms or k < Ein_ms:
            temp_leistung[index] = 0


        else:
            print("Fehler")
            temp_leistung[index] = 0




    return temp_leistung, columnName, standortbesetzt, anzahl_2, leistung_Gesamt, name_2

def FORMEL_WKA_Leistung(nenn_ms, ein_ms , leistung_s, moment_ms):

    a = 5

    vp_WP = ein_ms + ((nenn_ms)/2) + 1
    k = np.log(a/(leistung_s-a))/(leistung_s*vp_WP*(-1))

    temp_p = (a*leistung_s)/(a+(leistung_s-a)*np.exp(leistung_s*k*moment_ms*(-1)))

    return temp_p

def standortquality(year, wetterdaten, WKAanlagen):
    print('Start', year)
    temp_Header = wetterdaten.columns.values.tolist()
    exportFrame = pd.DataFrame(columns=['Name','Jahresleistung', 'ReferenzEnergieErtrag', 'Standortquality'])
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
            #modellunbekannt += 1

        if isinstance(WKAanlagen['LEISTUNG'][i], float) == False and isinstance(
                WKAanlagen['LEISTUNG'][i], numpy.int64) == False:
            WKAanlagen['LEISTUNG'][i] = 1000
            print('Fehler Leistungsdaten nicht schlimm')
        #print(WKAanlagen['NABENHOEHE'])

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
            name = str(WKAanlagen['Modell'][i]+'_'+ str(WKAanlagen['NABENHOEHE'][i]) + '_' + mWd[j])

            temp_name.append(name)
            temp_Jahresleistung.append(temp_leistung)
            #print(WKAanlagen['Referenzertrag [kWh]'][i])
            temp_ReferenzEnergieErtrag.append(WKAanlagen['Referenzertrag [kWh]'][i])
            #print(temp_leistung, WKAanlagen['Referenzertrag [kWh]'][i])
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

























