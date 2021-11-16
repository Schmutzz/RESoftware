import pandas as pd
from database import findoutFiles

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

def dateList_dataFrame(start,stop,freq):
    Datumabgleich = []
    hourly2019_2020 = pd.date_range(start, stop, freq=freq)

    for i in range(len(hourly2019_2020)):
        Datumabgleich.append(hourly2019_2020[i])

    exportFrame = pd.DataFrame(
        {'Datum': Datumabgleich
         }
    )

    return exportFrame




def erzeugungsdatenEEAnlagen(year, source , state):

    exportFrame = dateList_dataFrame('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00','60min')


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
                Abs_ms = 30
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
            headerlistLokation = ['MaStR-Nr. der Einheit','Bruttoleistung der Einheit', 'Wetter-ID']
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


            columnName = str(i) + '_Ezg_PV' + '_'+str(lokationsdaten['MaStR-Nr. der Einheit'][i])+ '_'+ str(lokationsdaten['Wetter-ID'][i])

            fkt_Bestrahlung = 492.48
            fkt_Solar = 0.9

            for k in wetterdaten[matcheswetterdaten[0]]:

                if lokationsdaten['Bruttoleistung der Einheit'][i] < 0:
                    Leistung.append(0)
                else:
                    #print(lokationsdaten['Bruttoleistung der Einheit'][i])
                    #print(type(lokationsdaten['Bruttoleistung der Einheit'][i]))
                    x = lokationsdaten['Bruttoleistung der Einheit'][i] * (k/fkt_Bestrahlung)*fkt_Solar
                    Leistung.append(x)

            #print('Eintrag bei ', i)
            exportFrame[columnName] = Leistung
            #print('Eintrag Efolgreich ', i)


    print(exportFrame)
    exportname = 'Datenbank\Erzeugung/Erz_'+ source +'_' + state +'_' + str(year) + '.csv'
    exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    print('Fertig')


