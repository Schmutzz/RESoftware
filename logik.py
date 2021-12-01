import pandas as pd
from database import findoutFiles
"""Erzeugt ein DataFrame oder eine Liste mit fortlaufenden Datum+Uhrzeit"""
from database import dateList_dataFrame as DateList
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



def erzeugungsdatenEEAnlagen(year, source , state):

    exportFrame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00','60min')


    filelist = findoutFiles('Datenbank\ConnectwithID\Erzeugung')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(year) in match]
    print(matchfilelist3)
    print('Hello')

    try:
        openfilename2 = 'Datenbank\Wetter/'+ source +'Wetterdaten_' + str(year) + '.csv'
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
            Leistung = []
            print(str(lokationsdaten['Wetter-ID'][i]))
            matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                  str(lokationsdaten['Wetter-ID'][i]) in match]
            print(matcheswetterdaten)
            if len(matcheswetterdaten) != 2:
                print('Fehler Wetterdaten')
                break
            columnName = str(i) + '_Ezg_' + str(lokationsdaten['TYP'][i]) + '_' + str(
                lokationsdaten['MODELL'][i]) + '_' + str(lokationsdaten['Wetter-ID'][i])
            try:
                Ein_ms = dictModell[lokationsdaten['MODELL'][i]][0]
                Nenn_ms = dictModell[lokationsdaten['MODELL'][i]][1]
                Abs_ms = dictModell[lokationsdaten['MODELL'][i]][2]
            except:
                Ein_ms = 3
                Nenn_ms = 13
                Abs_ms = 25
                print('Use Execpt')
            for k in wetterdaten[matcheswetterdaten[0]]:

                # Fehler raus suchen
                if k < 0:
                    Leistung.append(int(0))
                    continue

                # ueber nennleistung
                if k >= Nenn_ms:
                    Leistung.append(int(lokationsdaten['LEISTUNG'][i]))
                    continue
                # außerhalb der Betriebsgeschwindigekeit
                if k >= Abs_ms or k < Ein_ms:
                    Leistung.append(int(0))
                    continue
                # unter Nennleistung
                if k >= Ein_ms and k < Nenn_ms:
                    x = (lokationsdaten['LEISTUNG'][i] / (Nenn_ms)) * k

                    Leistung.append(int(x))
                    continue

            print('Eintrag bei ', i)

            exportFrame[columnName] = Leistung

            print('Eintrag Efolgreich ', i)

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


def erzeugungPerStunde(year, source1, source2):

    print("Start Erzeugung per Stunde")

    files = findoutFiles('Datenbank\Erzeugung/Einzel')

    matches = [match for match in files if str(year) in match]

    Datumabgleich = DateList('01.01.' + str(year)+ ' 00:00',
                                        '31.12.' + str(year) + ' 23:00', '60min', list=True)
    lengthmachtes = matches.__len__()
    lengthmachtes -= 1
    try:
        openfilename = 'Datenbank\Erzeugung/Einzel/' + matches[0]
        print(openfilename)
        df = pd.read_csv(openfilename, delimiter=';', decimal='.', header=0)
        print(df.index)
    except:
        print('FEHLER')

    for i in range(lengthmachtes):
        try:
            openfilename2 = 'Datenbank\Erzeugung/Einzel/' + matches[i+1]
            print(openfilename2)
            df2 = pd.read_csv(openfilename2, delimiter=';', decimal='.', header=0)

        except:
            print('FEHLER')
        if i == 0:
            #df.merge(right=df2, left_index=True, right_on='Datum')
            df3 = pd.concat([df, df2], axis=1, sort=False)
            print(df3)
        if i > 0:
            df3 = pd.concat([df3, df2], axis=1, sort=False)
            print(df3)
    exportname = 'Datenbank\Erzeugung/erzeugungsdatenGesamt_' + str(year) + '.csv'
    df3.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    del df3['Datum']

    sum_3= df3.sum(axis=1, numeric_only=None)
    #sum_3 = df3.iloc[2].sum(axis=0)
    #print(df3.values.sum())
    print(sum_3)
    lengthDatum = len(Datumabgleich)
    lentghSum_3 = len(sum_3)
    if lengthDatum != lentghSum_3:
        print('FEHLER')


    AusgabeFrame = pd.DataFrame(
        {
            'Datum': Datumabgleich,
            'SummeGruen': sum_3
        }
    )

    exportname = 'Datenbank\Erzeugung/erzeugungsdatenGesamt_komuliert_' + str(year) + '.csv'
    AusgabeFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    return AusgabeFrame

