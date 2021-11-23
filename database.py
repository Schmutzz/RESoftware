import pandas as pd
import csv
import os
from datetime import datetime
from zipfile import ZipFile

def findoutFiles(filename):
    print("Suche beginnt")
    files = os.listdir(filename)
    print(files)
    print(len(files))

    return files
def zipentpacken(zipFileName,source):
    try:
        with ZipFile(zipFileName, 'r') as zip:
            zip.extractall('Datenbank\Wetter/' + source + 'Text')
            print('File is unzipped in temp Datenbank\Wetter\WindText')

    except ValueError:
        print("Probleme mit der Zip-Datei")
    except BaseException:
        print("is not a Zipfile")
def dateList_dataFrame(start,stop,freq, list=False):
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

def testErzeugungszusammenfassungSolar(Year, state, source, avarage= True, weatherConnect = True):
    """Diese Funktion addiert alle Solarleistung aus einer Datei vor dem angegeben Jahr.
    Die Leistung im angegeben Jahr werden halbiert um die Mitte des bestcase/worstcase zu erreichen
    Die Leistungen werden nach Wetterstationen sortiert."""

    "Dataframe Listen vorbereitung"
    Erzeugungsjahr = []
    LeistungBisJahr = []
    LeistungInJahr = []
    LeistungGesamt = []
    WetterStation = []
    print('Start testErzeugungszusammenfassungSolar ')
    if weatherConnect == True:
        weatherIDConnect = 'zugeordnet'
    if weatherConnect == False:
        weatherIDConnect = 'gewichtet'

    Datumabgleich = dateList_dataFrame('01.01.' + str(Year-1),
                                       '01.01.' + str(Year+1), 'Y', list=True)
    lengthDatumabgleich = Datumabgleich.__len__()
    print(Datumabgleich)
    #2021 muss ersetzt werden durch Zeitfunktion
    filelist = findoutFiles('Datenbank\ConnectwithID\TEST')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(2021) in match]
    matchfilelist4 = [match for match in matchfilelist3 if weatherIDConnect in match]

    try:
        headerlistLokation = ['Nettonennleistung der Einheit', 'Inbetriebnahmedatum der Einheit', 'Wetter-ID_Head']
        openfilename1 = 'Datenbank\ConnectwithID\TEST/' + matchfilelist4[0]
        print(openfilename1)

        lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal='.',
                                     header=0, encoding='latin1')

        lengthLokationsDaten = lokationsdaten.__len__()
        print(lokationsdaten)
    except ValueError:
        print("falsches Format")

    #print(lokationsdaten['Wetter-ID_Head'].describe())

    for k in lokationsdaten['Wetter-ID_Head']:

        summeBisYear = 0
        SummeInYear = 0

        for j in range(lengthLokationsDaten):
            datetime_object = datetime.strptime(str(lokationsdaten['Inbetriebnahmedatum der Einheit'][j]), '%d.%m.%Y')

            if datetime_object <= Datumabgleich[0] and k == lokationsdaten['Wetter-ID_Head'][j]:
                summeBisYear += lokationsdaten['Nettonennleistung der Einheit'][j]

            if datetime_object > Datumabgleich[0] and datetime_object < Datumabgleich[1] and k == lokationsdaten['Wetter-ID_Head'][j]:
                SummeInYear += lokationsdaten['Nettonennleistung der Einheit'][j]

        SummeInYear /= 2
        Erzeugungsjahr.append(Year)
        LeistungBisJahr.append(summeBisYear)
        LeistungInJahr.append(SummeInYear)
        LeistungGesamt.append(summeBisYear + SummeInYear)
        WetterStation.append(k)

        """"IN BEARBEITUNG NOCH NICHT FERTIG"""








def testTxtWetterdatenSolarToCSV():
    print('Start')
    files = findoutFiles('Datenbank\Wetter\SolarText')
    dataFrame = {1: ['1', '2'], 2: ['3', '4']}
    header = ['STATIONS_ID', 'ZENIT', 'MESS_DATUM_WOZ', 'FG_LBERG']
    firstDataFrame = False

    matches = [match for match in files if "produkt_st_stunde" in match]
    print(matches)

    length = matches.__len__()

    for i in range(length):

        #try:
        openfilename = 'Datenbank\Wetter\SolarText/' + matches[i]
        print(openfilename)
        df = pd.read_csv(openfilename, usecols=header, delimiter=';', decimal='.', header=0)

        #if firstDataFrame == False:
           # dataFrame = df
          #  firstDataFrame = True

      #  else:
            #dataFrame.merge(right=df, left_index=True, how='cross', right_on='MESS_DATUM_WOZ')
            #dataFrame.merge(right=df, how='cross')
            #print(dataFrame)

        exportname = "erzeugungsdatenVersuche" + str(i) + ".csv"
        df.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

        #except ValueError:
            #print("falsches Format")



    print(df)

