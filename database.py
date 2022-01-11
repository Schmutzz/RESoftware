import pandas as pd
import csv
import os
from datetime import datetime
from zipfile import ZipFile
from pyproj import Proj


from geopy import distance
import geo


class weatherStation():
    __conuter = 0

    def __init__(self, ID, Source, stationshoehe):
        self.ID = ID
        self.Source = Source
        self.stationshoehe = stationshoehe

    def infoStation(self):
        print('Stationnummer: ', self.ID)
        print('Messart', self.Source)


class windWeatherStation(weatherStation):
    maxSpeed = 100
    maxDegree = 361

    def __init__(self):
        self.__Speed_ms = []
        self.__Degree_Gd = []
        self.__maxSpeed = 100
        self.__maxDegree = 361

    def setSpeed_ms(self, Value):
        if isinstance(Value, float) == False and isinstance(Value, int) == False:
            self.__Speed_ms.append(0)
            return False
        elif Value < 0 or Value > self.__maxSpeed:
            self.__Speed_ms.append(0)
            return False
        else:
            self.__Speed_ms.append(Value)

    def counterOfHourseperStep(self):
        listparameter = []
        falsch = []

        if len(self.__Speed_ms) == 0:
            return False
        for i in self.__maxSpeed:
            for k in range(35):
                if float(i) >= float(k):
                    listparameter[k] += 1
                else:
                    falsch[k] += 1


def findoutFiles(filename):
    # print("Suche beginnt")
    files = os.listdir(filename)
    # print(files)
    # print(len(files))

    return files


def zipentpacken(zipFileName, source):
    try:
        with ZipFile(zipFileName, 'r') as zip:
            zip.extractall('Datenbank\Wetter/' + source + 'Text')
            print('File is unzipped in temp Datenbank\Wetter\WindText')

    except ValueError:
        print("Probleme mit der Zip-Datei")
    except BaseException:
        print("is not a Zipfile")


def dateList_dataFrame(start, stop, freq, list=False):
    "Erzeugt eine DataFrame oder eine Liste mit einer Spalte"

    Datumabgleich = []
    hourly2019_2020 = pd.date_range(start, stop, freq=freq)

    for i in range(len(hourly2019_2020)):
        Datumabgleich.append(hourly2019_2020[i])

    exportFrame = pd.DataFrame(
        {'Datum': Datumabgleich
         }
    )
    if list == False:
        return exportFrame
    if list == True:
        return Datumabgleich


