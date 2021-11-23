"""einen Platz um nicht im Restlichen Code immer rumschreiben zu müssen"""
""" Email PW: 4He3m4t#"""
"""testMaster@bietigheimer-htc.de"""

from email.mime.text import MIMEText
from email.header import Header
import smtplib
import pandas as pd

def testMail():

    msg = 'Rate mal wo ich die Email geschrieben habe, morgen 9:20Uhr los ?'
    subj = 'Hihi eine Email'
    frm = 'Absender <testMaster@bietigheimer-htc.de>'
    to = ['Alex Wengert <alexander.wengert@haw-hamburg.de',
          'Kranauge, Nils <Nils.Kranauge@haw-hamburg.de>',
          'Gildenstern, Lasse <Lasse.Gildenstern@haw-hamburg.de>'
          'Muhamed, Alshimaa Nabil Awaad Badawy <Alshimaa.Muhamed@haw-hamburg.de>',
          'Kaibour, Siham <Siham.Kaibour@haw-hamburg.de>',
          'Kompch, Maximilian Hans <Maximilian.Kompch@haw-hamburg.de>',
          'Boje, Maximilian <Maximilian.Boje@haw-hamburg.de>']

    toSoftware = ['AW <alexander.wengert@haw-hamburg.de','MB <Maximilian.Boje@haw-hamburg.de>']
    toMe = 'AW <alexander.wengert@haw-hamburg.de'
    toBoje = 'MB <Maximilian.Boje@haw-hamburg.de>'

    # Email zusammenstellen
    mail = MIMEText(msg, 'plain', 'utf-8')
    mail['Subject'] = Header(subj, 'utf-8')
    mail['From'] = frm
    mail['To'] = toBoje

    # Email versenden

    smtp = smtplib.SMTP('web03.dimait.de')
    smtp.starttls()
    smtp.login('testMaster@bietigheimer-htc.de', '4He3m4t#')
    smtp.sendmail(frm, [toBoje], mail.as_string())
    smtp.quit()

def testZeitintervallDateien():
    Liste1 = []
    Liste2 = []

    hourly2019 = pd.date_range('01.01.2019 00:00', '31.12.2019 23:00', freq='60min')
    hourly2020 = pd.date_range('01.01.2020 00:00', '31.12.2020 23:00', freq='60min')

    for i in range(len(hourly2019)):
        Liste1.append(hourly2019[i])

    for i in range(len(hourly2020)):
        Liste2.append(hourly2020[i])

    dataFrame = pd.DataFrame(
        {'Datum1': hourly2019,
         }
    )
    exportname2 = "Datenbank/" + "Datum" + ".csv"
    dataFrame.to_csv(exportname2, sep=';', encoding='utf-8', index=False)

    dataFrame = pd.DataFrame(
        {'Datum1': hourly2019,
         }
    )
    exportname3 = "Datenbank/" + "Datum2" + ".csv"
    dataFrame.to_csv(exportname3, sep=';', encoding='utf-8', index=False)

def testTxtWetterdatenToCSV():
    print('Start')
    try:
        openfilename = 'Datenbank\Wetter\SolarText/produkt_st_stunde_19720101_20150131_03032.txt'
        print(openfilename)
        df = pd.read_csv(openfilename, delimiter=';', decimal='.', header=0)
        """if firstDataFrame == False:
            dataFrame = df
            firstDataFrame = True
        else:
            dataFrame = dataFrame.append(df, ignore_index=True)"""

    except ValueError:
        print("falsches Format")

    print(df)


