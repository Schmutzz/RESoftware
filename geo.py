import geopy
from geopy.geocoders import Nominatim
from geopy.geocoders import get_geocoder_for_service

class Geodaten:

    #geolocator = Nominatim(user_agent="my_request")

    def __init__(self, strOrt, strKreis):
        self.strOrt = strOrt
        self.strKreis = strKreis

    def geocode(self):

        cls = get_geocoder_for_service("nominatim")
        geolocator = cls(**dict(user_agent="my_App"))

        location = geolocator.geocode(self.strOrt + ', ' + self.strKreis)
        return location.raw

    def getXcor(self):
        return self.geocode()['lon']

    def getYcor(self):
        return self.geocode()['lat']

    def getName(self):
        return self.geocode()['display_name']