def erzeugungsZsmPV(year, state, source='PV', weatherConnect=True):
    """Diese Funktion addiert alle Solarleistung aus einer Datei vor dem angegeben Jahr.
    Die Leistung im angegeben Jahr werden halbiert um die Mitte des bestcase/worstcase zu erreichen
    Die Leistungen werden nach Wetterstationen sortiert."""

    "Dataframe Listen vorbereitung"
    Erzeugungsjahr = []
    Bundesland = []
    LeistungBisJahr = []
    LeistungInJahr = []
    LeistungGesamt = []
    WetterStation = []
    print('Start erzeugungsZsmPV ')
    if weatherConnect == True:
        weatherIDConnect = 'zugeordnet'
    if weatherConnect == False:
        weatherIDConnect = 'gewichtet'

    Datumabgleich = dateList_dataFrame('01.01.' + str(year - 1),
                                       '01.01.' + str(year + 1), 'Y', list=True)
    # print(Datumabgleich)
    # 2021 muss ersetzt werden durch Zeitfunktion
    filelist = findoutFiles('Datenbank\ConnectwithID\PV_einzelneAnlagen')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(2021) in match]
    matchfilelist4 = [match for match in matchfilelist3 if weatherIDConnect in match]

    try:
        headerlistLokation = ['Nettonennleistung der Einheit', 'Inbetriebnahmedatum der Einheit', 'Wetter-ID_Head']
        openfilename1 = 'Datenbank\ConnectwithID\PV_einzelneAnlagen/' + matchfilelist4[0]
        # print(openfilename1)

        lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal=',',
                                     header=0, encoding='latin1')

        # print(lokationsdaten)
    except ValueError:
        print("falsches Format")

    try:
        headerlistLokation2 = ['Stations_id', 'Bundesland']
        openfilename2 = 'Import\Wetterstationen/StundeWindStationen.csv'
        # print(openfilename2)

        wetterID = pd.read_csv(openfilename2, delimiter=';', usecols=headerlistLokation2, decimal=',',
                               header=0, encoding='latin1')

        # print(wetterID)
    except ValueError:
        print("falsches Format")

    # print(lokationsdaten['Wetter-ID_Head'].describe())

    for i, k in enumerate(wetterID['Stations_id']):

        summeBisYear = 0
        SummeInYear = 0

        for j in range(len(lokationsdaten)):

            datetime_object = datetime.strptime(str(lokationsdaten['Inbetriebnahmedatum der Einheit'][j]), '%d.%m.%Y')

            if datetime_object <= Datumabgleich[0] and k == lokationsdaten['Wetter-ID_Head'][j]:
                summeBisYear += lokationsdaten['Nettonennleistung der Einheit'][j]

            if datetime_object > Datumabgleich[0] and datetime_object < Datumabgleich[1] and k == \
                    lokationsdaten['Wetter-ID_Head'][j]:
                SummeInYear += lokationsdaten['Nettonennleistung der Einheit'][j]
        # wird für die Bedingung gebraucht
        sum_3 = summeBisYear + SummeInYear

        if sum_3 == 0:
            continue

        SummeInYear /= 2
        Erzeugungsjahr.append(year)
        LeistungBisJahr.append(summeBisYear)
        LeistungInJahr.append(SummeInYear)
        LeistungGesamt.append(summeBisYear + SummeInYear)
        WetterStation.append(wetterID['Stations_id'][i])
        Bundesland.append(wetterID['Bundesland'][i])
        # print('New Value')
        # print(wetterID['Stations_id'][i])

    AusgabeFrame = pd.DataFrame(
        {
            'Jahr': Erzeugungsjahr,
            'LeistungBisJahr': LeistungBisJahr,
            'LeistungInJahr': LeistungInJahr,
            'Leistung': LeistungGesamt,
            'Wetter-ID': WetterStation,
            'Bundesland': Bundesland
        }
    )

    exportname = 'Datenbank\ConnectwithID\Erzeugung/PV_Anlagen_' + state + '_WetterID_' + str(year) + '_komuliert.csv'
    AusgabeFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

    print('ENDE erzeugungsZsmPV ')


def TxtWetterdatenSolarToCSV():
    print('Start')
    files = findoutFiles('Datenbank\Wetter\SolarText')
    dataFrame = {1: ['1', '2'], 2: ['3', '4']}
    header = ['STATIONS_ID', 'ZENIT', 'MESS_DATUM_WOZ', 'FG_LBERG']
    firstDataFrame = False

    matches = [match for match in files if "produkt_st_stunde" in match]
    print(matches)

    length = matches.__len__()

    for i in range(length):
        # try:
        openfilename = 'Datenbank\Wetter\SolarText/' + matches[i]
        print(openfilename)
        df = pd.read_csv(openfilename, usecols=header, delimiter=';', decimal='.', header=0)

        # if firstDataFrame == False:
        # dataFrame = df
        #  firstDataFrame = True

        #  else:
        # dataFrame.merge(right=df, left_index=True, how='cross', right_on='MESS_DATUM_WOZ')
        # dataFrame.merge(right=df, how='cross')
        # print(dataFrame)

        exportname = "erzeugungsdatenVersuche" + str(i) + ".csv"
        df.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

        # except ValueError:
        # print("falsches Format")

    print(df)


