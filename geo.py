from geopy.geocoders import get_geocoder_for_service
from geopy import distance


# getting OSM data for a single, specific location
class SingleLocation:

    # locationSpecifier is giving a specific area to search the location in
    def __init__(self, location, locationSpecifier):
        self.location = location
        self.locationSpecifier = locationSpecifier

    def geocode(self, location, locationSpecifier):
        cls = get_geocoder_for_service("nominatim")
        geolocator = cls(**dict(user_agent="my_app"))
        try:
            data = geolocator.geocode(location + ', ' + locationSpecifier)
            if data == None:
                raise Exception
        except Exception:
            print('this location is wrong: ' + location)
            return False
        else:
            return data.raw

    def getXcor(self):
        temp = self.geocode(str(self.location), str(self.locationSpecifier))
        if temp != False:
            return temp['lon']
        else:
            return 0.0

    def getYcor(self):
        temp = self.geocode(str(self.location), str(self.locationSpecifier))
        if temp != False:
            return temp['lat']
        else:
            return 0.0

    def getName(self):
        temp = self.geocode(str(self.location), str(self.locationSpecifier))
        if temp != False:
            return temp[['display_name']]
        else:
            return 'not_found'

    def getRaw(self):
        temp = self.geocode(str(self.location), str(self.locationSpecifier))
        if temp != False:
            return temp
        else:
            return 'not_found'

    def getCoords(self):
        temp = self.geocode(str(self.location), str(self.locationSpecifier))
        if temp != False:
            return [temp['lat'], temp['lon']]
        else:
            return 0.0


