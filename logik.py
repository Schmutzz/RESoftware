import pandas as pd
from database import findoutFiles
"""Erzeugt ein DataFrame oder eine Liste mit fortlaufenden Datum+Uhrzeit"""
from database import dateList_dataFrame as DateList


class WKAmodell:
    __counter = 0

    def __init__(self, Modell, Ein_ms, Nenn_ms, Abs_ms, Nenn_kW):
        type(self).__counter += 1
        self.modellName = Modell
        self.Ein_ms = Ein_ms
        self.Nenn_ms = Nenn_ms
        self.Abs_ms = Abs_ms
        self.Nenn_kW = Nenn_kW

    def __del__(self):
        type(self).__counter -= 1

    def showItems(self):
        print(self.modellName)
        print(self.Ein_ms)
        print(self.Nenn_ms)
        print(self.Abs_ms)
        print(self.Nenn_kW)
        return 'Siehste'

    def leistung_kw(self, wind_ms):
        'Fehler Winddaten'
        if wind_ms < 0:
            return 0
        'Außerhalb der Betriebs_ms'
        if wind_ms > self.Abs_ms or wind_ms < self.Ein_ms:
            return 0
        'Von Ein_ms bis Nenn_ms'
        if wind_ms >= self.Ein_ms and wind_ms <= self.Nenn_ms:
            P_kw = (self.Nenn_kW / self.Nenn_ms) * wind_ms
            return P_kw
        'Ab Nenn_ms bis Abs_ms'
        if wind_ms > self.Nenn_ms and wind_ms <= self.Abs_ms:
            return self.Nenn_kW


    @staticmethod
    def getAnzahlWKAmodell():
        return WKAmodell.__counter






def WEAmodellDictionary():
    try:
        headerlistModell = ['Modell', 'Einschaltgeschwindigkeit m/s', 'Nenngeschwindigkeit m/s',
                            'Abschaltgeschwindigkeit m/s']
        openfilename3 = 'Datenbank\WEAModell/WEAModell.csv'
        print(openfilename3)
        df = pd.read_csv(openfilename3, usecols=headerlistModell, delimiter=';', decimal=',', header=0,
                                  encoding='latin1')
        print(df)
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
    WKA = dict()

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
            df['Leistung'][i] = 1500


    Ein_ms = df['Einschaltgeschwindigkeit m/s'].tolist()
    Nenn_ms = df['Nenngeschwindigkeit m/s'].tolist()
    Abs_ms = df['Abschaltgeschwindigkeit m/s'].tolist()
    P_kw = df['Leistung'].tolist()

    for index, k in enumerate(df['Modell']):
        WKA[k] = WKAmodell(k, Ein_ms[index], Nenn_ms[index], Abs_ms[index], P_kw[index])

    return WKA



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
        print(wetterdaten)
    except ValueError:
        print("falsches Format")

    if source == 'Wind':
        try:
            headerlistLokation = ['TYP', 'LEISTUNG', 'MODELL', 'Wetter-ID']
            openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matchfilelist3[0]
            print(openfilename1)

            lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal='.',
                                         header=0, encoding='latin1')

            lengthLocation = lokationsdaten.__len__()
            print(lokationsdaten)
        except ValueError:
            print("falsches Format")

        dictModell = WEAmodellDictionary()

        for i in range(lengthLocation):
            #print('Durchlaufnummer: ', i)
            Leistung = []
            #print(str(lokationsdaten['Wetter-ID'][i]))
            matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                  str(lokationsdaten['Wetter-ID'][i]) in match]
            #print(matcheswetterdaten)
            if len(matcheswetterdaten) != 2:
                print('Fehler Wetterdaten nicht schlimm')
                break
            columnName = str(i) + '_Ezg_' + str(lokationsdaten['TYP'][i]) + '_' + str(
                lokationsdaten['MODELL'][i]) + '_' + str(lokationsdaten['Wetter-ID'][i])
            try:
                Ein_ms = dictModell[lokationsdaten['MODELL'][i]][0]
            except:
                Ein_ms = 3
            try:
                Nenn_ms = dictModell[lokationsdaten['MODELL'][i]][1]
            except:
                Nenn_ms = 13
            try:
                Abs_ms = dictModell[lokationsdaten['MODELL'][i]][2]
            except:
                Abs_ms = 25
                #print('Use Execpt')
            for k in wetterdaten[matcheswetterdaten[0]]:

                # Fehler raus suchen
                if k < 0:
                    Leistung.append(int(0))

                # unter Nennleistung
                elif k >= Ein_ms and k < Nenn_ms:
                    x = (lokationsdaten['LEISTUNG'][i] / (Nenn_ms)) * k

                    Leistung.append(int(x))
                # ueber nennleistung
                elif k >= Nenn_ms and k < Abs_ms:
                    Leistung.append(int(lokationsdaten['LEISTUNG'][i]))

                # außerhalb der Betriebsgeschwindigekeit
                elif k >= Abs_ms or k < Ein_ms:
                    Leistung.append(int(0))


                else:
                    print("Fehler")
                    Leistung.append(int(0))

            print('Eintrag bei ', i)

            exportFrame[columnName] = Leistung

            #print('Eintrag Efolgreich ', i)

    if source == 'PV':
        try:
            headerlistLokation = ['Leistung','Bundesland', 'Wetter-ID']
            openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matchfilelist3[0]
            print(openfilename1)

            lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal=',',
                                         header=0, encoding='latin1')

            lengthLocation = lokationsdaten.__len__()
            print(lokationsdaten)
        except ValueError:
            print("falsches Format")

        for i in range(lengthLocation):
            Leistung = []
            print(i)
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
                    Leistung.append(0)
                else:
                    #print(lokationsdaten['Bruttoleistung der Einheit'][i])
                    #print(type(lokationsdaten['Bruttoleistung der Einheit'][i]))
                    x = lokationsdaten['Leistung'][i] * (k/fkt_Bestrahlung)*fkt_Solar
                    Leistung.append(x)

            #print('Eintrag bei ', i)
            exportFrame[columnName] = Leistung
            #print('Eintrag Efolgreich ', i)


    print(exportFrame)
    exportname = 'Datenbank\Erzeugung\Einzel/Erz_'+ source +'_' + state +'_' + str(year) + '.csv'
    exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

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
    EE_Erz['Verbrauch_Gesamt'] = verbrauch['Verbrauch_Gesamt']
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

    EE_Erz['>100%'] = liste_100
    EE_Erz['>75%'] = liste_75
    EE_Erz['>60%'] = liste_60
    EE_Erz['>50%'] = liste_50
    EE_Erz['>45%'] = liste_45
    EE_Erz['<45%'] = liste_k45

    print(EE_Erz)
    exportname = "GruenEnergie_" + str(year) + ".csv"
    EE_Erz.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

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