import pandas as pd
import numpy as np
from database import findoutFiles
"""Erzeugt ein DataFrame oder eine Liste mit fortlaufenden Datum+Uhrzeit"""
from database import dateList_dataFrame as DateList
import time
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


def erzeugungsdatenEEAnlagen(year, source , state):

    exportFrame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00','60min')


    filelist = findoutFiles('Datenbank\ConnectwithID\Erzeugung')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(year) in match]
    print(matchfilelist3)
    print('Hello')

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
            headerlistLokation = ['TYP', 'Modell', 'Wetter-ID','LEISTUNG' ]
            openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matchfilelist3[0]
            print(openfilename1)

            lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal='.',
                                         header=0, encoding='latin1')

            lengthLocation = lokationsdaten.__len__()
            lengthLocation2 = lengthLocation
            #print(lokationsdaten)
        except ValueError:
            print("falsches Format")

        peter = WEAmodellDictionary_Class()
        dictModell = peter.getdict()


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
                wetterIDunbekannt += 1
                continue

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


            for k in wetterdaten[matcheswetterdaten[0]]:

                #Fehler raus suchen
                if k < 0:
                    leistung.append(int(0))

                # unter Nennleistung
                elif k >= Ein_ms and k < Nenn_ms:
                    x = (lokationsdaten['LEISTUNG'][i] / (Nenn_ms)) * k

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

            #print('Eintrag bei ', i)

            exportFrame[columnName] = leistung



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
            print(df)
        if i > 0:
            del df2['Datum']
            #df.merge(right=df2, left_index=True, right_on='Datum')
            df = pd.concat([df, df2], axis=1, sort=False)
            sum_1 = df.sum(axis=1, numeric_only=None)
            print(sum_1)


    del df['Datum']
    sum_3 = df.sum(axis=1, numeric_only=None)

    print(sum_3)
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

def verbrauchGesamt(year):

    files = findoutFiles('Datenbank\Verbrauch\Einzeln')

    matches = [match for match in files if str(year) in match]

    Datumabgleich = DateList('01.01.' + str(year) + ' 00:00',
                             '31.12.' + str(year) + ' 23:00', '60min', list=True)

    try:
        openfilename = 'Datenbank\Verbrauch\Einzeln/' + matches[0]
        print(openfilename)
        df = pd.read_csv(openfilename, encoding='latin1' ,delimiter=';', decimal=',', header=0)
        print(df.index)
    except:
        print('FEHLER')

    del df['Datum']

    sum_G = df.sum(axis=1, numeric_only=None)
    sum_HH = df['HH_NETZ_Hamburg']
    del df['HH_NETZ_Hamburg']
    sum_SH = df.sum(axis=1, numeric_only=None)
    lentghSum_3 = len(sum_G)
    print(sum_G)

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

    return AusgabeFrame

def analyseEE(year, EE_Erz, verbrauch):

    del verbrauch['Datum']
    #print(FrameVerbrauch)
    #print(FrameErzeung)
    EE_Erz['Erzeugung_Gesamt'] = EE_Erz['Erzeugung_Wind'] + EE_Erz['Erzeugung_PV']
    EE_Erz['Diff_EE_zu_Verb'] = EE_Erz['Erzeugung_Gesamt'] - verbrauch['Verbrauch_Gesamt']
    EE_Erz['Verbrauch_Gesamt'] = verbrauch['Verbrauch_HH'] + verbrauch['Verbrauch_SH']

    EE_Erz['Verbrauch_HH'] = verbrauch['Verbrauch_HH']
    EE_Erz['Verbrauch_SH'] = verbrauch['Verbrauch_SH']
    print(EE_Erz)

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

    print(EE_Erz)
    exportname = "GruenEnergie_" + str(year) + ".csv"
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
        print(lokdaten)
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

def Windlastprofil(year, source):
    print("Start WindLastProfil")
    schritt = 1
    try:
        openfilename2 = 'Datenbank\Wetter/'+ source +'_Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)
        #print(wetterdaten)
    except ValueError:
        print("falsches Format")

    mWd = [match for match in wetterdaten.columns.values.tolist() if
                          str('m/s') in match]
    mwd = [match for match in mWd if
                          str('19171') in match]
    WindAnalyseSchritte = []

    for i in range(29):
        WindAnalyseSchritte.append(i)
        #WindAnalyseSchritte.append(i+schritt)

    del WindAnalyseSchritte[0:1]

    AnalyseProfilbz = []
    for i in WindAnalyseSchritte:
        AnalyseProfilbz.append('von_'+str(i-schritt)+'_bis_'+str(i)+'_ms')

    print(WindAnalyseSchritte)
    print(AnalyseProfilbz)


    'Header Names für die Auswertung'
    exportFrame = pd.DataFrame(
        {'AnalyseProfil': AnalyseProfilbz
         }
    )

    print(mWd)

    for i in range(len(mWd)):
        listparameter = [0] * len(WindAnalyseSchritte)
        #print(wetterdaten[mWd[i]])

        for j in wetterdaten[mWd[i]]:

            for index, k in enumerate(WindAnalyseSchritte):
                #print(float(j), float(k))
                if float(k)-schritt < float(j) and float(k) >= float(j):
                    listparameter[index] += 1

                    #print(listparameter[index])

        exportFrame[mWd[i]] = listparameter
    exportFrame.set_index('AnalyseProfil', inplace=True)
    print(exportFrame)
    exportFrame2 = exportFrame.T
    print(exportFrame2)
    #exportFrame2.loc['AnalyseProfil',:] = AnalyseProfilbz

    exportname2 = 'Datenbank\Wetter\WindAnalyse/Windanlyse_' + str(year) + '.csv'
    exportFrame2.to_csv(exportname2, sep=';', encoding='utf-8', index=True , decimal=',')

    print('Ende')
    return exportname2

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

