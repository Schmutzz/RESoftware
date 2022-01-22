"""einen Platz um nicht im Restlichen Code immer rumschreiben zu müssen"""
""" Email PW: 4He3m4t#"""
"""testMaster@bietigheimer-htc.de"""

from email.mime.text import MIMEText
from email.header import Header
import smtplib
import pandas as pd
import numpy as np

def max_verkopfte_tabelle():
    '''read and convert data 2019'''
    ee_data_19 = pd.read_csv('GruenEnergie_2019.csv', sep=';', encoding='latin1')
    x_values_19 = np.arange(8760)
    pct_75_19 = [percentage_power] * 8760
    # pct_renewable_19 = ee_data_19['EE_Anteil'].tolist()
    deficit_19 = ee_data_19['Diff_EE_zu_Verb'].tolist()
    conv_power_19 = 0
    wind_power_19 = ee_data_19['Erzeugung_Wind'].tolist()
    pv_power_19 = ee_data_19['Erzeugung_PV'].tolist()
    combined_power_19 = ee_data_19['Erzeugung_Gesamt'].tolist()
    consumption_19 = ee_data_19['Verbrauch_Gesamt'].tolist()
    relevant_wind_19 = []
    pct_renewable_19 = []

    for i in range(8760):
        consumption_19[i] = float(consumption_19[i].replace(',', '.'))
        combined_power_19[i] = float(combined_power_19[i].replace(',', '.'))
        # wind_power_19_sim[i] = float(wind_power_19_sim[i].replace(',', '.'))
        pv_power_19[i] = float(pv_power_19[i].replace(',', '.'))
        deficit_19[i] = float(deficit_19[i].replace(',', '.'))
        pct_renewable_19.append(((combined_power_19[i] + biomass_hourly_19[i]) / consumption_19[i]) * 100)
        # pct_renewable_19[i] = pct_renewable_19[i].replace('%', '')
        # pct_renewable_19[i] = float(pct_renewable_19[i].replace(',', '.'))

        if deficit_19[i] < 0:
            conv_power_19 -= deficit_19[i]
    '''    if consumption_19[i] > combined_power_19[i]:
            relevant_wind_19.append(wind_power_19[i])
        else:
            relevant_wind_19.append(wind_power_19[i] - (combined_power_19[i] - consumption_19[i]))'''

    pv_sum_19 = np.sum(pv_power_19)
    conv_sum_19 = np.sum(conv_power_19)
    wind_sum_19 = np.sum(consumption_19) - conv_sum_19
    energy_mix_values_19 = [wind_sum_19, pv_sum_19, biomass_sum, conv_sum_19]

    x_ticks_19 = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]

    table_19 = pd.DataFrame(columns=headers)

    monthly_wind_19 = []
    monthly_solar_19 = []
    monthly_renewable_19 = []
    monthly_consumption_19 = []
    monthly_deficit_19 = []
    monthly_hours_19 = []
    monthly_reached_19 = []

    for i in range(len(x_ticks_19)):
        hours = 0
        real_deficit_19 = 0
        if i != 0:
            x_ticks_19[i] += x_ticks_19[i - 1]
            monthly_wind_19.append(round_sum_twh(wind_power_19[x_ticks_19[i - 1]:x_ticks_19[i]]))
            monthly_solar_19.append(round_sum_twh(pv_power_19[x_ticks_19[i - 1]:x_ticks_19[i]]))
            monthly_renewable_19.append(round_sum_twh(combined_power_19[x_ticks_19[i - 1]:x_ticks_19[i]]))
            monthly_consumption_19.append(round_sum_twh(consumption_19[x_ticks_19[i - 1]:x_ticks_19[i]]))
            # monthly_deficit_19.append(round_sum_twh(deficit_19[x_ticks_19[i - 1]:x_ticks_19[i]]))
            for j in range(x_ticks_19[i - 1], x_ticks_19[i]):
                if pct_renewable_19[j] >= percentage_power:
                    hours += 1
                if deficit_19[j] < 0:
                    real_deficit_19 -= deficit_19[j]
            monthly_deficit_19.append(round_twh(real_deficit_19))
            monthly_hours_19.append(hours)
            if (monthly_hours_19[i] / (x_ticks_19[i] - x_ticks_19[i - 1])) > percentage_hours / 100:
                monthly_reached_19.append('Yes')
            else:
                monthly_reached_19.append('No')

        else:
            monthly_wind_19.append(round_sum_twh(wind_power_19[0:x_ticks_19[0]]))
            monthly_solar_19.append(round_sum_twh(pv_power_19[0:x_ticks_19[0]]))
            monthly_renewable_19.append(round_sum_twh(combined_power_19[0:x_ticks_19[0]]))
            monthly_consumption_19.append(round_sum_twh(consumption_19[0:x_ticks_19[0]]))
            # monthly_deficit_19.append(round_sum_twh(deficit_19[0:x_ticks_19[0]]))
            for j in range(x_ticks_19[0]):
                if pct_renewable_19[j] >= percentage_power:
                    hours += 1
                if deficit_19[j] < 0:
                    real_deficit_19 -= deficit_19[j]
            monthly_deficit_19.append(round_twh(real_deficit_19))
            monthly_hours_19.append(hours)
            if (monthly_hours_19[0] / x_ticks_19[0]) > percentage_hours / 100:
                monthly_reached_19.append('Yes')
            else:
                monthly_reached_19.append('No')

    '''pv_sum_19 = np.sum(monthly_solar_19)
    cons_sum_19 = np.sum(monthly_consumption_19)
    conv_sum_19 = 0
    for i in range(len(monthly_deficit_19)):
        if monthly_deficit_19[i] < 0:
            conv_sum_19 -= monthly_deficit_19[i]

    wind_sum_19 = cons_sum_19 - pv_sum_19 - conv_sum_19'''

    data_19 = [months, monthly_wind_19, monthly_solar_19, monthly_renewable_19, monthly_consumption_19, monthly_deficit_19,
               monthly_hours_19, monthly_reached_19]

    last_row_19 = ['Yearly']
    last_row_19.append(round_sum(monthly_wind_19))
    last_row_19.append(round_sum(monthly_solar_19))
    last_row_19.append(round_sum(monthly_renewable_19))
    last_row_19.append(round_sum(monthly_consumption_19))
    last_row_19.append(round_sum(monthly_deficit_19))
    last_row_19.append(round_sum(monthly_hours_19))

    if (last_row_19[-1] / 8760) > percentage_hours / 100:
        last_row_19.append('Yes (' + str(round((last_row_19[-1] / 8760) * 100, 2)) + '%)')
    else:
        last_row_19.append('No (' + str(round((last_row_19[-1] / 8760) * 100, 2)) + '%)')

    for i in range(len(headers)):
        table_19[headers[i]] = data_19[i]

    table_19.loc[len(table_19)] = last_row_19
    print(table_19)

    '''read and convert data 2020'''
    ee_data_20 = pd.read_csv('GruenEnergie_2020.csv', sep=';', encoding='latin1')
    x_values_20 = np.arange(8784)
    pct_75_20 = [percentage_power] * 8784
    # pct_renewable_20 = ee_data_20['EE_Anteil'].tolist()
    deficit_20 = ee_data_20['Diff_EE_zu_Verb'].tolist()
    conv_power_20 = 0
    wind_power_20 = ee_data_20['Erzeugung_Wind'].tolist()
    pv_power_20 = ee_data_20['Erzeugung_PV'].tolist()
    combined_power_20 = ee_data_20['Erzeugung_Gesamt'].tolist()
    consumption_20 = ee_data_20['Verbrauch_Gesamt'].tolist()
    relevant_wind_20 = []
    pct_renewable_20 = []

    for i in range(8784):
        consumption_20[i] = float(consumption_20[i].replace(',', '.'))
        combined_power_20[i] = float(combined_power_20[i].replace(',', '.'))
        # wind_power_20[i] = float(wind_power_20[i].replace(',', '.'))
        pv_power_20[i] = float(pv_power_20[i].replace(',', '.'))
        deficit_20[i] = float(deficit_20[i].replace(',', '.'))
        pct_renewable_20.append(((combined_power_20[i] + biomass_hourly_20[i]) / consumption_20[i]) * 100)
        '''pct_renewable_20[i] = pct_renewable_20[i].replace('%', '')
        pct_renewable_20[i] = float(pct_renewable_20[i].replace(',', '.'))'''

        if deficit_20[i] < 0:
            conv_power_20 -= deficit_20[i]
    '''    if consumption_20[i] > combined_power_20[i]:
            relevant_wind_20.append(wind_power_20[i])
        else:
            relevant_wind_20.append(wind_power_20[i] - (combined_power_20[i] - consumption_20[i]))'''

    pv_sum_20 = np.sum(pv_power_20)
    conv_sum_20 = np.sum(conv_power_20)
    wind_sum_20 = np.sum(consumption_20) - conv_sum_20
    energy_mix_values_20 = [wind_sum_20, pv_sum_20, 2.8 * 1e9, conv_sum_20]

    x_ticks_20 = [744, 696, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]

    table_20 = pd.DataFrame(columns=headers)

    monthly_wind_20 = []
    monthly_solar_20 = []
    monthly_renewable_20 = []
    monthly_consumption_20 = []
    monthly_deficit_20 = []
    monthly_hours_20 = []
    monthly_reached_20 = []

    for i in range(len(x_ticks_20)):
        hours = 0
        real_deficit_20 = 0
        if i != 0:
            x_ticks_20[i] += x_ticks_20[i - 1]
            monthly_wind_20.append(round_sum_twh(wind_power_20[x_ticks_20[i - 1]:x_ticks_20[i]]))
            monthly_solar_20.append(round_sum_twh(pv_power_20[x_ticks_20[i - 1]:x_ticks_20[i]]))
            monthly_renewable_20.append(round_sum_twh(combined_power_20[x_ticks_20[i - 1]:x_ticks_20[i]]))
            monthly_consumption_20.append(round_sum_twh(consumption_20[x_ticks_20[i - 1]:x_ticks_20[i]]))
            # monthly_deficit_20.append(round_sum_twh(deficit_20[x_ticks_20[i - 1]:x_ticks_20[i]]))
            for j in range(x_ticks_20[i - 1], x_ticks_20[i]):
                if pct_renewable_20[j] >= percentage_power:
                    hours += 1
                if deficit_20[j] < 0:
                    real_deficit_20 -= deficit_20[j]
            monthly_deficit_20.append(round_twh(real_deficit_20))
            monthly_hours_20.append(hours)
            if (monthly_hours_20[i] / (x_ticks_20[i] - x_ticks_20[i - 1])) > percentage_hours / 100:
                monthly_reached_20.append('Yes')
            else:
                monthly_reached_20.append('No')

        else:
            monthly_wind_20.append(round_sum_twh(wind_power_20[0:x_ticks_20[0]]))
            monthly_solar_20.append(round_sum_twh(pv_power_20[0:x_ticks_20[0]]))
            monthly_renewable_20.append(round_sum_twh(combined_power_20[0:x_ticks_20[0]]))
            monthly_consumption_20.append(round_sum_twh(consumption_20[0:x_ticks_20[0]]))
            # monthly_deficit_20.append(round_sum_twh(deficit_20[0:x_ticks_20[0]]))
            for j in range(x_ticks_20[0]):
                if pct_renewable_20[j] >= percentage_power:
                    hours += 1
                if deficit_20[j] < 0:
                    real_deficit_20 -= deficit_20[j]
            monthly_deficit_20.append(round_twh(real_deficit_20))
            monthly_hours_20.append(hours)
            if (monthly_hours_20[0] / x_ticks_20[0]) > percentage_hours / 100:
                monthly_reached_20.append('Yes')
            else:
                monthly_reached_20.append('No')


    data_20 = [months, monthly_wind_20, monthly_solar_20, monthly_renewable_20, monthly_consumption_20, monthly_deficit_20,
               monthly_hours_20, monthly_reached_20]

    last_row_20 = ['Yearly']
    last_row_20.append(round_sum(monthly_wind_20))
    last_row_20.append(round_sum(monthly_solar_20))
    last_row_20.append(round_sum(monthly_renewable_20))
    last_row_20.append(round_sum(monthly_consumption_20))
    last_row_20.append(round_sum(monthly_deficit_20))
    last_row_20.append(round_sum(monthly_hours_20))

    if (last_row_20[-1] / 8760) > percentage_hours / 100:
        last_row_20.append('Yes (' + str(round((last_row_20[-1] / 8760) * 100, 2)) + '%)')
    else:
        last_row_20.append('No (' + str(round((last_row_20[-1] / 8760) * 100, 2)) + '%)')

    for i in range(len(headers)):
        table_20[headers[i]] = data_20[i]

    table_20.loc[len(table_20)] = last_row_20
    print(table_20.head())