# getting the mean coordinates of multiple given locations, also works for single locations
class Multiple:

    # locationSpecifier is giving a specific area to search the location in
    # locationList can also be a single location (postal code or string)
    def __init__(self, locationList, locationSpecifier):
        self.locationList = locationList
        self.locationSpecifier = locationSpecifier

    # tries to find location, prints out specific location if it cant be found, doesnt stop the process
    def geocode(self, location, locationSpecifier):
        cls = get_geocoder_for_service("nominatim")
        geolocator = cls(**dict(user_agent="my_app"))
        try:
            data = geolocator.geocode(location + ', ' + locationSpecifier)
            if data == None:
                raise Exception
        except Exception:
            print('this location is wrong: ' + location)
            return False
        else:
            return data.raw

    # returns the mean coords of locationList, returns [0, 0] if no location was found
    def getMeanCoords(self):
        x = 0.0
        y = 0.0
        counter = 0

        # for lists
        if isinstance(self.locationList, list):

            # for list of strings
            if all(isinstance(n, str) for n in self.locationList):
                for i in self.locationList:
                    temp = self.geocode(i, self.locationSpecifier)
                    if temp != False:
                        x += float(temp['lon'])
                        y += float(temp['lat'])
                        counter += 1

                if counter != 0:
                    # calculating the mean values
                    x = x / counter
                    y = y / counter

                    return [round(y, 7), round(x, 7)]

                else:
                    return [0, 0]

            # for list of integers (postal codes)
            elif all(isinstance(n, int) for n in self.locationList):
                for i in self.locationList:
                    temp = self.geocode(str(i), self.locationSpecifier)
                    if temp != False:
                        x += float(temp['lon'])
                        y += float(temp['lat'])
                        counter += 1

                if counter != 0:
                    # calculating the mean values
                    x = x / counter
                    y = y / counter

                    return [round(y, 7), round(x, 7)]

                else:
                    return [0, 0]

        # returning data if only one location is given
        elif isinstance(self.locationList, str):

            temp = self.geocode(self.locationList, self.locationSpecifier)
            if temp != False:
                x = float(temp['lon'])
                y = float(temp['lat'])
                return [round(y, 7), round(x, 7)]
            else:
                return [0, 0]

        # returning data if one postal code is given
        elif isinstance(self.locationList, int):

            temp = self.geocode(str(self.locationList), self.locationSpecifier)
            if temp != False:
                x = float(temp['lon'])
                y = float(temp['lat'])
                return [round(y, 7), round(x, 7)]
            else:
                return [0, 0]

    def getMeanX(self):
        x = 0.0
        counter = 0

        # checking if the method is working with a list
        if isinstance(self.locationList, list):

            # for list of strings
            if all(isinstance(n, str) for n in self.locationList):
                for i in self.locationList:
                    temp = self.geocode(i, self.locationSpecifier)
                    if temp != False:
                        x += float(temp['lon'])
                        counter += 1

                if counter != 0:
                    # calculating the mean values
                    x = x / counter

                    return round(x, 7)

                else:
                    return 0.0

            # for list of integers (postal codes)
            elif all(isinstance(n, int) for n in self.locationList):
                for i in self.locationList:
                    temp = self.geocode(str(i), self.locationSpecifier)
                    if temp != False:
                        x += float(temp['lon'])
                        counter += 1

                if counter != 0:
                    # calculating the mean values
                    x = x / counter

                    return round(x, 7)

                else:
                    return 0.0

            # returning data if only one location is given
            elif isinstance(self.locationList, str):

                temp = self.geocode(self.locationList, self.locationSpecifier)
                if temp != False:
                    x = float(temp['lon'])
                    return round(x, 7)
                else:
                    return 0.0

            # returning data if one postal code is given
            elif isinstance(self.locationList, int):

                temp = self.geocode(str(self.locationList), self.locationSpecifier)
                if temp != False:
                    x = float(temp['lon'])
                    return round(x, 7)
                else:
                    return 0.0

    def getMeanY(self):
        y = 0.0
        counter = 0

        # checking if the method is working with a list
        if isinstance(self.locationList, list):

            # for list of strings
            if all(isinstance(n, str) for n in self.locationList):
                for i in self.locationList:
                    temp = self.geocode(i, self.locationSpecifier)
                    if temp != False:
                        y += float(temp['lon'])
                        counter += 1

                if counter != 0:
                    # calculating the mean values
                    y = y / counter

                    return round(y, 7)

                else:
                    return 0.0

            # for list of integers (postal codes)
            elif all(isinstance(n, int) for n in self.locationList):
                for i in self.locationList:
                    temp = self.geocode(str(i), self.locationSpecifier)
                    if temp != False:
                        y += float(temp['lon'])
                        counter += 1

                if counter != 0:
                    # calculating the mean values
                    y = y / counter

                    return round(y, 7)

                else:
                    return 0.0

            # returning data if only one location is given
            elif isinstance(self.locationList, str):

                temp = self.geocode(self.locationList, self.locationSpecifier)
                if temp != False:
                    y = float(temp['lon'])
                    return round(y, 7)
                else:
                    return 0.0

            # returning data if one postal code is given
            elif isinstance(self.locationList, int):

                temp = self.geocode(str(self.locationList), self.locationSpecifier)
                if temp != False:
                    y = float(temp['lon'])
                    return round(y, 7)
                else:
                    return 0.0


# adds a coords column to a dataframe ('Coords')
def addCoords(df, locationHeader, specifierHeader, finished_filename):

    locationList = replaceSpecialSigns(df[locationHeader].tolist())
    specifierList = replaceSpecialSigns(df[specifierHeader].tolist())
    coords = []

    for index, location in enumerate(locationList):
        if locationList[index].contains(','):
            locationList[index] = listFromStr(locationList[index], ',')

    for index, location in enumerate(locationList):
        coords.append(getCoords(location, specifierList[index]))

    df['Coords'] = coords
    df.to_csv(finished_filename, sep=';', index=False, encoding='latin1')


# adds weatherstation-ID to a dataframe ('Wetter-ID_Head')
def addWeather(df_locations, df_weatherStations, locationCoordsHead, stationCoordsHead, ID_Head, finished_filename):

    ids = df_weatherStations[ID_Head].tolist()
    weatherCoords = df_weatherStations[stationCoordsHead].tolist()
    locationCoords = df_locations[locationCoordsHead].tolist()
    id_list = []

    for location in locationCoords:
        min_id = 0
        min_dist = 0

        # distance method argument is a tuple
        location = editCoords(location)
        for index, station in enumerate(weatherCoords):
            station = editCoords(station)
            temp_dist = distance.distance(location, station).km
            if (temp_dist < min_dist) or index == 0:
                min_dist = temp_dist
                min_id = ids[index]

        id_list.append(min_id)

    df_locations['Wetter-ID_Head'] = id_list
    df_locations.to_csv(finished_filename, sep=';', index=False, encoding='latin1')


