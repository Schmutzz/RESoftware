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

def testListemiteinzelnenWerten(list):

    listeNeu = []


    for i in list:
        if i in listeNeu:
            continue
            print()
        else:
            listeNeu.append(i)


    return listeNeu









