import zipfile

import requests
import pandas as pd
from zipfile import ZipFile


def cdcdataobservations_germanyHourly(source, idFile):
    """Wetterdaten werden aus CDC Portal eingelesen"""
    importTrueOrFalse = []

    """Auswahl der Datenart"""
    if source == 'wind':
        indizie = "FF"
        indizie2 = 'akt'
        urlanfang = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/' + source + '/recent/'
    if source == 'solar':
        indizie = "ST"
        indizie2 = 'row'
        urlanfang = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/' + source + '/'


    try:
        filename = 'Import\Wetterstationen/' + idFile + '.csv'
        print(filename)
        df = pd.read_csv(filename, delimiter=';', encoding="latin1")
        print(df)
    except ValueError:
        print("falsches Format")



    lenght = df['Stations_id'].__len__()
    for i in range(lenght):
        zipFileName = "0"
        print(df['Stations_id'][i])
        if df['Stations_id'][i] <= 999:
            zusatznullen = "00"

            url = urlanfang + 'stundenwerte_'+ indizie +'_' + zusatznullen + str(df['Stations_id'][i]) + '_' + indizie2 + '.zip'
            r = requests.get(url, allow_redirects=True)
            zipFileName = 'Datenbank\Wetter/' + source + 'ZipDateien/stundenwerte_'+ indizie +'_' + zusatznullen + str(df['Stations_id'][i]) + '_' + indizie2 + '.zip'
            open(zipFileName, 'wb').write(r.content)


        if df['Stations_id'][i] <= 9999 and df['Stations_id'][i] > 999:
            zusatznullen = "0"
            url = urlanfang + 'stundenwerte_'+ indizie +'_' + zusatznullen + str(df['Stations_id'][i]) + '_' + indizie2 + '.zip'
            r = requests.get(url, allow_redirects=True)
            zipFileName = 'Datenbank\Wetter/' + source + 'ZipDateien/stundenwerte_'+ indizie +'_' + zusatznullen + str(df['Stations_id'][i]) + '_' + indizie2 + '.zip'
            open(zipFileName, 'wb').write(r.content)


        if df['Stations_id'][i] > 9999:
            url = urlanfang + 'stundenwerte_'+ indizie +'_' + str(df['Stations_id'][i]) + '_' + indizie2 + '.zip'
            r = requests.get(url, allow_redirects=True)
            zipFileName = 'Datenbank\Wetter/' + source + 'ZipDateien/stundenwerte_'+ indizie +'_' + str(df['Stations_id'][i]) + '_' + indizie2 + '.zip'
            open(zipFileName, 'wb').write(r.content)

        try:
            with ZipFile(zipFileName, 'r') as zip:
                zip.extractall('Datenbank\Wetter/' + source + 'Text')
                print('File is unzipped in temp Datenbank\Wetter\WindText')
                importTrueOrFalse.append(True)
        except ValueError:
            print("Probleme mit der Zip-Datei")
        except BaseException:
            print(str(df['Stations_id'][i]) + "is not a Zipfile")
            importTrueOrFalse.append(False)

    if importTrueOrFalse.__len__() == lenght:
        df['TrueOrFalse'] = importTrueOrFalse
        print(df)
        exportname = "Datenbank/" + "Fazit" + source + "Daten" + ".csv"
        df.to_csv(exportname, sep=';', encoding='latin1', index=False)