def generation_PV_energy(year, source, state):
    exportFrame = DateList('01.01.' + str(year) + ' 00:00', '31.12.' + str(year) + ' 23:00', '60min')

    filelist = findoutFiles('Datenbank\ConnectwithID\Erzeugung')
    matchfilelist1 = [match for match in filelist if state in match]
    matchfilelist2 = [match for match in matchfilelist1 if source in match]
    matchfilelist3 = [match for match in matchfilelist2 if str(year) in match]
    print(matchfilelist3)

    try:
        openfilename2 = 'Datenbank\Wetter/' + source + '_Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)
        # print(wetterdaten)
    except ValueError:
        print("erzeugungsdaten_ee_anlagen Falsches Format")

    modellunbekannt = 0
    wetterIDunbekannt = 0
    lengthLocation2 = 0


    if source == 'PV':
        try:
            headerlistLokation = ['Leistung', 'Bundesland', 'Wetter-ID']
            openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matchfilelist3[0]
            print(openfilename1)

            lokationsdaten = pd.read_csv(openfilename1, delimiter=';', usecols=headerlistLokation, decimal=',',
                                         header=0, encoding='latin1')

            lengthLocation = lokationsdaten.__len__()
            # print(lokationsdaten)
        except ValueError:
            print("falsches Format")

        for i in range(lengthLocation):
            leistung = []
            # print(i)
            # print(str(lokationsdaten['Wetter-ID'][i]))

            matcheswetterdaten = [match for match in wetterdaten.columns.values.tolist() if
                                  str(lokationsdaten['Wetter-ID'][i]) in match]
            # print(matcheswetterdaten)
            if len(matcheswetterdaten) != 2:
                print('Fehler Wetterdaten')
                break

            columnName = str(i) + '_Ezg_PV' + '_' + str(lokationsdaten['Bundesland'][i]) + '_' + str(
                lokationsdaten['Wetter-ID'][i])

            fkt_Bestrahlung = 492.48
            fkt_Solar = 0.9

            for k in wetterdaten[matcheswetterdaten[0]]:

                if k < 0:
                    leistung.append(0)
                else:
                    # print(lokationsdaten['Bruttoleistung der Einheit'][i])
                    # print(type(lokationsdaten['Bruttoleistung der Einheit'][i]))
                    x = lokationsdaten['Leistung'][i] * (k / fkt_Bestrahlung) * fkt_Solar
                    leistung.append(x)

            # print('Eintrag bei ', i)
            exportFrame[columnName] = leistung
            # print('Eintrag Efolgreich ', i)

    exportname = 'Datenbank\Erzeugung\Einzel/Erz_' + source + '_' + state + '_' + str(year) + '.csv'
    exportFrame.to_csv(exportname, sep=';', encoding='utf-8', index=False, decimal=',')
    print("Modell ungekannt Anzahl: ", modellunbekannt)
    print("Wetter-ID ungekannt Anzahl: ", wetterIDunbekannt)
    print("Eingelesene Zeilen", lengthLocation2)
    print("Ausgegebene Zeilen", len(exportFrame.columns))

    print('Fertig')






















'''test = pd.read_csv('REE_AnalyseCompleted/REE_Analysejahr_2019_21-01-2022_18-57/REE_beforREexpansion_64_2019_18-57.csv',
                   sep=';', decimal=',', encoding='utf-8')
a = test['EE>100%'].value_counts()[1]
print(test['EE>100%'].value_counts())
print(test['EE>100%'].tolist().count(True))
'''

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



