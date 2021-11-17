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
    print('Start')

    Datumabgleich = []

    hourly2019_2020 = pd.date_range('01.01.'+str(Year)+' 00:00', '31.12.'+str(Year)+' 23:00', freq='60min')

    for i in range(len(hourly2019_2020)):
        Datumabgleich.append(hourly2019_2020[i])

    files = findoutFiles('Datenbank\Wetter\WindText')

    hoursInYear = Datumabgleich.__len__()

    matches = [match for match in files if "produkt_ff_stunde" in match]
    print(matches)

    length = matches.__len__()
    firsttime = True
    for i in range(length):
        windgeschwindigkeit = []
        windausrichtung = []
        try:
            openfilename = 'Datenbank\Wetter\WindText/' + matches[i]
            print(openfilename)
            df = pd.read_csv(openfilename, delimiter=';', decimal='.', header=0)
        except ValueError:
            print("falsches Format")
            print(matches[i] + "nicht in der Liste")
            continue
        Wind_MproS = 'Wind_m/s_' + str(df['STATIONS_ID'][2])
        Wind_grad = 'Wind_grad_' + str(df['STATIONS_ID'][2])
        importLength = df.__len__()
        #print(df)
        start = 0
        for k in range(importLength):
            if start >= hoursInYear:
                break
            #print('.')
            datetime_object = datetime.strptime(str(df['MESS_DATUM'][k]), '%Y%m%d%H')
            try:
                if Datumabgleich[0] < datetime_object and datetime_object != Datumabgleich[start]:
                    print('fehlender Messert')

                    while datetime_object != Datumabgleich[start]:
                        print('.')
                        #print(Datumabgleich[start])
                        windgeschwindigkeit.append(-999)
                        windausrichtung.append(-999)
                        start += 1
            except IndexError:
                print('Pause')
            if start >= hoursInYear:
                break
            if datetime_object == Datumabgleich[start]:
                #print('Die beiden nächsten')
                #print(Datumabgleich[start])
                #print(datetime_object)
                windgeschwindigkeit.append(df['   F'][k])
                windausrichtung.append(df['   D'][k])
                start += 1
                continue

        #print(str(start) + openfilename)

        if firsttime == True:
            firsttime = False
            exportFrame = pd.DataFrame(
                {   'Datum':Datumabgleich,
                    Wind_MproS: windgeschwindigkeit,
                    Wind_grad: windausrichtung
                }
            )

            continue
        if firsttime == False:
            exportFrame[Wind_MproS] = windgeschwindigkeit
            exportFrame[Wind_grad] = windausrichtung
            print(exportFrame)


    exportname = 'Datenbank\Wetter/WindWetterdaten_'+str(Year)+'.csv'
    exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')

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


