def verbrauchGesamt(year):

    files = findoutFiles('Datenbank\Verbrauch\Einzeln')

    matches = [match for match in files if str(year) in match]

    Datumabgleich = DateList('01.01.' + str(year) + ' 00:00',
                             '31.12.' + str(year) + ' 23:00', '60min', list=True)

    #try:
    openfilename = 'Datenbank\Verbrauch\Einzeln/' + matches[0]
    print(openfilename)
    df = pd.read_csv(openfilename, encoding='latin1' ,delimiter=';', decimal=',', header=0)
    print(df.index)
    #except:
    print('FEHLER')

    del df['Datum']

    sum_3 = df.sum(axis=1, numeric_only=None)
    lengthDatum = len(Datumabgleich)
    lentghSum_3 = len(sum_3)

    AusgabeFrame = pd.DataFrame(
        {
            'Datum': Datumabgleich,
            'SummeVerbrauch': sum_3
        }
    )

    exportname = "Datenbank\Verbrauch\Verbrauch_komuliert_"+ str(year) + ".csv"
    AusgabeFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    return AusgabeFrame

def analyseEE(year, FrameErzeung, FrameVerbrauch):

    del FrameVerbrauch['Datum']
    #print(FrameVerbrauch)
    #print(FrameErzeung)
    FrameErzeung['Verbrauch'] = FrameVerbrauch['SummeVerbrauch']
    print(FrameErzeung)
    FrameErzeung['EE_Anteil'] = FrameErzeung['SummeGruen']/FrameVerbrauch['SummeVerbrauch']
    liste_100 = []
    liste_75 = []
    liste_60 = []
    liste_50 = []
    liste_45 = []
    liste_k45 = []


    for i in FrameErzeung['EE_Anteil']:

        if i >= 1.0:
            liste_100.append(True)
            liste_75.append(False)
            liste_60.append(False)
            liste_50.append(False)
            liste_45.append(False)
            liste_k45.append(False)
            continue
        if i >= 0.75:
            liste_100.append(False)
            liste_75.append(True)
            liste_60.append(False)
            liste_50.append(False)
            liste_45.append(False)
            liste_k45.append(False)
            continue
        if i >= 0.6:
            liste_100.append(False)
            liste_75.append(False)
            liste_60.append(True)
            liste_50.append(False)
            liste_45.append(False)
            liste_k45.append(False)
            continue
        if i >= 0.5:
            liste_100.append(False)
            liste_75.append(False)
            liste_60.append(False)
            liste_50.append(True)
            liste_45.append(False)
            liste_k45.append(False)
            continue
        if i >= 0.45:
            liste_100.append(False)
            liste_75.append(False)
            liste_60.append(False)
            liste_50.append(False)
            liste_45.append(True)
            liste_k45.append(False)
            continue
        if i < 0.45:
            liste_100.append(False)
            liste_75.append(False)
            liste_60.append(False)
            liste_50.append(False)
            liste_45.append(False)
            liste_k45.append(True)
            continue

    FrameErzeung['>100%'] = liste_100
    FrameErzeung['>75%'] = liste_75
    FrameErzeung['>60%'] = liste_60
    FrameErzeung['>50%'] = liste_50
    FrameErzeung['>45%'] = liste_45
    FrameErzeung['<45%'] = liste_k45

    print(FrameErzeung)
    exportname = "GruenEnergie_"+ str(year) + ".csv"
    FrameErzeung.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

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