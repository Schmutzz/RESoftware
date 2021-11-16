from geopy.geocoders import get_geocoder_for_service


# getting OSM data for a specific location
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


# getting the mean coordinates of multiple given locations, also works for single locations
class Multiple:

    # locationSpecifier is giving a specific area to search the location in
    # locationList can be a single location
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

        # checking if the method is working with a list
        if isinstance(self.locationList, list):
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

        # returning data if only one location is given
        elif isinstance(self.locationList, str):

            temp = self.geocode(self.locationList, self.locationSpecifier)
            if temp != False:
                x = float(temp['lon'])
                y = float(temp['lat'])
                return [round(y, 7), round(x, 7)]
            else:
                return [0, 0]

        # returning data if a postal code is given
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
            return self.geocode(self.locationList, self.locationSpecifier)['lat']

