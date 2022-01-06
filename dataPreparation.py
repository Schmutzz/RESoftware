import database as db
import internetDownload as itd
import geo as gpd
import pandas as pd
import logik as lgk


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

def wetterdaten_from_CDC(year):

    itd.cdcdataobservations_germanyHourly('wind', 'StundeWindStationen')
    itd.cdcdataobservations_germanyHourly('solar', 'StundeSolarStationen')

    liste = db.findoutFiles('Datenbank\Wetter\WindZipDateien')

    for i in range(len(liste)):
        zipfilename = 'Datenbank\Wetter\WindZipDateien/' + liste[i]
        db.zipentpacken(zipfilename, 'Wind')

    db.TxtWetterdatenToCSV(year, 'PV')
    db.TxtWetterdatenToCSV(year, 'Wind')

def PV_zusammenfassung(year):

    db.erzeugungsZsmPV(year, 'HH', 'PV')
    db.erzeugungsZsmPV(year, 'SH', 'PV')

def weatherStation_getCoords():

    try:
        openfilename1 = 'Import\Wetterstationen/StundeWindStationen.csv'
        print(openfilename1)

        weather = pd.read_csv(openfilename1, delimiter=';', encoding='latin1')

    except:
        print('falsches Format')

    df = gpd.addCoords(weather, 'Stationsname', 'Bundesland', 'Coords')

    finished_filename = 'Datenbank\Wetter/StundeWindStationen_Coords.csv'
    df.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')

    '---------------------------------------------------------------------------------'

    try:
        openfilename1 = 'Import\Wetterstationen/StundeSolarStationen.csv'
        print(openfilename1)

        weather = pd.read_csv(openfilename1, delimiter=';', encoding='latin1')

    except:
        print('falsches Format')

    df = gpd.addCoords(weather, 'Stationsname', 'Bundesland', 'Coords')

    finished_filename = 'Datenbank\Wetter/StundeSolarStationen_Coords.csv'
    df.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')

def plannedAreas_toUTM_and_connectWeahterID(source, state, weather):

    filelist = db.findoutFiles('Datenbank\ConnectwithID\Erzeugung')

    matches = [match for match in filelist if source in match]
    matches = [match for match in matches if state in match]
    matches = [match for match in matches if str('geplanterAusbau') in match]
    name = 'WindparksSH_geplanterAusbau_UTM'
    # headerlistLokation = ['OSTWERT (EPSG:4647)', 'NORDWERT (EPSG:4647']
    try:
        openfilename1 = 'Datenbank\ConnectwithID\Erzeugung/' + matches[0]
        print(openfilename1)

        df = pd.read_csv(openfilename1, delimiter=';', decimal=',', encoding='latin1')

    except:
        print('falsches Format')


    df = db.utm_to_gk(name, df, export=False)
    df = gpd.addWeather(df, weather, 'Coords UTM', 'Coords', 'Stations_id')

    finished_filename = 'Datenbank\ConnectwithID\Erzeugung/WindparksSH_geplanterAusbau_UTM_WeatherID.csv'
    df.to_csv(finished_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')

def erzeugung_Wind_PV(year):
    print('year')
    lgk.erzeugungsdatenEEAnlagen(year, 'Wind', 'HH')
    lgk.erzeugungsdatenEEAnlagen(year, 'PV', 'HH')
    lgk.erzeugungsdatenEEAnlagen(year, 'Wind', 'SH')
    lgk.erzeugungsdatenEEAnlagen(year, 'PV', 'SH')

def plannedAreas_getCoords_and_getWeather(alleStandorte_Coords, windWeatherStation):

    print('start')
    #alleStandorte_Coords = gpd.addCoords(alleStandorte_Coords, 'StadtPot', 'KreisPot', 'Coords Pot')
    #alleStandorte_Coords = gpd.addCoords(alleStandorte_Coords, 'StadtVor', 'KreisVor', 'Coords Vor')

    alleStandorte_Coords = gpd.addWeather(alleStandorte_Coords, windWeatherStation, 'Coords Pot', 'Coords',
                                          'Stations_id', '_Pot')
    alleStandorte_Coords = gpd.addWeather(alleStandorte_Coords, windWeatherStation, 'Coords Vor', 'Coords',
                                          'Stations_id', '_Vor')


    finished_filename = 'Datenbank\ConnectwithID/AlleStandorte_Coords_final.csv'
    alleStandorte_Coords.to_csv(finished_filename, sep=';', index=False, encoding='utf-8-sig')

def erzeugung_plannendAreas(year, geplanterAusbau):
    try:
        openfilename2 = 'Datenbank\Wetter/Wind_Wetterdaten_' + str(year) + '.csv'
        print(openfilename2)
        wetterdaten = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)

    except ValueError:
        print("falsches Format")

    #df = lgk.erzeugungEEAnlage_singleFrame(wetterdaten, geplanterAusbau, year, export=False)
    try:
        openfilename2 = 'Datenbank\Erzeugung\Erz_geplanterAusbau/Erz_geplanterAusbau_2019.csv'
        print(openfilename2)
        df = pd.read_csv(openfilename2, delimiter=';', decimal=',', header=0)

    except ValueError:
        print("falsches Format")

    lgk.erzeugungPerStunde_singleFrame(year, df, export=True)