# adds list of weatherstation-IDs and corresponding weighting factors ('Wetter-ID_Head', 'Gewichtung)
def addWeatherRadian(df_locations, df_weatherStations, locationCoordsHead, stationCoordsHead, ID_Head, finished_filename,
                     radian=5):

    # lists method works with
    ids = df_weatherStations[ID_Head].tolist()
    weatherCoords = df_weatherStations[stationCoordsHead].tolist()
    locationCoords = df_locations[locationCoordsHead].tolist()

    # empty lists method will return
    id_list = []
    factor_list = []
    radianReset = radian

    for i, location in enumerate(locationCoords):
        ids_in_radian = []
        distances = []
        weatherReset = []

        # distance method argument is a tuple
        location = editCoords(location)

        while len(ids_in_radian) < 3:
            for index, stationCoords in enumerate(weatherCoords):

                stationCoords_temp = editCoords(stationCoords)

                temp_dist = distance.distance(location, stationCoords_temp).km
                if temp_dist < radian:
                    ids_in_radian.append(ids[index])
                    ids.remove(ids[index])
                    weatherReset.append(stationCoords)
                    weatherCoords.remove(stationCoords)
                    distances.append(temp_dist)

            radian += 3

        # return used ids/coordinates to the complete list
        for j in ids_in_radian:
            ids.append(j)
        for k in weatherReset:
            weatherCoords.append(k)

        radian = radianReset
        factors = calcFactor(distances, radian)
        factor_list.append(factors)
        id_list.append(ids_in_radian)
        print(i)

    df_locations['Wetter-ID_Head'] = id_list
    df_locations['Gewichtung'] = factor_list
    df_locations.to_csv(finished_filename, sep=';', index=False, encoding='latin1')


# combines two coordinates columns into one ('Coords')
def combineCoords(df, longitude_head, latitude_head):

    lon = df[longitude_head].tolist()
    lat = df[latitude_head].tolist()
    coords = []

    for index, x in enumerate(lon):
        coords.append(str([lon[index], lat[index]]))

    df['Coords'] = coords


# returns coords as tuple
def editCoords(coords):

    coords = str(coords)
    coords = coords.replace('[', '')
    coords = coords.replace(']', '')
    coords = tuple(listFromStr(coords, ', '))
    return coords


# calculates "weight-factors"
def calcFactor(distances, radian):

    factors = []
    scoreList = []
    scoreSum = 0.0

    for i, dist in enumerate(distances):
        scoreList.append(1000 * (1 / (pow(2, dist / (radian * 1.5)))))
        scoreSum += scoreList[i]

    for score in scoreList:
        factors.append(float.__round__(score / scoreSum, 6))

    return factors


# cut a string into a list of strings via certain seperation sign
def listFromStr(text, seperator):

    list_of_str = text.split(seperator)
    return list_of_str


# get mean coords for a list of locations
def getCoords(list_of_cities, specifier):

    object = Multiple(list_of_cities, specifier)

    return object.getMeanCoords()


# replaces encoded special signs (ä, ö, ü, ß)
def replaceSpecialSigns(text):

    if isinstance(text, list):
        for index, i in enumerate(text):
            if isinstance(i, str):
                i = i.replace('Ã¼', 'ü')
                i = i.replace('Ã¶', 'ö')
                i = i.replace('Ã', 'ß')
                i = i.replace('Ã¤', 'ä')
                i = i.replace('Kr Hzgt ', 'Herzogtum')
                i = i.replace('Kr ', '')
                i = i.replace('St.', 'Sankt')
                text[index] = i
    elif isinstance(text, str):
        text = text.replace('Ã¼', 'ü')
        text = text.replace('Ã¶', 'ö')
        text = text.replace('Ã', 'ß')
        text = text.replace('Ã¤', 'ä')
        text = text.replace('Kr Hzgt ', 'Herzogtum')
        text = text.replace('Kr ', '')
        text = text.replace('St.', 'Sankt')

    return text