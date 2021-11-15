import pandas as pd
from database import findoutFiles

def modellDictionary():
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



def erzeugungsdaten(year, source , state):

    Datumabgleich = []

    hourly2019_2020 = pd.date_range('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', freq='60min')

    for i in range(len(hourly2019_2020)):
        Datumabgleich.append(hourly2019_2020[i])

    exportFrame = pd.DataFrame(
        {'Datum': Datumabgleich
         }
    )

    filelist = findoutFiles('Datenbank\ConnectwithID\Erzeugung')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(year) in match]
    print(matchfilelist3)
    print('Hello')
    try:
        headerlistLokation= ['TYP', 'LEISTUNG', 'MODELL', 'Wetter-ID']
        openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matchfilelist3[0]
        print(openfilename1)
        lokationsdaten = pd.read_csv(openfilename1, usecols=headerlistLokation, delimiter=';', decimal='.', header=0)
        lengthLocation = lokationsdaten.__len__()
        print(lokationsdaten)
    except ValueError:
        print("falsches Format")


    try:
        openfilename2 = 'Datenbank\Wetter/'+ source +'Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)
        print(wetterdaten)
    except ValueError:
        print("falsches Format")


    dictModell = modellDictionary()

    print(dictModell)
    print(dictModell['Enercon E-70 E4/2000'][1])

    for i in range(lengthLocation):
        Leistung = []
        print(str(lokationsdaten['Wetter-ID'][i]))
        matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if str(lokationsdaten['Wetter-ID'][i]) in match]
        print(matcheswetterdaten)
        if len(matcheswetterdaten) != 2:
            print('Fehler Wetterdaten')
            break
        columnName= str(i)+'_Ezg_'+str(lokationsdaten['TYP'][i]) +'_'+ str(lokationsdaten['MODELL'][i])
        Ein_ms = dictModell[lokationsdaten['MODELL'][i]][0]
        Nenn_ms = dictModell[lokationsdaten['MODELL'][i]][1]
        Abs_ms = dictModell[lokationsdaten['MODELL'][i]][2]

        for k in wetterdaten[matcheswetterdaten[0]]:

            #Fehler raus suchen
            if k < 0:
                Leistung.append(int(0))
                continue

            #ueber nennleistung
            if k >= Nenn_ms:
                Leistung.append(int(lokationsdaten['LEISTUNG'][i]))
                continue
            #außerhalb der Betriebsgeschwindigekeit
            if k >= Abs_ms or k < Ein_ms:
                Leistung.append(int(0))
                continue
            #unter Nennleistung
            if k >= Ein_ms and k < Nenn_ms:

                x = (lokationsdaten['LEISTUNG'][i]/(Nenn_ms)) * k

                Leistung.append(int(x))
                continue

        print('Eintrag bei ', i)

        exportFrame[columnName] = Leistung

        print('Eintrag Efolgreich ', i)

    print(exportFrame)
    exportname = 'Datenbank\Erzeugung/Erz_'+ source +'_' + state +'_' + str(year) + '.csv'
    exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    print('Fertig')