def TxtWetterdatenToCSV(Year, source):
    print('Start testTxtdatenWindToCSV ', source)
    "Kontrolle der Daten"

    FilesName = []
    FilesTrueFalse = []
    AnzahlDaten = []
    DatenTrue = []
    DatenD_TFalse = []
    DatenDFalse = []
    D_T_Prozent = []
    D_Prozent = []

    Datumabgleich = dateList_dataFrame('01.01.' + str(Year) + ' 00:00',
                                       '31.12.' + str(Year) + ' 23:00', '60min', list=True)
    valueOfDatesInYear = Datumabgleich.__len__()
    if source == 'PV':
        sourceName1 = 'PV_LBERG_'
        sourceName2 = 'PV_Zenit_'
        textName = 'produkt_st_stunde'
        MessDate = 'MESS_DATUM_WOZ'
        MessDateType = '%Y%m%d%H:%M'
        MessSource1 = 'FG_LBERG'
        MessSource2 = 'ZENIT'
    if source == 'Wind':
        sourceName1 = 'Wind_m/s_'
        sourceName2 = 'Wind_grad_'
        textName = "produkt_ff_stunde"
        MessDate = 'MESS_DATUM'
        MessSource1 = '   F'
        MessSource2 = '   D'
        MessDateType = '%Y%m%d%H'

    try:
        files = findoutFiles('Datenbank\Wetter/' + source + 'Text')
    except ValueError:
        print('WARNING')

    matches = [match for match in files if textName in match]
    print(matches)

    lengthOFWeatherStations = matches.__len__()
    firsttime = True

    for i in range(lengthOFWeatherStations):
        windMperS = []
        windDegree = []
        try:
            openfilename = 'Datenbank\Wetter/' + source + 'Text/' + matches[i]
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

        Source_1 = sourceName1 + str(df['STATIONS_ID'][2])
        Source_2 = sourceName2 + str(df['STATIONS_ID'][2])

        importLength = df.__len__()
        # print(df)
        start = 0
        falseExpiry = 0
        trueExpiry = 0
        falseValueExpiry = 0
        "Um fehlende Messwerte sinnvoll zu füllen wird der Zeitpunktunt in 7 vergangenen Punkten angeschaut"
        "1 Tag / 2 Tage /3 Tage /1 Jahr /1 Jahr + 1 Tag / 1 Jahr +2 Tage /1 Jahr + 3 Tage"
        "Es wird dann aus diesen Daten ein mittel gebildet. Sollte ein Wert fehlen wir dieser ignoriert"
        "Gibt es gar keine Werte wird -999 eingetragen"

        lostWeatherValueDate = [2, 8, 12, 16, 24, 48, 36, 52, 72, 8760, 8784, 8808, 17616, 17520, 17568, 17616]
        # lostWeatherValueDate = [2, 8, 12, 16]
        lostWeatherValueError = [1, 2, 3, -1, -2, -3, 24, 72, 8760, 8784, 8808, 17616, 17520, 17568, 17616]
        for k in range(importLength):
            if start >= valueOfDatesInYear:
                "Fehlerhandling muss noch gemacht werden!"
                break

            datetime_object = datetime.strptime(str(df[MessDate][k]), MessDateType)
            # datetime_object = datetime.strptime(str(df['MESS_DATUM'][k]), '%Y%m%d%H:%M')
            try:
                if Datumabgleich[0] <= datetime_object and datetime_object != Datumabgleich[start]:
                    print('fehlender Messert und fehlendes Datum')
                    print('Ersatzwerte werden gesucht.')

                    while datetime_object != Datumabgleich[start]:
                        substituteWeather = []
                        substituteDegree = []
                        for j in lostWeatherValueDate:
                            if (k - j) < 0:
                                continue

                            "Eintragen wenn die Messwerte Falsch sind "
                            if df[MessSource1][k - j] > -999 and df[MessSource2][k - j] > -999:
                                substituteWeather.append(df[MessSource1][k - j])
                                substituteDegree.append(df[MessSource2][k - j])
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
            if Datumabgleich[0] <= datetime_object and (df[MessSource1][k] < 0 or df[MessSource2][k] < 0):
                print('fehlender Messert -999')
                substituteWeather = []
                substituteDegree = []
                for j in lostWeatherValueError:
                    if (k - j) < 0:
                        continue

                    "Eintragen wenn die Messwerte Falsch sind "
                    if df[MessSource1][k - j] > -999 and df[MessSource2][k - j] > -999:
                        substituteWeather.append(df[MessSource1][k - j])
                        substituteDegree.append(df[MessSource2][k - j])
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

                falseValueExpiry += 1
                start += 1

            if datetime_object == Datumabgleich[start]:
                # print('Die beiden nächsten')
                # print(Datumabgleich[start])
                # print(datetime_object)
                windMperS.append(df[MessSource1][k])
                windDegree.append(df[MessSource2][k])

                start += 1
                trueExpiry += 1
                continue

        # print(str(start) + openfilename)
        AnzahlDaten.append(start)
        DatenTrue.append(trueExpiry)
        DatenD_TFalse.append(falseExpiry)
        DatenDFalse.append(falseValueExpiry)
        D_Prozent.append(falseValueExpiry / start)
        D_T_Prozent.append(trueExpiry / start)

        if firsttime == True:
            firsttime = False
            exportFrame = pd.DataFrame(
                {'Datum': Datumabgleich,
                 Source_1: windMperS,
                 Source_2: windDegree}
            )

            continue
        if valueOfDatesInYear != start:
            print("Stop")
        if firsttime == False:
            exportFrame[Source_1] = windMperS
            exportFrame[Source_2] = windDegree
            # print(exportFrame)

    KontrolFrame = pd.DataFrame(
        {'DatenName': FilesName,
         'Daten eingelesen': FilesTrueFalse,
         'Daten Anzahl': AnzahlDaten,
         'Daten Richtig': DatenTrue,
         'Error Anzahl': DatenDFalse,
         'Kein Datum': DatenD_TFalse,
         'Error in Prozent': D_Prozent,
         'Kein Datum in Prozent': D_T_Prozent
         }
    )

    exportname1 = 'Datenbank\Wetter/' + source + '_Wetterdaten_' + str(Year) + '.csv'
    exportFrame.to_csv(exportname1, sep=';', encoding='utf-8', index=False, decimal=',')
    exportname2 = 'Datenbank\Wetter/' + source + '_Datenauswertung' + str(Year) + '.csv'
    KontrolFrame.to_csv(exportname2, sep=';', encoding='utf-8', index=False, decimal=',')
    print('Fertig testTxtdatenWindToCSV ', source)