def einmalLöschenbitte():
    print('Start testTxtWetterdatenWindToCSV')
    "Kontrolle der Daten"

    FilesName = []
    FilesTrueFalse = []
    AnzahlDaten = []
    DatenTrue = []
    DatenFalse = []
    DatenProzent = []

    Datumabgleich = dateList_dataFrame('01.01.' + str(Year) + ' 00:00',
                                       '31.12.' + str(Year) + ' 23:00', '60min', list=True)

    files = findoutFiles('Datenbank\Wetter\WindText')

    valueOfDatesInYear = Datumabgleich.__len__()

    matches = [match for match in files if "produkt_ff_stunde" in match]
    print(matches)

    lengthOFWeatherStations = matches.__len__()
    firsttime = True

    for i in range(lengthOFWeatherStations):
        windMperS = []
        windDegree = []
        try:
            openfilename = 'Datenbank\Wetter\WindText/' + matches[i]
            print(openfilename)
            df = pd.read_csv(openfilename, delimiter=';', decimal='.', header=0)
            FilesTrueFalse.append(True)
            print(df.shape)

        except ValueError:
            "Fehlerhandling muss noch gemacht werden!"
            print("falsches Format")
            print(matches[i] + "Falsch in der Liste")
            FilesTrueFalse.append(False)
            continue

        FilesName.append(matches[i])

        Wind_MproS = 'Wind_m/s_' + str(df['STATIONS_ID'][2])
        Wind_grad = 'Wind_grad_' + str(df['STATIONS_ID'][2])

        importLength = df.__len__()
        # print(df)
        start = 0
        falseExpiry = 0
        trueExpiry = 0
        "Um fehlende Messwerte sinnvoll zu füllen wird der Zeitpunktunt in 7 vergangenen Punkten angeschaut"
        "1 Tag / 2 Tage /3 Tage /1 Jahr /1 Jahr + 1 Tag / 1 Jahr +2 Tage /1 Jahr + 3 Tage"
        "Es wird dann aus diesen Daten ein mittel gebildet. Sollte ein Wert fehlen wir dieser ignoriert"
        "Gibt es gar keine Werte wird -999 eingetragen"

        lostWeatherValue = [24, 48, 72, 8760, 8784, 8808, 17616, 17520, 17568, 17616]

        for k in range(importLength):
            if start >= valueOfDatesInYear:
                "Fehlerhandling muss noch gemacht werden!"
                break

            datetime_object = datetime.strptime(str(df['MESS_DATUM'][k]), '%Y%m%d%H')
            try:
                if Datumabgleich[0] <= datetime_object and datetime_object != Datumabgleich[start]:
                    print('fehlender Messert und fehlendes Datum')
                    print('Ersatzwerte werden gesucht.')

                    while datetime_object != Datumabgleich[start]:
                        substituteWeather = []
                        substituteDegree = []
                        for j in lostWeatherValue:
                            if (k - j) < 0:
                                continue
                            asd = datetime.strptime(str(df['MESS_DATUM'][k - j]), '%Y%m%d%H')
                            # print(asd)
                            # print(datetime_object)
                            # print(df['   F'][k - j])
                            # print(df['   D'][k - j])
                            "Eintragen wenn die Messwerte Falsch sind "
                            if df['   F'][k - j] > -999 and df['   D'][k - j] > -999:
                                substituteWeather.append(df['   F'][k - j])
                                substituteDegree.append(df['   D'][k - j])
                            "Anzahl der Eintragungen"
                        lengthOfsubstituteWeather = len(substituteWeather)
                        lengthOfsubstituteDegree = len(substituteDegree)
                        "Fehler wenn kein Eintrag erfolgt ist"
                        if lengthOfsubstituteWeather == 0 or lengthOfsubstituteDegree == 0:
                            "Fehlerhandling muss noch gemacht werden!"
                            break

                        MperS = sum(substituteWeather) / lengthOfsubstituteWeather
                        Degree = sum(substituteDegree) / lengthOfsubstituteDegree
                        if MperS == -999 or Degree == -999:
                            MperS = 0
                            Degree = 0
                        "Ermitteln des neuen Werts"
                        windMperS.append(MperS)
                        windDegree.append(Degree)
                        falseExpiry += 1
                        start += 1

            except IndexError:
                "Fehlerhandling muss noch gemacht werden!"
                print('Pause')
                "erneute überprüfung da Start verändert wurde"
                falseExpiry += 1
            if start >= valueOfDatesInYear:
                break
            if Datumabgleich[0] <= datetime_object and (df['   F'][k] < 0 or df['   F'][k] < 0):
                print('fehlender Messert -999')
                substituteWeather = []
                substituteDegree = []
                for j in lostWeatherValue:
                    if (k - j) < 0:
                        continue
                    asd = datetime.strptime(str(df['MESS_DATUM'][k - j]), '%Y%m%d%H')
                    # print(asd)
                    # print(datetime_object)
                    # print(df['   F'][k - j])
                    # print(df['   D'][k - j])
                    "Eintragen wenn die Messwerte Falsch sind "
                    if df['   F'][k - j] > -999 and df['   D'][k - j] > -999:
                        substituteWeather.append(df['   F'][k - j])
                        substituteDegree.append(df['   D'][k - j])
                    "Anzahl der Eintragungen"
                lengthOfsubstituteWeather = len(substituteWeather)
                lengthOfsubstituteDegree = len(substituteDegree)
                "Fehler wenn kein Eintrag erfolgt ist"
                if lengthOfsubstituteWeather == 0 or lengthOfsubstituteDegree == 0:
                    "Fehlerhandling muss noch gemacht werden!"
                    break
                MperS = sum(substituteWeather) / lengthOfsubstituteWeather
                Degree = sum(substituteDegree) / lengthOfsubstituteDegree
                if MperS == -999 or Degree == -999:
                    MperS = 0
                    Degree = 0
                "Ermitteln des neuen Werts"
                windMperS.append(MperS)
                windDegree.append(Degree)
                falseExpiry += 1
                start += 1

            if datetime_object == Datumabgleich[start]:
                # print('Die beiden nächsten')
                # print(Datumabgleich[start])
                # print(datetime_object)
                windMperS.append(df['   F'][k])
                windDegree.append(df['   D'][k])
                start += 1
                trueExpiry += 1
                continue

        # print(str(start) + openfilename)
        AnzahlDaten.append(start)
        DatenTrue.append(trueExpiry)
        DatenFalse.append(falseExpiry)
        DatenProzent.append(trueExpiry / start)

        if firsttime == True:
            firsttime = False
            exportFrame = pd.DataFrame(
                {'Datum': Datumabgleich,
                 Wind_MproS: windMperS,
                 Wind_grad: windDegree}
            )

            continue
        if valueOfDatesInYear != start:
            print("Stop")
        if firsttime == False:
            exportFrame[Wind_MproS] = windMperS
            exportFrame[Wind_grad] = windDegree
            # print(exportFrame)

    KontrolFrame = pd.DataFrame(
        {'DatenName': FilesName,
         'Daten eingelesen': FilesTrueFalse,
         'Daten Anzahl': AnzahlDaten,
         'Daten Richtig': DatenTrue,
         'Daten Falsch': DatenFalse,
         'Daten in Prozent': DatenProzent
         }
    )

    exportname1 = 'WindWetterdaten_' + str(Year) + '.csv'
    exportFrame.to_csv(exportname1, sep=';', encoding='utf-8', index=False, decimal=',')
    exportname2 = 'Datenauswertung.csv'
    KontrolFrame.to_csv(exportname2, sep=';', encoding='utf-8', index=False, decimal=',')
    print('Fertig')