def testTxtWetterdatenWindToCSV(Year):
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
        #print(df)
        start = 0
        falseExpiry = 0
        trueExpiry = 0
        "Um fehlende Messwerte sinnvoll zu füllen wird der Zeitpunktunt in 7 vergangenen Punkten angeschaut"
        "1 Tag / 2 Tage /3 Tage /1 Jahr /1 Jahr + 1 Tag / 1 Jahr +2 Tage /1 Jahr + 3 Tage"
        "Es wird dann aus diesen Daten ein mittel gebildet. Sollte ein Wert fehlen wir dieser ignoriert"
        "Gibt es gar keine Werte wird -999 eingetragen"

        lostWeatherValue = [24, 48, 72, 8760, 8784, 8808, 17616, 17520, 17568, 17616 ]

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
                            asd = datetime.strptime(str(df['MESS_DATUM'][k-j]), '%Y%m%d%H')
                            #print(asd)
                            #print(datetime_object)
                            #print(df['   F'][k - j])
                            #print(df['   D'][k - j])
                            "Eintragen wenn die Messwerte Falsch sind "
                            if df['   F'][k-j] > -999 and df['   D'][k - j] > -999:
                                substituteWeather.append(df['   F'][k - j])
                                substituteDegree.append(df['   D'][k - j])
                            "Anzahl der Eintragungen"
                        lengthOfsubstituteWeather = len(substituteWeather)
                        lengthOfsubstituteDegree = len(substituteDegree)
                        "Fehler wenn kein Eintrag erfolgt ist"
                        if lengthOfsubstituteWeather == 0 or lengthOfsubstituteDegree ==0:
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
                        falseExpiry +=1
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
                    if (k-j) < 0:
                        continue
                    asd = datetime.strptime(str(df['MESS_DATUM'][k - j]), '%Y%m%d%H')
                    #print(asd)
                    #print(datetime_object)
                    #print(df['   F'][k - j])
                    #print(df['   D'][k - j])
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
                start +=1

            if datetime_object == Datumabgleich[start]:
                #print('Die beiden nächsten')
                #print(Datumabgleich[start])
                #print(datetime_object)
                windMperS.append(df['   F'][k])
                windDegree.append(df['   D'][k])
                start += 1
                trueExpiry += 1
                continue

        #print(str(start) + openfilename)
        AnzahlDaten.append(start)
        DatenTrue.append(trueExpiry)
        DatenFalse.append(falseExpiry)
        DatenProzent.append(trueExpiry/start)

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
            #print(exportFrame)



    KontrolFrame = pd.DataFrame(
        {'DatenName': FilesName,
         'Daten eingelesen': FilesTrueFalse,
         'Daten Anzahl': AnzahlDaten,
         'Daten Richtig': DatenTrue,
         'Daten Falsch': DatenFalse,
         'Daten in Prozent': DatenProzent
         }
    )

    exportname1 = 'WindWetterdaten_'+str(Year)+'.csv'
    exportFrame.to_csv(exportname1, sep=';', encoding='utf-8', index=False, decimal=',')
    exportname2 = 'Datenauswertung.csv'
    KontrolFrame.to_csv(exportname2, sep=';', encoding='utf-8', index=False, decimal=',')
    print('Fertig')


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




    def opensignleCSV(self,i):

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

        dataFrame= {1: ['1', '2'], 2: ['3', '4']}

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

class importValues():

    def __init__(self, x):
        self.x = x

    def openCSV(self):
        df = pd.read_csv('ImportDatei\Import_CDR_Report_08_2021.csv', sep=';')
        print(self.x)
        return df

    def writeCSV(self):

        PrintData = {'col1':[1,2],'col2':[2,3]}
        export_csv = pd.DataFrame(data=PrintData)
        egal = export_csv.to_csv('ExportDatei\ichsuchedich.csv', sep=';', index=False, header=True)

    def openCSVfile(self):
        print('start')
        with open('ImportDatei\Import_CDR_Report_08_2021.csv', mode='r', newline='\n') as dataHH:
            spamreader = csv.reader(dataHH, delimiter=';')

            ##importcolumn = sum(1 for row in dataHH)
            ImportDaten = []
            MeterStart = []
            MeterStop = []
            TimeStart = []
            TimeStop = []


            for column in spamreader:
                ImportDaten.append(column[4])
                print(column[4])
                MeterStart.append(column[19])
                MeterStop.append(column[20])
                TimeStart.append(column[22])
                TimeStop.append(column[23])


            print('lilalu')


        dataHH.close()
    def openCSVfileTEST(self):
        print('start')
        with open('ImportDatei\ImportROHDaten.csv', mode='r', newline='\n') as dataHH:
            spamreader = csv.reader(dataHH, delimiter=';')

            for column in spamreader:
                print(column)

            print('lilalu')


        dataHH.close()

