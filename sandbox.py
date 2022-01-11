"""einen Platz um nicht im Restlichen Code immer rumschreiben zu müssen"""
""" Email PW: 4He3m4t#"""
"""testMaster@bietigheimer-htc.de"""

from email.mime.text import MIMEText
from email.header import Header
import smtplib
import pandas as pd
import numpy as np

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

def testListemiteinzelnenWerten(list):

    listeNeu = []


    for i in list:
        if i in listeNeu:
            continue
            print()
        else:
            listeNeu.append(i)


    return listeNeu

def freie_leistung_Vor(year, standort):
    print('Start freie_leistung_Vor')
    WeaModell_fl_name = 'Enercon E-82/3000'
    WeaModell_fl_leistung = 3000
    WeaModell_fl = ((15 * np.square(float(82))) / 10000)
    temp_anzahl = []
    temp_leistung = []
    temp_fl = []

    for index, i in enumerate(standort['freieVor in Vor']):

        if i > 0:
            anzahl = i / WeaModell_fl
            leistung = int(anzahl) * WeaModell_fl_leistung
            temp_anzahl.append(int(anzahl))
            temp_leistung.append(leistung)
            temp_fl.append(WeaModell_fl)
        else:
            temp_anzahl.append(0)
            temp_leistung.append(0)
            temp_fl.append(0)

    standort[WeaModell_fl_name] = temp_fl
    standort['temp_anzahl'] = temp_anzahl
    standort['temp_leistung'] = temp_leistung

    print('freie_leistung_pot')
    return standort

#rint(lgk.WKAmodell.getAnzahlWKAmodell())
class TestAlex:
    def __init__(self, x):
        self.x = x

    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, x):
        if x < 0:
            self.__x = 0
        elif x > 100:
            self.__x = 100
        else:
            self.__x = x

p1= TestAlex(999)
print(p1.x)
p2 = TestAlex(-999)
print(p2.x)
p3 = TestAlex(14)
print(p3.x)
b = p3.x
print(b)

'''
def annualOutput_WKA(year, Ein_ms, Nenn_ms, Abs_ms, leistung_Gesamt, weatherData, nabenhohe):

    temp_DatelistPerHoure = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', '60min')

    temp_wetter = wind_hochrechnung(weatherData, nabenhohe, 10)
    temp_leistung = [0] * len(temp_DatelistPerHoure)

    for index, k in enumerate(temp_wetter):

        # Fehler raus suchen
        if k < 0:
            temp_leistung[index] = 0

        # unter Nennleistung
        elif k >= Ein_ms and k < Nenn_ms:
            x = FORMEL_WKA_Leistung(Nenn_ms, Ein_ms, leistung_Gesamt, k)
            temp_leistung[index] = int(x)

        # ueber nennleistung
        elif k >= Nenn_ms and k < Abs_ms:
            temp_leistung[index] = int(leistung_Gesamt)

        # außerhalb der Betriebsgeschwindigekeit
        elif k >= Abs_ms or k < Ein_ms:
            temp_leistung[index] = 0


        else:
            print("Fehler")
            temp_leistung[index] = 0

    return temp_leistung[index]

'''

'''while (end_vergleichswert >= vergleichswert * ausbaubegrenzungsfaktor):
    'Wieviel Impact hat eine weitere WKA auf mein NegativGraph'
    tempSum_negativGraph = 0
    max_Anzahl += 1
    for index, i in enumerate(deepestPointsIndex):
        tempSum_negativGraph += deepestPointsValues[index] + (DB_WKA[modellName][i] * max_Anzahl)

    if max_Anzahl == 1:
        vergleichswert = (start_SumNegativGraph * (-1)) - (tempSum_negativGraph * (-1))
        end_vergleichswert = vergleichswert
        continue

    end_vergleichswert = ((start_SumNegativGraph * (-1)) - (tempSum_negativGraph * (-1))) / max_Anzahl
    print(end_vergleichswert)'''



