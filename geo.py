from geopy.geocoders import get_geocoder_for_service
import pandas as pd
import geodata as gd
from geopy import distance

"""

class SingleLocation:

    # locationSpecifier is giving a specific area to search the location in
    def __init__(self, location, locationSpecifier):
        self.location = location
        self.locationSpecifier = locationSpecifier

    def geocode(self, location, locationSpecifier):
        cls = get_geocoder_for_service("nominatim")
        geolocator = cls(**dict(user_agent="my_app"))
        data = geolocator.geocode(location + ', ' + locationSpecifier)
        return data.raw

    def getXcor(self):
        return self.geocode(self.location, self.locationSpecifier)['lon']

    def getYcor(self):
        return self.geocode(self.location, self.locationSpecifier)['lat']

    def getName(self):
        return self.geocode(self.location, self.locationSpecifier)['display_name']

    def getRaw(self):
        return self.geocode(self.location, self.locationSpecifier)


# getting the mean coordinates of multiple given locations
class Multiple:

    # locationSpecifier is giving a specific area to search the location in
    def __init__(self, locationList, locationSpecifier):  # locationList MUST be a list of multiple strings!!!
        self.locationList = locationList
        self.locationSpecifier = locationSpecifier

    def geocode(self, location, locationSpecifier):
        cls = get_geocoder_for_service("nominatim")
        geolocator = cls(**dict(user_agent="my_app"))
        data = geolocator.geocode(location + ', ' + locationSpecifier)
        return data.raw

    def getMeanCoords(self):
        x = 0.0
        y = 0.0
        counter = 0

        # checking if the method is working with a list
        if isinstance(self.locationList, list):
            for i in self.locationList:
                x += float(self.geocode(i, self.locationSpecifier)['lon'])
                y += float(self.geocode(i, self.locationSpecifier)['lat'])
                counter += 1

            # calculating the mean values
            x = x / counter
            y = y / counter

            return [x, y]

        # returning data if only one location is given
        elif isinstance(self.locationList, str):
            x = float(self.geocode(self.locationList, self.locationSpecifier)['lon'])
            y = float(self.geocode(self.locationList, self.locationSpecifier)['lat'])
            return [x, y]

    def getMeanX(self):
        x = 0.0
        counter = 0

        # checking if the method is working with a list
        if isinstance(self.locationList, list):
            for i in self.locationList:
                x += float(self.geocode(i, self.locationSpecifier)['lon'])
                counter += 1

            # returning the mean
            return x / counter

        # returning data if only one location is given
        elif isinstance(self.locationList, str):
            return self.geocode(self.locationList, self.locationSpecifier)['lon']

    def getMeanY(self):
        y = 0.0
        counter = 0

        # checking if the method is working with a list
        if isinstance(self.locationList, list):
            for i in self.locationList:
                y += float(self.geocode(i, self.locationSpecifier)['lat'])
                counter += 1

            # returning the mean
            return y / counter

        # returning data if only one location is given
        elif isinstance(self.locationList, str):
            return self.geocode(self.locationList, self.locationSpecifier)


enc_var = 'latin1'  # for encoding special symbols


# cut a string into a list of strings via certain seperation sign
def listFromStr(text, seperator):
    list_of_str = text.split(seperator)
    return list_of_str


areas_SH = pd.read_csv('opendata_wka_ib_gv_vb_sh_20210713.csv', sep=';', encoding=enc_var, decimal=',')
# areas_HH = pd.read_csv('WindparksHH_Koordinaten.csv', sep=';',encoding='latin1', decimal=',')

stations = pd.read_excel('Liste Wetterstationen HH_SH.xlsx')


def addCoords(df, cityHeader, specifierHeader, finished_filename):
    cities = df[cityHeader].tolist()
    specifiers = df[specifierHeader].tolist()
    copyCities = []
    copySpec = []

    for i in cities:
        i = i.replace('Ã¼', 'ü')
        i = i.replace('Ã¶', 'ö')
        i = i.replace('Ã', 'ß')
        i = i.replace('Ã¤', 'ä')
        copyCities.append(i)
    cities = copyCities

    for i in specifiers:
        i = i.replace('Ã¼', 'ü')
        i = i.replace('Ã¶', 'ö')
        i = i.replace('Ã', 'ß')
        i = i.replace('Ã¤', 'ä')
        copySpec.append(i)
    specifiers = copySpec

    def getCoords(list_of_cities, specifier):
        object = gd.Multiple(list_of_cities, specifier)

        return object.getMeanCoords()

    coords = []

    def goThrough(cities, specifiers):
        # lst = []

        # for idx, city in enumerate(cities):
        #   lst.append(listFromStr(city))

        for index, city in enumerate(cities):
            dif_coords = getCoords(city, specifiers[index])
            coords.append(dif_coords)

    goThrough(cities, specifiers)

    df['Coords'] = coords

    df.to_csv(finished_filename, sep=';', index=False)


addCoords(areas_SH, 'GEMEINDE', 'KREIS', 'WindparksSH_Koordinaten.csv')


def addWeather(areas, stations, areaCoordsHead, stationCoordsHead, finished_filename):
    ids = stations['ID'].tolist()
    weatherCoords = stations[stationCoordsHead].tolist()
    areaCoords = areas[areaCoordsHead].tolist()
    id_list = []

    for areaIndex, area in enumerate(areaCoords):
        min_id = 0
        min_dist = 1000000
        area = area.replace('[', '')
        area = area.replace(']', '')
        area = tuple(listFromStr(area, ', '))
        for weatherIndex, weather in enumerate(weatherCoords):
            weather = weather.replace('[', '')
            weather = weather.replace(']', '')
            weather = tuple(listFromStr(weather, ', '))
            temp_dist = distance.distance(area, weather).km
            if temp_dist < min_dist:
                min_dist = temp_dist
                min_id = ids[weatherIndex]

        id_list.append(min_id)

    areas['Wetter-ID'] = id_list

    areas.to_csv(finished_filename, sep=';', index=False)


areas_SH_Coords = pd.read_csv('WindparksSH_Koordinaten.csv', sep=';', encoding=enc_var, decimal=',')

addWeather(areas_SH_Coords, stations, 'Coords', 'Koordinaten', 'WindparksSH_WetterID.csv')

"""
