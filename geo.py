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