def stand_distance_analyse(year, standorte):
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
    testTuple = ('0', '0')
    faktorAusbaufl = 1.1
    listnames = []
    p = 1
    for qindex, i in enumerate(standorte['ID']):
        temp_ausbau = geo.editCoords(standorte['Coords Vor'][qindex])

        if temp_ausbau != testTuple and standorte['WKAVor'][qindex] == 'WKA in Betrieb':
            p += 1
            listnames.append(i)

    listFl = [0] * len(listnames)
    anzahl = [0] * len(listnames)
    standortindex = 0
    for index, i in enumerate(standorte['Coords Vor']):

        temp_ausbau = geo.editCoords(i)
        if temp_ausbau != testTuple and standorte['WKAVor'][index] == 'WKA in Betrieb':

            for kindex, j in enumerate(WKA['Coords UTM']):

                temp_wka = geo.editCoords(j)
                distance = geo.distance(temp_wka, temp_ausbau)

                if distance <= faktorAusbaufl:
                    listFl[standortindex] = listFl[standortindex] + ((15 * np.square(float(WKA['ROTORDURCHMESSER'][kindex])))/10000 )
                    anzahl[standortindex] += 1

            listFl[standortindex] = round(listFl[standortindex], 3)
            listFl[standortindex] = float(listFl[standortindex])
            standortindex +=1





    print(listFl)

    # del exportFrame['Datum']
    # print(exportFrame)

    exportFrame = pd.DataFrame(np.c_[listnames, listFl, anzahl], columns=['ID', 'Fläche in ha', 'Anzahl WEAs'])
    #exportFrame.insert(loc=0, column='Typ', value=WKA['TYP'])
    finished_filename = 'Datenbank\Ausbauflaechen/VerbauteFlaechen_radius_'+str(faktorAusbaufl)+'_'+str(year)+'.csv'

    exportFrame.to_csv(finished_filename, sep=';',decimal=',', index=False, encoding='utf-8-sig')

    return exportFrame

def freie_ha_vor(year, standorte, belgegteha):
    print('Start freie_ha_pot')

    print(standorte)
    print(belgegteha)

    temp_freiVor = []
    temp_belegtVor = []
    for index, i in enumerate(standorte['haVor']):
        x = 0
        y = 0
        for kindex, j in enumerate(belgegteha['Fläche in ha']):

            if belgegteha['ID'][kindex] == standorte['ID'][index]:
                print(belgegteha['ID'][kindex], standorte['ID'][index])
                print(i, j)
                x = (float(i)-float(j))
                y = float(j)
        print(standorte['haVor'][index], standorte['WKAVor'][index] )
        if standorte['haVor'][index] > 0 and standorte['WKAVor'][index] == '-':
            x = standorte['haVor'][index]

        temp_freiVor.append(x)
        temp_belegtVor.append(y)
    print(temp_freiVor)
    standorte['besetze Fläche'] = temp_belegtVor
    standorte['freieVor in ha'] = temp_freiVor

    # exportFrame.insert(loc=0, column='Typ', value=WKA['TYP'])
    finished_filename = 'KurzAnschauen_'+str(year)+'.csv'

    standorte.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')
    print(standorte)
    return standorte


    print('Ende freie_ha_pot')

def freie_leistung_Vor(year, standort):
    print('Start freie_leistung_Vor')
    WeaModell_fl_name = 'Enercon E-126/3500'
    WeaModell_fl_leistung = 3500
    WeaModell_fl = ((15 * np.square(float(127)))/10000)
    temp_anzahl = []
    temp_leistung = []
    temp_fl = []

    for index, i in enumerate(standort['freieVor in ha']):

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
    print(EE_Analyse)
    b = EE_Analyse.sort_values(by=['Diff_EE_zu_Verb'], ascending=False)
    qindex = int(8760 * 0.75)
    value = 0
    for index, i in enumerate(b['Diff_EE_zu_Verb']):
        if index == qindex:
            value= i

    #b.to_csv('kurzzz.csv', sep=';',decimal=',', index=False, encoding='utf-8-sig')
    #print(b['Diff_EE_zu_Verb'][qindex])
    #print(b)
    print('Ende Anlyse Ausbau')

    return value

def leistung_im_Jahr(year, Windlastprofil, standorte, value):


    if value > 0:
        print('hallo')








