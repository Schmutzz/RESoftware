import zipfile

import requests
import pandas as pd
from zipfile import ZipFile

def testGeoDaten():
    importTrueOrFalse = []
    try:
        filename = 'Import\Wetterstationen/WetterstationenID.csv'
        print(filename)
        df = pd.read_csv(filename, delimiter=';', encoding="latin1")
        print(df)
    except ValueError:
        print("falsches Format")

    urlanfang = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/extreme_wind/recent/'
    lenght = df['ID'].__len__()
    for i in range(lenght):
        zipFileName = "0"
        print(df['ID'][i])
        if df['ID'][i] <= 999:
            zusatznullen = "00"

            url = urlanfang + 'stundenwerte_FX_' + zusatznullen + str(df['ID'][i]) + '_akt.zip'
            r = requests.get(url, allow_redirects=True)
            zipFileName = 'Datenbank\Wetter\WindZipDateien/stundenwerte_FX_' + zusatznullen + str(df['ID'][i]) + '_akt.zip'
            open(zipFileName, 'wb').write(r.content)


        if df['ID'][i] <= 9999 and df['ID'][i] > 999:
            zusatznullen = "0"
            url = urlanfang + 'stundenwerte_FX_' + zusatznullen + str(df['ID'][i]) + '_akt.zip'
            r = requests.get(url, allow_redirects=True)
            zipFileName = 'Datenbank\Wetter\WindZipDateien/stundenwerte_FX_' + zusatznullen + str(df['ID'][i]) + '_akt.zip'
            open(zipFileName, 'wb').write(r.content)


        if df['ID'][i] > 9999:
            url = urlanfang + 'stundenwerte_FX_' + str(df['ID'][i]) + '_akt.zip'
            r = requests.get(url, allow_redirects=True)
            zipFileName = 'Datenbank\Wetter\WindZipDateien/stundenwerte_FX_' + str(df['ID'][i]) + '_akt.zip'
            open(zipFileName, 'wb').write(r.content)

        try:
            with ZipFile(zipFileName, 'r') as zip:
                zip.extractall('Datenbank\Wetter\WindText')
                print('File is unzipped in temp Datenbank\Wetter\WindText')
                importTrueOrFalse.append(True)
        except ValueError:
            print("Probleme mit der Zip-Datei")
        except BaseException:
            print(str(df['ID'][i]) + "is not a Zipfile")
            importTrueOrFalse.append(False)

    if importTrueOrFalse.__len__() == lenght:
        df['TrueOrFalse'] = importTrueOrFalse
        print(df)
        exportname = "Datenbank/" + "FazitWindDaten" + ".csv"
        df.to_csv(exportname, sep=';', encoding='latin1', index=False)
