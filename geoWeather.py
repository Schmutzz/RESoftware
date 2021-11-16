import pandas as pd
import geodata as gd
from geopy import distance


# cut a string into a list of strings via certain seperation sign
def listFromStr(text, seperator):
    list_of_str = text.split(seperator)
    return list_of_str


# get mean coords for a list of locations
def getCoords(list_of_cities, specifier):
    object = gd.Multiple(list_of_cities, specifier)

    return object.getMeanCoords()


# replaces encoded special signs (ä, ö, ü, ß)
def replaceSpecialSigns(lst):
    if isinstance(lst, list):
        for index, i in enumerate(lst):
            if isinstance(i, str):
                i = i.replace('Ã¼', 'ü')
                i = i.replace('Ã¶', 'ö')
                i = i.replace('Ã', 'ß')
                i = i.replace('Ã¤', 'ä')
                lst[index] = i
    elif isinstance(lst, str):
        lst = lst.replace('Ã¼', 'ü')
        lst = lst.replace('Ã¶', 'ö')
        lst = lst.replace('Ã', 'ß')
        lst = lst.replace('Ã¤', 'ä')

    return lst


# adds a coords column to a dataframe
def addCoords(df, locationHeader, specifierHeader, finished_filename):
    locations = replaceSpecialSigns(df[locationHeader].tolist())
    specifiers = replaceSpecialSigns(df[specifierHeader].tolist())

    def goThrough(locations, specifiers):
        coords = []

        for index, singleLoc in enumerate(locations):
            coords.append(getCoords(singleLoc, specifiers[index]))

        return coords

    coordsList = goThrough(locations, specifiers)

    df['Coords'] = coordsList

    df.to_csv(finished_filename, sep=';', index=False, encoding='latin1')


# adds weatherstation-ID to a dataframe (coordinates have to exist in a single column)
def addWeather(df_locations, df_weatherStations, areaCoordsHead, stationCoordsHead, ID_Head, finished_filename):
    ids = df_weatherStations[ID_Head].tolist()
    weatherCoords = df_weatherStations[stationCoordsHead].tolist()
    areaCoords = df_locations[areaCoordsHead].tolist()
    id_list = []

    for location in enumerate(areaCoords):
        min_id = 0
        min_dist = 0

        # distance method argument is a tuple
        location = location.replace('[', '')
        location = location.replace(']', '')
        location = tuple(listFromStr(location, ', '))
        for index, station in enumerate(weatherCoords):
            station = station.replace('[', '')
            station = station.replace(']', '')
            station = tuple(listFromStr(station, ', '))
            temp_dist = distance.distance(location, station).km
            if (temp_dist < min_dist) or index == 0:
                min_dist = temp_dist
                min_id = ids[index]

        id_list.append(min_id)

    df_locations['Wetter-ID_Head'] = id_list

    df_locations.to_csv(finished_filename, sep=';', index=False, encoding='latin1')


# returns a list of coordinate duos -> [longitude, latitude]
def combineCoords(df, lon_head, lat_head):
    lon = df[lon_head].tolist()
    lat = df[lat_head].tolist()
    coords = []

    for x, y in enumerate(lon, lat):
        coords.append(str([x, y]))

    return coords
