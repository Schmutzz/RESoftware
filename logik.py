import pandas as pd

def erzeugungsdatenWindHH(Year):

    Datumabgleich = []

    hourly2019_2020 = pd.date_range('01.01.' + str(Year) + ' 00:00', '31.12.' + str(Year) + ' 23:00', freq='60min')

    for i in range(len(hourly2019_2020)):
        Datumabgleich.append(hourly2019_2020[i])

    exportFrame = pd.DataFrame(
        {'Datum': Datumabgleich
         }
    )

    print('Hello')
    try:
        headerlist= ['TYP', 'LEISTUNG', 'MODELL', 'Wetter-ID']
        openfilename = 'Datenbank\ConnectwithID/WindparksHH_WetterID.csv'
        print(openfilename)
        lokationsdaten = pd.read_csv(openfilename, usecols=headerlist, delimiter=';', decimal='.', header=0)
        lengthLocation = lokationsdaten.__len__()

    except ValueError:
        print("falsches Format")

    print(lokationsdaten)
    try:
        openfilename = 'Datenbank\Wetter/WindWetterdaten_' + str(Year) + '.csv'
        print(openfilename)
        wetterdaten = pd.read_csv(openfilename, delimiter=';', decimal=',', header=0)
    except ValueError:
        print("falsches Format")
    print(wetterdaten)

    for i in range(lengthLocation):
        Leistung = []
        print(str(lokationsdaten['Wetter-ID'][i]))
        matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if str(lokationsdaten['Wetter-ID'][i]) in match]
        print(matcheswetterdaten)
        if len(matcheswetterdaten) != 2:
            print('Fehler')
            break
        columnName= str(i)+'_Ezg_'+str(lokationsdaten['TYP'][i]) +'_'+ str(lokationsdaten['MODELL'][i])
        Ein_ms = 2.5
        Nenn_ms = 13.5
        Abs_ms = 34

        for k in wetterdaten[matcheswetterdaten[0]]:
            findApartner = False
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
                round(x, 2)
                Leistung.append(int(x))
                continue

        print('Eintrag bei ', i)

        exportFrame[columnName] = Leistung

        print('Eintrag Efolgreich ', i)

    print(exportFrame)
    exportname = 'Datenbank\Erzeugung/Erzeugung_HH_' + str(Year) + '.csv'
    exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    print('Fertig')


