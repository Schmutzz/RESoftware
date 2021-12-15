import pandas as pd
import database as db
import geo as gpd
import internetDownload as itd
import sandbox
import logik as lgk

print('start')

#lgk.windlastprofil(2019)
#lgk.windlastprofil(2019)


def openAusbauflaechen(export=True):
    """Import Erzeugungsflächen"""
    ortschaften = ['DIT', 'LAU', 'NFL', 'OHS', 'PIN', 'PLO', 'RDE', 'SEG', 'SLF', 'STE', 'STO']
    sheetanzahl = [101, 88, 129, 83, 16, 24, 169, 94, 123, 112, 25]

    print('Main Start')
    dit = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).openSheet()
    summe = dit.shape[0]

    dit53 = db.openLocationdata('Import\Standort', ortschaften[0], sheetanzahl[0]).opensingelSheetSpecial(53)
    summe += dit53.shape[0]
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

    merge_df['haPot'] = merge_df['haPot'].replace(['-'], '0')
    merge_df['haVor'] = merge_df['haVor'].replace(['-'], '0')

    if export == True:
        print('Export')
        exportname = "Datenbank\Ausbauflaechen\AusbauStandorte_gesamt_SH/" + "AlleStandorte" + ".csv"
        merge_df.to_csv(exportname, sep=';', encoding='utf-8-sig', index=False)



def testStandartImport():
    standartListe = ["Date", "Time", "Cons_Prod", "Location", "Energynetwork", "Energy_in_kWh", "Energysource"]
    egal = db.regulatedImport('Import\Erzeugung/', standartListe).openAndCompleteAllFile()
    "Überprüfung der Daten Fehlt"
    exportname = "Datenbank\Erzeugung/" + "erzeugungsdatenVersuche" + ".csv"
    egal.to_csv(exportname, sep=';', encoding='utf-8', index=False)
    print(egal)


# openAusbauflaechen()
# testGPD()
# testStandartImport()
# itd.cdcdataobservations_germanyHourly('wind', 'StundeWindStationen')
# itd.cdcdataobservations_germanyHourly('solar', 'StundeSolarStationen')

# liste = database.findoutFiles('Datenbank\Wetter\WindZipDateien')
# for i in range(len(liste)):
# zipfilename = 'Datenbank\Wetter\WindZipDateien/' + liste[i]
# database.zipentpacken(zipfilename, 'Wind')

# database.TxtWetterdatenToCSV(2019, 'PV')
# database.TxtWetterdatenToCSV(2019, 'Wind')
# database.TxtWetterdatenToCSV(2020, 'PV')
# database.TxtWetterdatenToCSV(2020, 'Wind')

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


# database.erzeugungsZsmPV(2019,'HH')
# database.erzeugungsZsmPV(2020,'HH')
# database.erzeugungsZsmPV(2019,'SH')
# database.erzeugungsZsmPV(2020,'SH')
#db.erzeugungsZsmPV(2019,'HH', 'PV')
#db.erzeugungsZsmPV(2020,'HH', 'PV')
#db.erzeugungsZsmPV(2019,'SH', 'PV')
#db.erzeugungsZsmPV(2020,'SH', 'PV')

#ablauf2019()

standortliste_123 = []
list_value = []
standort_main = 0
anzahl_2 = []
leistung_Gesamt= []
name_2 = []

def ablaufVorAusbau(year, export):
    #lgk.erzeugungsdatenEEAnlagen(year, 'Wind', 'HH')
    #lgk.erzeugungsdatenEEAnlagen(year, 'Wind', 'SH')
    #lgk.erzeugungsdatenEEAnlagen(year, 'PV', 'SH')
    #lgk.erzeugungsdatenEEAnlagen(year, 'PV', 'HH')

    PV_Gesamt = lgk.erzeugungPerStunde(year, 'PV')
    Wind_Gesamt = lgk.erzeugungPerStunde(year, 'Wind')

    del PV_Gesamt['Datum']
    EE_Erz_Wind_Gesamt = pd.concat([Wind_Gesamt, PV_Gesamt], axis=1, sort=False)

    verbrauch_Wind_Gesamt = lgk.verbrauchGesamt(year)

    EE_Analyse = lgk.analyseEE(year, EE_Erz_Wind_Gesamt, verbrauch_Wind_Gesamt, export = export)

    return EE_Analyse

try:
    openfilename1 = 'Datenbank\ConnectwithID/AlleStandorte_Coords.csv'
    print(openfilename1)

    alleStandorte_Coords = pd.read_csv(openfilename1, delimiter=';', decimal='.', encoding='utf-8')

except:
    print('falsches Format')

try:
    openfilename1 = 'Import\Wetterstationen/StundeWindStationen.csv'
    print(openfilename1)

    weather = pd.read_csv(openfilename1, delimiter=';', encoding='latin1')

except:
    print('falsches Format')

df = gpd.addCoords(weather, 'Stationsname', 'Bundesland', 'Coords')

alleStandorte_Coord = gpd.addWeather(alleStandorte_Coords, df, 'Coords Pot', 'Coords', 'Stations_id')
print(alleStandorte_Coord)
'''alleStandorte_Coords = gpd.addCoords(alleStandorte_Coords, 'StadtPot', 'KreisPot', 'Coords Pot')
alleStandorte_Coords = gpd.addCoords(alleStandorte_Coords, 'StadtVor', 'KreisVor', 'Coords Vor')

finished_filename = 'Datenbank\ConnectwithID/AlleStandorte_Coords.csv'
alleStandorte_Coords.to_csv(finished_filename, sep=';', index=False, encoding='utf-8-sig')
'''
#db.utm_to_gk(2019, 'Wind', 'SH')
#db.utm_to_gk(2019, 'Wind', 'HH')
#db.utm_to_gk(2020, 'Wind', 'SH')
#db.utm_to_gk(2020, 'Wind', 'HH')

verbaut2019 = lgk.stand_distance_analyse(2019, alleStandorte_Coord)
freieha2019 = lgk.freie_ha_vor(2019, alleStandorte_Coord, verbaut2019)
standort_mitfreierLeistung = lgk.freie_leistung_Vor(2019, freieha2019)


for i in range(250):
    # verbaut2020 = lgk.stand_distance_analyse(2020, alleStandorte_Coords)
    if i == 0:
        EE_Analyse = ablaufVorAusbau(2019, export = True)
        finished_filename = 'KORZ.csv'
        standort_mitfreierLeistung.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')
    else:
        EE_Analyse = ablaufVorAusbau(2019, export = False)



    value = lgk.ausbau(2019, EE_Analyse, standort_mitfreierLeistung)

    if value >= 0:
        print(standortliste_123)
        print(value)
        finished_filename = 'FERTIG.csv'

        EE_Analyse.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')
        break
    list_value.append(value)
    print(value)
    #print(Windlastprofil)
    # lgk.Windlastprofil(2020, 'Wind')
    standort = lgk.leistung_im_Jahr(2019, standort_mitfreierLeistung, value, standort_main)
    print('end')
    standortliste_123.append(standort[0])
    anzahl_2.append(standort[1])
    leistung_Gesamt.append(standort[2])
    name_2.append(standort[3])
    standort_main = int(standort[0])


print('Fertig')

print(standortliste_123)
print(list_value)
print('Fertig')










