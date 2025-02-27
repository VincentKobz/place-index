from dataclasses import dataclass
from restaurant import TRIP_API_KEY
import requests

TRIP_API_HEADERS = {
    "accept": "application/json"
}

@dataclass
class TripadvisorApiSettings:
    """
    Class to store the settings for the tripadvisor api
    """
    key: str
    radius_unit: str = "m"
    language: str = "en"
    currency: str = "EUR"

class TripAdvisorApi:
    """
    Class to wrap the tripadvisor api
    """
    NEARBY_SEARCH = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"
    LOCATION = "https://api.content.tripadvisor.com/api/v1/location"

    def __init__(self):
        self.settings = TripadvisorApiSettings(key=TRIP_API_KEY)

    def api_nearby_wrapper(self, lat, long, distance: int):
        """
        Get the restaurants nearby using the tripadvisor nearby search api
        :param lat:
        :param long:
        :param distance:
        :return:
        """
        params = {
            "key": self.settings.key,
            "latLong": f"{lat},{long}",
            "category": "restaurants",
            "radius": distance,
            "radiusUnit": "m",
            "language": self.settings.language,
        }
        return requests.get(self.NEARBY_SEARCH, headers=TRIP_API_HEADERS, params=params)

    def api_details_wrapper(self, location_id: int):
        """
        Get the details of a location using the tripadvisor details api
        :param location_id:
        :return:
        """
        params = {
            "key": self.settings.key,
            "language": self.settings.language,
            "currency": self.settings.currency
        }

        response =  requests.get(f"{self.LOCATION}/{location_id}/details", headers=TRIP_API_HEADERS, params=params)

        return response


    def api_search_by_location_wrapper(self, restaurant_name: str, address: str):
        """
        Search for a restaurant by name and address using the tripadvisor search api
        :param restaurant_name:
        :param address:
        :return:
        """
        params = {
            "key": self.settings.key,
            "language": self.settings.language,
            "currency": self.settings.currency,
            "category": "restaurants",
            "searchQuery": restaurant_name,
            "address": address
        }
        return requests.get(f"{self.LOCATION}/search", headers=TRIP_API_HEADERS, params=params)


    def api_tripadvisor_reviews(self, location_id: int):
        """
        Get reviews from tripadvisor using the location id
        :param location_id:
        :return:
        """
        params = {
            "key": self.settings.key,
            "language": self.settings.language
        }
        return requests.get(f"{self.LOCATION}/{location_id}/reviews", headers=TRIP_API_HEADERS, params=params)