def utm_to_gk(name, df, export=False):
    # myProj = Proj(proj='utm', zone=32 , ellps='WGS84' ,preserve_units=False
    myProj = Proj("epsg:4647", preserve_units=False)

    lon, lat = myProj(df['OSTWERT (EPSG:4647)'].tolist(), df['NORDWERT (EPSG:4647)'].tolist(), inverse=True)
    coords = [0] * len(lon)

    for i in range(len(lon)):
        coords[i] = [lat[i], lon[i]]

    print(coords)
    print(type(coords))
    df['Coords UTM'] = coords

    if export == True:
        exportname = 'Datenbank\ConnectwithID\Erzeugung/' + name + '.csv'
        df.to_csv(exportname, sep=';', encoding='utf-8-sig', index=False, decimal=',')

    print('Fertig')

    return df


class regulatedImport():
    """Diese Klasse importiert .csv Dateien nach einem Regulierten Schemata
        Das Schema wird in einer List vorgegeben
        Nur die Spalten werden eingelesen
        Häufung von Dateien ist in Ordnung und werden gesucht"""

    def __init__(self, filename, headerList):
        self.filename = filename
        self.fileList = findoutFiles(filename)
        self.headerList = headerList
        self.i = len(self.fileList)

    def opensignleCSV(self, i):

        try:
            openfilename = self.filename + self.fileList[i]
            print(openfilename)
            df = pd.read_csv(openfilename, usecols=self.headerList, delimiter=';', decimal=',', header=0)
            # df = pd.read_csv(openfilename, delimiter=';')

            return df

        except ValueError:
            print("falsches Format")
            return False

    def openAndCompleteAllFile(self):

        dataFrame = {1: ['1', '2'], 2: ['3', '4']}

        firstDataFrame = False

        for b in range(self.i):

            try:
                openfilename = self.filename + self.fileList[b]
                print(openfilename)
                df = pd.read_csv(openfilename, usecols=self.headerList, delimiter=';', decimal=',', header=0)
                if firstDataFrame == False:
                    dataFrame = df
                    firstDataFrame = True
                else:
                    dataFrame = dataFrame.append(df, ignore_index=True)

            except ValueError:
                print("falsches Format")
                continue

        return dataFrame





