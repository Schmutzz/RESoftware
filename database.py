import pandas as pd
import csv



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













