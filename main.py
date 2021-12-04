import pandas as pd

import database
import database as db
import geo as gpd
import internetDownload as itd
import sandbox

import logik as lgk

def openAusbauflaechen(export=True):
    """Import Erzeugungsflächen"""
    ortschaften = ['DIT', 'LAU', 'NFL', 'OHS', 'PIN', 'PLO', 'RDE', 'SEG', 'SLF', 'STE', 'STO']
    sheetanzahl = [101, 88, 129, 83, 16, 24, 169, 94, 123, 112, 25]

    print('Main Start')
    dit = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).openSheet()
    summe = dit.shape[0]

    dit53 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).opensingelSheetSpecial(53)
    summe +=dit53.shape[0]
    dit57 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).opensingelSheetSpecial(57)
    summe += dit57.shape[0]
    dit59 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).opensingelSheetSpecial(59)
    summe += dit59.shape[0]
    lau = db.openLocationdata('Import\Standort', ortschaften[1], sheetanzahl[1]).openSheet()
    summe += lau.shape[0]
    nfl = db.openLocationdata('Import\Standort', ortschaften[2], sheetanzahl[2]).openSheet()
    summe += nfl.shape[0]
    ohs = db.openLocationdata('Import\Standort', ortschaften[3], sheetanzahl[3]).openSheet()
    summe += ohs.shape[0]
    pin = db.openLocationdata('Import\Standort', ortschaften[4], sheetanzahl[4]).openSheet()
    summe += pin.shape[0]
    plo = db.openLocationdata('Import\Standort', ortschaften[5], sheetanzahl[5]).openSheet()
    summe += plo.shape[0]
    rde = db.openLocationdata('Import\Standort', ortschaften[6], sheetanzahl[6]).openSheet()
    summe += rde.shape[0]
    seg = db.openLocationdata('Import\Standort', ortschaften[7], sheetanzahl[7]).openSheet()
    summe += seg.shape[0]
    slf = db.openLocationdata('Import\Standort', ortschaften[8], sheetanzahl[8]).openSheet()
    summe += slf.shape[0]
    ste = db.openLocationdata('Import\Standort', ortschaften[9], sheetanzahl[9]).openSheetSTE()
    summe += ste.shape[0]
    sto = db.openLocationdata('Import\Standort', ortschaften[10], sheetanzahl[10]).openSheet()
    summe += sto.shape[0]
    print('Hier ist die Summe der Reihen', summe)

    "DataFrames zusammenführen und eine .csv Datei erstellen"

    merge_df = dit.append(dit53, ignore_index=True)
    #print(merge_df["ID"])
    merge_df = merge_df.append(dit57, ignore_index=True)
    merge_df = merge_df.append(dit59, ignore_index=True)
    merge_df = merge_df.append(lau, ignore_index=True)
    merge_df = merge_df.append(nfl, ignore_index=True)
    merge_df = merge_df.append(ohs, ignore_index=True)
    merge_df = merge_df.append(pin, ignore_index=True)
    merge_df = merge_df.append(plo, ignore_index=True)
    merge_df = merge_df.append(rde, ignore_index=True)
    merge_df = merge_df.append(seg, ignore_index=True)
    merge_df = merge_df.append(slf, ignore_index=True)
    merge_df = merge_df.append(ste, ignore_index=True)
    merge_df = merge_df.append(sto, ignore_index=True)
    #merge_df['haPot'] = merge_df['haPot'].map({'-': '0'})
    #merge_df['haVor'] = merge_df['haVor'].map({'-': '0'})
    #merge_df.loc[merge_df.haPot == '-'] = '0'
    #merge_df.loc[merge_df.haVor == '-'] = '0'
    merge_df['haPot'] = merge_df['haPot'].replace(['-'], '0')
    merge_df['haVor'] = merge_df['haVor'].replace(['-'], '0')

    if export == True:
        print('Export')
        exportname = "Datenbank\Ausbauflaechen\AusbauStandorte_gesamt_SH/" + "AlleStandorte" + ".csv"
        merge_df.to_csv(exportname, sep=';', encoding='utf-8-sig', index=False)

def testGPD():
    a = gpd.SingleLocation("Bietigheim-Bissingen", "74321")
    print(a.getRaw())
    liste = ["Bietigheim-Bissingen", "Asperg","Ingersheim", "Ludwigsburg", "Heimfeld"]
    b = gpd.Multiple(liste,"Deutschland")