class openLocationdata():
    """Diese Klasse dient zum öffnen Spezieller csv Dateien.
    Daher auch die 3 Speizifikationen"""

    def __init__(self, filename, location, maxLength):
        self.filename = filename
        self.maxLength = maxLength
        self.location = location
        self.sheetnumber = 1
        self.ID = []
        self.KreisPot = []
        self.KreisVor = []
        self.StadtPot = []
        self.StadtVor = []
        self.haPot = []
        self.haVor = []
        self.WKAPot = []
        self.WKAVor = []

    def setSheetnumber(self, neuSheet):
        if neuSheet < 5 and neuSheet > 0:
            self.sheetnumber = neuSheet
            return True

    def openSheet(self):

        for i in range(self.maxLength):

            # print('start')
            openfile = self.filename + "/" + self.location + "/Sheet" + str(self.sheetnumber) + ".csv"
            # print(openfile)
            ausnaheme = False
            zeilennummer = 1
            setPot = False
            setVor = False
            with open(openfile, mode='r', newline='\n') as SHflaeche:
                spamreader = csv.reader(SHflaeche, delimiter=',')

                for column in spamreader:
                    lengthCloumn = len(column)
                    if lengthCloumn != 7:
                        print(openfile)
                        break
                    if zeilennummer == 1:
                        self.ID.append(column[6])
                        "Funktioniert"
                    if zeilennummer == 3:
                        self.KreisPot.append(column[2])
                        self.KreisVor.append(column[6])
                        "Funktioniert"
                    if zeilennummer == 4:
                        if len(column[3]) < 2:
                            self.StadtPot.append(column[2])
                            self.StadtVor.append(column[6])
                        else:
                            self.StadtPot.append(column[3])
                            self.StadtVor.append(column[6])
                        "Funktioniert"
                    if zeilennummer == 5 and len(column[2]) > 3:
                        self.StadtPot[-1] = self.StadtPot[-1] + str(column[2])
                        ausnaheme = True
                    if zeilennummer == 5 and len(column[3]) > 3:
                        self.StadtPot[-1] = self.StadtPot[-1] + str(column[3])
                        ausnaheme = True
                    if zeilennummer == 5 and len(column[5]) > 3:
                        self.StadtVor[-1] = self.StadtVor[-1] + str(column[6])
                        ausnaheme = True
                    if zeilennummer == 5 and len(column[6]) > 3:
                        self.StadtVor[-1] = self.StadtVor[-1] + str(column[6])
                        ausnaheme = True

                    if zeilennummer == 6 and ausnaheme == False:
                        self.haPot.append(column[2])
                        self.haVor.append(column[6])
                    # if zeilennummer > 6 and ausnaheme == False:
                    # break
                    if zeilennummer == 7 and ausnaheme == True:
                        self.haPot.append(column[2])
                        self.haVor.append(column[6])
                    # if zeilennummer > 7 and ausnaheme == True:
                    # break
                    if zeilennummer == 11:
                        holecloumn = column
                        print(column)
                        matches = [match for match in holecloumn if "WKA in Betrieb" in match]
                        print(type(matches))
                        print(matches)

                        if not matches:
                            print('empty')
                        else:
                            if 'WKA in Betrieb' in column[0]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[1]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[2]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[3]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[4]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if 'WKA in Betrieb' in column[5]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if 'WKA in Betrieb' in column[6]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if setPot == True and setVor == False:
                                self.WKAVor.append('-')
                            if setPot == False and setVor == True:
                                self.WKAPot.append('-')
                            print(column)
                            print(matches)
                            break
                    if zeilennummer == 12:
                        holecloumn = column
                        print(column)
                        matches = [match for match in holecloumn if "WKA in Betrieb" in match]
                        print(type(matches))

                        print(matches)
                        if not matches:
                            print('empty')
                        else:
                            if 'WKA in Betrieb' in column[0]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[1]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[2]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[3]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[4]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if 'WKA in Betrieb' in column[5]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if 'WKA in Betrieb' in column[6]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if setPot == True and setVor == False:
                                self.WKAVor.append('-')
                            if setPot == False and setVor == True:
                                self.WKAPot.append('-')
                            print(column)
                            print(matches)
                            break
                    if zeilennummer == 13:
                        holecloumn = column
                        print(column)
                        matches = [match for match in holecloumn if "WKA in Betrieb" in match]

                        print(type(matches))
                        print(matches)
                        if not matches:
                            print('empty')
                            self.WKAPot.append('-')
                            self.WKAVor.append('-')
                            break
                        else:
                            if 'WKA in Betrieb' in column[0]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[1]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[2]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[3]:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[4]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if 'WKA in Betrieb' in column[5]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if 'WKA in Betrieb' in column[6]:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if setPot == True and setVor == False:
                                self.WKAVor.append('-')
                            if setPot == False and setVor == True:
                                self.WKAPot.append('-')
                            print(column)
                            print(matches)
                            break
                    zeilennummer += 1
            SHflaeche.close()
            self.sheetnumber += 1

        # print(self.ID, self.KreisPot, self.KreisVor, self.StadtPot, self.StadtVor, self.haPot, self.haVor)
        # print(self.ID)
        print(len(self.WKAPot))
        print(len(self.WKAVor))
        print(len(self.KreisPot))
        exportFrame = pd.DataFrame(
            {'ID': self.ID,
             'KreisPot': self.KreisPot,
             'KreisVor': self.KreisVor,
             'StadtPot': self.StadtPot,
             'StadtVor': self.StadtVor,
             'haPot': self.haPot,
             'haVor': self.haVor,
             'WKAPot': self.WKAPot,
             'WKAVor': self.WKAVor
             }
        )
        exportname = "Datenbank\Ausbauflaechen\AusbauStandorte_einzeln/" + self.location + "_reineDaten" + ".csv"
        exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False)
        return exportFrame

    def openSheetSTE(self):

        for i in range(self.maxLength):

            # print('start')
            openfile = self.filename + "/" + self.location + "/Sheet" + str(self.sheetnumber) + ".csv"
            # print(openfile)
            ausnaheme = False
            zeilennummer = 1

            with open(openfile, mode='r', newline='\n') as SHflaeche:
                spamreader = csv.reader(SHflaeche, delimiter=',')
                setPot = False
                setVor = False
                for column in spamreader:
                    lengthCloumn = len(column)
                    if lengthCloumn != 5:
                        print(openfile)
                        break
                    if zeilennummer == 1:
                        if len(column[2]) < 5:
                            self.ID.append(column[4])
                        else:
                            self.ID.append(column[2])
                        "Funktioniert"
                    if zeilennummer == 3:
                        self.KreisPot.append(column[2])
                        self.KreisVor.append(column[4])
                        "Funktioniert"
                    if zeilennummer == 4:
                        """if len(column[3]) < 2:
                            self.StadtPot.append(column[2])
                            self.StadtVor.append(column[4])"""
                        "else:"
                        self.StadtPot.append(column[2])
                        self.StadtVor.append(column[4])
                        "Funktioniert"
                    if zeilennummer == 5 and len(column[1]) > 3 and len(column[2]) == 0:
                        self.StadtPot[-1] = self.StadtPot[-1] + str(column[1])
                        ausnaheme = True
                    """if zeilennummer == 5 and len(column[3]) > 3:
                            self.StadtPot[-1] = self.StadtPot[-1] + str(column[3])
                            ausnaheme = True"""
                    if zeilennummer == 5 and len(column[3]) > 3 and len(column[4]) == 0:
                        self.StadtVor[-1] = self.StadtVor[-1] + str(column[3])
                        ausnaheme = True
                    """if zeilennummer == 5 and len(column[5]) > 3:
                            self.StadtVor[-1] = self.StadtVor[-1] + str(column[6])
                            ausnaheme = True"""

                    if zeilennummer == 6 and ausnaheme == False:
                        self.haPot.append(column[2])
                        self.haVor.append(column[4])

                    if zeilennummer == 7 and ausnaheme == True:
                        self.haPot.append(column[2])
                        self.haVor.append(column[4])

                    if zeilennummer == 10 or zeilennummer == 11 or zeilennummer == 12 or zeilennummer == 13 or zeilennummer == 14:
                        holecloumn = column
                        print(column)
                        matches = [match for match in holecloumn if "WKA in Betrieb" in match]
                        print(type(matches))
                        lengthmatches = matches.__len__()
                        print(matches)
                        if not matches:
                            print('empty')

                            if zeilennummer < 14:
                                zeilennummer += 1
                                continue
                        else:
                            if 'WKA in Betrieb' in column[0] and setPot == False:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[1] and setPot == False:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[2] and setPot == False:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True
                            if 'WKA in Betrieb' in column[3] and setVor == False:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if 'WKA in Betrieb' in column[4] and setVor == False:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if lengthmatches > 1 and setPot == True and setVor == False:
                                self.WKAVor.append('WKA in Betrieb')
                                setVor = True
                            if lengthmatches > 1 and setVor == True and setPot == False:
                                self.WKAPot.append('WKA in Betrieb')
                                setPot = True

                            print(column)
                            print(matches)

                        if (setPot == True and setVor == True):
                            break

                        if zeilennummer == 14:

                            if setPot == True and setVor == False:
                                self.WKAVor.append('-')
                            if setPot == False and setVor == True:
                                self.WKAPot.append('-')
                            if setPot == False and setVor == False:
                                self.WKAPot.append('-')
                                self.WKAVor.append('-')
                            break

                    zeilennummer += 1
            SHflaeche.close()
            self.sheetnumber += 1

        # print(self.ID, self.KreisPot, self.KreisVor, self.StadtPot, self.StadtVor, self.haPot, self.haVor)
        # print(self.ID)
        print(len(self.WKAPot))
        print(len(self.WKAVor))
        print(len(self.KreisPot))

        exportFrame = pd.DataFrame(
            {'ID': self.ID,
             'KreisPot': self.KreisPot,
             'KreisVor': self.KreisVor,
             'StadtPot': self.StadtPot,
             'StadtVor': self.StadtVor,
             'haPot': self.haPot,
             'haVor': self.haVor,
             'WKAPot': self.WKAPot,
             'WKAVor': self.WKAVor
             }
        )
        exportname = "Datenbank\Ausbauflaechen\AusbauStandorte_einzeln/" + self.location + "_reineDatenSpecial" + ".csv"
        exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False)
        return exportFrame

    def opensingelSheetSpecial(self, sheet):

        # print('start')
        openfile = self.filename + "/" + self.location + "/Sheet" + str(sheet) + ".csv"
        # print(openfile)
        ausnaheme = False
        zeilennummer = 1
        setPot = False
        setVor = False
        with open(openfile, mode='r', newline='\n') as SHflaeche:
            spamreader = csv.reader(SHflaeche, delimiter=',')

            for column in spamreader:
                lengthCloumn = len(column)
                if lengthCloumn != 5:
                    print(openfile)
                    break
                if zeilennummer == 1:
                    if len(column[2]) < 5:
                        self.ID.append(column[4])
                    else:
                        self.ID.append(column[2])
                    "Funktioniert"
                if zeilennummer == 3:
                    self.KreisPot.append(column[2])
                    self.KreisVor.append(column[4])
                    "Funktioniert"
                if zeilennummer == 4:
                    """if len(column[3]) < 2:
                        self.StadtPot.append(column[2])
                        self.StadtVor.append(column[4])"""
                    "else:"
                    self.StadtPot.append(column[2])
                    self.StadtVor.append(column[4])
                    "Funktioniert"
                if zeilennummer == 5 and len(column[1]) > 3 and len(column[2]) == 0:
                    self.StadtPot[-1] = self.StadtPot[-1] + str(column[1])
                    ausnaheme = True
                """if zeilennummer == 5 and len(column[3]) > 3:
                        self.StadtPot[-1] = self.StadtPot[-1] + str(column[3])
                        ausnaheme = True"""
                if zeilennummer == 5 and len(column[3]) > 3 and len(column[4]) == 0:
                    self.StadtVor[-1] = self.StadtVor[-1] + str(column[3])
                    ausnaheme = True
                """if zeilennummer == 5 and len(column[5]) > 3:
                        self.StadtVor[-1] = self.StadtVor[-1] + str(column[6])
                        ausnaheme = True"""

                if zeilennummer == 6 and ausnaheme == False:
                    self.haPot.append(column[2])
                    self.haVor.append(column[4])

                if zeilennummer == 7 and ausnaheme == True:
                    self.haPot.append(column[2])
                    self.haVor.append(column[4])
                if zeilennummer == 11:
                    holecloumn = column
                    print(column)
                    matches = [match for match in holecloumn if "WKA in Betrieb" in match]
                    print(type(matches))
                    print(matches)

                    if not matches:
                        print('empty')
                    else:
                        if 'WKA in Betrieb' in column[0]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[1]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[2]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[3]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[4]:
                            self.WKAVor.append('WKA in Betrieb')
                            setVor = True
                        if 'WKA in Betrieb' in column[5]:
                            self.WKAVor.append('WKA in Betrieb')
                            setVor = True
                        if 'WKA in Betrieb' in column[6]:
                            self.WKAVor.append('WKA in Betrieb')
                        if setPot == True and setVor == False:
                            self.WKAVor.append('-')
                        if setPot == False and setVor == True:
                            self.WKAPot.append('-')
                        print(column)
                        print(matches)
                        break
                if zeilennummer == 12:
                    holecloumn = column
                    print(column)
                    matches = [match for match in holecloumn if "WKA in Betrieb" in match]
                    print(type(matches))

                    print(matches)
                    if not matches:
                        print('empty')
                    else:
                        if 'WKA in Betrieb' in column[0]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[1]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[2]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[3]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[4]:
                            self.WKAVor.append('WKA in Betrieb')
                            setVor = True
                        if 'WKA in Betrieb' in column[5]:
                            self.WKAVor.append('WKA in Betrieb')
                            setVor = True
                        if 'WKA in Betrieb' in column[6]:
                            self.WKAVor.append('WKA in Betrieb')
                            setVor = True
                        if setPot == True and setVor == False:
                            self.WKAVor.append('-')
                        if setPot == False and setVor == True:
                            self.WKAPot.append('-')
                        print(column)
                        print(matches)
                        break
                if zeilennummer == 13:
                    holecloumn = column
                    print(column)
                    matches = [match for match in holecloumn if "WKA in Betrieb" in match]

                    print(type(matches))
                    print(matches)
                    if not matches:
                        print('empty')
                        self.WKAPot.append('-')
                        self.WKAVor.append('-')
                        break
                    else:
                        if 'WKA in Betrieb' in column[0]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[1]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[2]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[3]:
                            self.WKAPot.append('WKA in Betrieb')
                            setPot = True
                        if 'WKA in Betrieb' in column[4]:
                            self.WKAVor.append('WKA in Betrieb')
                            setVor = True
                        if 'WKA in Betrieb' in column[5]:
                            self.WKAVor.append('WKA in Betrieb')
                            setVor = True
                        if 'WKA in Betrieb' in column[6]:
                            self.WKAVor.append('WKA in Betrieb')
                            setVor = True
                        if setPot == True and setVor == False:
                            self.WKAVor.append('-')
                        if setPot == False and setVor == True:
                            self.WKAPot.append('-')
                        print(column)
                        print(matches)
                        break

                zeilennummer += 1
        SHflaeche.close()
        self.sheetnumber += 1

        print(len(self.WKAPot))
        print(len(self.WKAVor))
        print(len(self.KreisPot))
        exportFrames = pd.DataFrame(
            {'ID': self.ID,
             'KreisPot': self.KreisPot,
             'KreisVor': self.KreisVor,
             'StadtPot': self.StadtPot,
             'StadtVor': self.StadtVor,
             'haPot': self.haPot,
             'haVor': self.haVor,
             'WKAPot': self.WKAPot,
             'WKAVor': self.WKAVor
             }
        )
        exportname = "Datenbank\Ausbauflaechen\AusbauStandorte_einzeln/" + self.location + "_reineDatenSpecial" + str(
            sheet) + ".csv"
        exportFrames.to_csv(exportname, sep=';', encoding='utf-8', index=False)
        return exportFrames
