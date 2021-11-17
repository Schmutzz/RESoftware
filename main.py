import pandas as pd

import database
import database as db
import geo as gpd
import internetDownload as itd
import sandbox
import logik as lgk

def openAusbauflaechen():
    """Import Erzeugungsflächen"""
    ortschaften = ['DIT', 'LAU', 'NFL', 'OHS', 'PIN', 'PLO', 'RDE', 'SEG', 'SLF', 'STE', 'STO']
    sheetanzahl = [101, 88, 129, 83, 16, 24, 169, 94, 123, 112, 25]

    print('Main Start')
    dit = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).openSheet()
    dit53 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).opensingelSheetSpecial(53)
    dit57 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).opensingelSheetSpecial(57)
    dit59 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).opensingelSheetSpecial(59)
    lau = db.openLocationdata('Import\Standort', ortschaften[1], sheetanzahl[1]).openSheet()
    nfl = db.openLocationdata('Import\Standort', ortschaften[2], sheetanzahl[2]).openSheet()
    ohs = db.openLocationdata('Import\Standort', ortschaften[3], sheetanzahl[3]).openSheet()
    pin = db.openLocationdata('Import\Standort', ortschaften[4], sheetanzahl[4]).openSheet()
    plo = db.openLocationdata('Import\Standort', ortschaften[5], sheetanzahl[5]).openSheet()
    rde = db.openLocationdata('Import\Standort', ortschaften[6], sheetanzahl[6]).openSheet()
    seg = db.openLocationdata('Import\Standort', ortschaften[7], sheetanzahl[7]).openSheet()
    slf = db.openLocationdata('Import\Standort', ortschaften[8], sheetanzahl[8]).openSheet()
    ste = db.openLocationdata('Import\Standort', ortschaften[9], sheetanzahl[9]).openSheetSTE()
    sto = db.openLocationdata('Import\Standort', ortschaften[10], sheetanzahl[10]).openSheet()

    "DataFrames zusammenführen und eine .csv Datei erstellen"

    merge_df = dit.append(dit53, ignore_index=True)
    print(merge_df["ID"])
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

    exportname = "Datenbank/Wind/AusbauStandorte_gesamt_SH/" + "AlleStandorte" + ".csv"
    merge_df.to_csv(exportname, sep=';', encoding='utf-8', index=False)

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
#sandbox.testMail()
#liste = database.findoutFiles('Datenbank\Wetter\WindZipDateien')
#for i in range(len(liste)):
   #zipfilename = 'Datenbank\Wetter\WindZipDateien/' + liste[i]
    #database.zipentpacken(zipfilename, 'Wind')

#database.testTxtWetterdatenWindToCSV(2019)
#.testTxtWetterdatenWindToCSV(2020)



def ablauf2019():
    lgk.erzeugungsdatenEEAnlagen(2019, 'Wind', 'HH')
    lgk.erzeugungsdatenEEAnlagen(2019, 'Wind', 'SH')
    lgk.erzeugungsdatenEEAnlagen(2019, 'PV', 'SH')
    lgk.erzeugungsdatenEEAnlagen(2019, 'PV', 'HH')

def ablauf2020():
    lgk.erzeugungsdatenEEAnlagen(2020, 'Wind', 'HH')
    lgk.erzeugungsdatenEEAnlagen(2020, 'Wind', 'SH')
    lgk.erzeugungsdatenEEAnlagen(2020, 'PV', 'SH')
    lgk.erzeugungsdatenEEAnlagen(2020, 'PV', 'HH')


ablauf2019()
print('end')