def testStandartImport():
    standartListe = ["Date", "Time", "Cons_Prod", "Location", "Energynetwork", "Energy_in_kWh", "Energysource"]
    egal = db.regulatedImport('Import\Erzeugung/', standartListe).openAndCompleteAllFile()
    "Überprüfung der Daten Fehlt"
    exportname = "Datenbank\Erzeugung/" + "erzeugungsdatenVersuche" + ".csv"
    egal.to_csv(exportname, sep=';', encoding='utf-8', index=False)
    print(egal)

#openAusbauflaechen()
#testGPD()
#testStandartImport()
#itd.cdcdataobservations_germanyHourly('wind', 'StundeWindStationen')
#itd.cdcdataobservations_germanyHourly('solar', 'StundeSolarStationen')

#liste = database.findoutFiles('Datenbank\Wetter\WindZipDateien')
#for i in range(len(liste)):
   #zipfilename = 'Datenbank\Wetter\WindZipDateien/' + liste[i]
    #database.zipentpacken(zipfilename, 'Wind')

#database.TxtWetterdatenToCSV(2019, 'PV')
#database.TxtWetterdatenToCSV(2019, 'Wind')
#database.TxtWetterdatenToCSV(2020, 'PV')
#database.TxtWetterdatenToCSV(2020, 'Wind')



def ablauf2019():
    print('2019')
    lgk.erzeugungsdatenEEAnlagen(2019, 'Wind', 'HH')
    lgk.erzeugungsdatenEEAnlagen(2019, 'Wind', 'SH')
    lgk.erzeugungsdatenEEAnlagen(2019, 'PV', 'SH')
    lgk.erzeugungsdatenEEAnlagen(2019, 'PV', 'HH')

def ablauf2020():
    print('2020')
    lgk.erzeugungsdatenEEAnlagen(2020, 'Wind', 'HH')
    lgk.erzeugungsdatenEEAnlagen(2020, 'Wind', 'SH')
    lgk.erzeugungsdatenEEAnlagen(2020, 'PV', 'SH')
    lgk.erzeugungsdatenEEAnlagen(2020, 'PV', 'HH')

#database.erzeugungsZsmPV(2019,'HH')
#database.erzeugungsZsmPV(2020,'HH')
#database.erzeugungsZsmPV(2019,'SH')
#database.erzeugungsZsmPV(2020,'SH')
#database.testErzeugungszusammenfassungSolar(2019,'HH', 'PV')
#database.testErzeugungszusammenfassungSolar(2020,'HH', 'PV')
#database.testErzeugungszusammenfassungSolar(2019,'SH', 'PV')
#database.testErzeugungszusammenfassungSolar(2020,'SH', 'PV')


#ablauf2019()
#ablauf2020()
'''
PV_2019 = lgk.erzeugungPerStunde(2019, 'PV')
PV_2020 = lgk.erzeugungPerStunde(2020, 'PV')
Wind_2019 = lgk.erzeugungPerStunde(2019, 'Wind')
Wind_2020 = lgk.erzeugungPerStunde(2020, 'Wind')
del PV_2019['Datum']
EE_Erz_2019 = pd.concat([Wind_2019, PV_2019], axis=1, sort=False)
del PV_2020['Datum']
EE_Erz_2020 = pd.concat([Wind_2020, PV_2020], axis=1, sort=False)


verbrauch_2019 = lgk.verbrauchGesamt(2019)
verbrauch_2020 = lgk.verbrauchGesamt(2020)

lgk.analyseEE(2019, EE_Erz_2019, verbrauch_2019)
lgk.analyseEE(2020, EE_Erz_2020, verbrauch_2020)

#lgk.analyseAusbauFl()'''

lgk.Windlastprofil(2019, 'Wind')
lgk.Windlastprofil(2020, 'Wind')

#print('end')
'''lilila = [1,2,3,4,5,6,9,7,5,6,84,1,3,5,4,2,1,3,5,4,8,7,49,7,6,4,1,3,4,6,4,6,46,5]
listparameter = []
falsch = []
for i in lilila:
    for k in range(35):
        if float(i) >= float(k):
            listparameter[k] += 1
        else:
            falsch[k] += 1'''