class openLocationdata():

    """Diese Klasse dient zum öffnen Spezieller csv Dateien.
    Daher auch die 3 Speizifikationen"""

    def __init__(self, filename, location,maxLength):
        self.filename = filename
        self.maxLength =maxLength
        self.location = location
        self.sheetnumber = 1
        self.ID = []
        self.KreisPot = []
        self.KreisVor = []
        self.StadtPot = []
        self.StadtVor = []
        self.haPot = []
        self.haVor = []

    def setSheetnumber(self, neuSheet):
        if neuSheet < 5 and neuSheet > 0:
            self.sheetnumber = neuSheet
            return True

    def openSheet(self):

        for i in range(self.maxLength):

            #print('start')
            openfile = self.filename + "/" + self.location + "/Sheet" + str(self.sheetnumber) + ".csv"
            #print(openfile)
            ausnaheme = False
            zeilennummer = 1

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
                    if zeilennummer > 6 and ausnaheme == False:
                        break
                    if zeilennummer == 7 and ausnaheme == True:
                        self.haPot.append(column[2])
                        self.haVor.append(column[6])
                    if zeilennummer > 7 and ausnaheme == True:
                        break

                    zeilennummer += 1
            SHflaeche.close()
            self.sheetnumber +=1

        #print(self.ID, self.KreisPot, self.KreisVor, self.StadtPot, self.StadtVor, self.haPot, self.haVor)
        #print(self.ID)

        exportFrame = pd.DataFrame(
            {'ID': self.ID,
             'KreisPot': self.KreisPot,
             'KreisVor': self.KreisVor,
             'StadtPot': self.StadtPot,
             'StadtVor': self.StadtVor,
             'haPot': self.haPot,
             'haVor': self.haVor
            }
        )
        exportname = "Datenbank/Wind/AusbauStandorte_einzeln/" + self.location + "_reineDaten" + ".csv"
        exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False)
        return exportFrame

    def openSheetSTE(self):

        for i in range(self.maxLength):

            #print('start')
            openfile = self.filename + "/" + self.location + "/Sheet" + str(self.sheetnumber) + ".csv"
            #print(openfile)
            ausnaheme = False
            zeilennummer = 1

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
                    if zeilennummer > 6 and ausnaheme == False:
                        break
                    if zeilennummer == 7 and ausnaheme == True:
                        self.haPot.append(column[2])
                        self.haVor.append(column[4])
                    if zeilennummer > 7 and ausnaheme == True:
                        break

                    zeilennummer += 1
            SHflaeche.close()
            self.sheetnumber +=1

        #print(self.ID, self.KreisPot, self.KreisVor, self.StadtPot, self.StadtVor, self.haPot, self.haVor)
        #print(self.ID)

        exportFrame = pd.DataFrame(
            {'ID': self.ID,
             'KreisPot': self.KreisPot,
             'KreisVor': self.KreisVor,
             'StadtPot': self.StadtPot,
             'StadtVor': self.StadtVor,
             'haPot': self.haPot,
             'haVor': self.haVor
            }
        )
        exportname = "Datenbank/Wind/AusbauStandorte_einzeln/" + self.location + "_reineDatenSpecial" + ".csv"
        exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False)
        return exportFrame

    def opensingelSheetSpecial(self, sheet):

        # print('start')
        openfile = self.filename + "/" + self.location + "/Sheet" + str(sheet) + ".csv"
        # print(openfile)
        ausnaheme = False
        zeilennummer = 1

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
                if zeilennummer > 6 and ausnaheme == False:
                    break
                if zeilennummer == 7 and ausnaheme == True:
                    self.haPot.append(column[2])
                    self.haVor.append(column[4])
                if zeilennummer > 7 and ausnaheme == True:
                    break

                zeilennummer += 1
        SHflaeche.close()
        self.sheetnumber += 1

        exportFrames = pd.DataFrame(
        {'ID': self.ID,
         'KreisPot': self.KreisPot,
         'KreisVor': self.KreisVor,
         'StadtPot': self.StadtPot,
         'StadtVor': self.StadtVor,
         'haPot': self.haPot,
         'haVor': self.haVor
            }
        )
        exportname = "Datenbank/Wind/AusbauStandorte_einzeln/" + self.location + "_reineDatenSpecial" + str(sheet) + ".csv"
        exportFrames.to_csv(exportname, sep=';', encoding='utf-8', index=False)
        return exportFrames


















