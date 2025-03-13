import json

import requests

from place_index import GMAPS_API_KEY
from place_index.metadatas import GMAPS_URL

from place_index.generic_places import Restaurant
from place_index.gmaps.gmaps_integrator import gmaps_place_convertor


class PlacesGoogleFields:
    def __init__(self):
        self.mask = []
        self.add_base_fields()

    def add_field(self, field):
        self.mask.append(field)

    def add_base_fields(self):
        self.mask += [
            "places.displayName",
            "places.id",
            "places.types",
            "places.primaryType",
            "places.rating",
            "places.priceLevel",
            "places.formattedAddress",
            "places.types",
            "places.priceRange",
            "places.paymentOptions",
            "places.accessibilityOptions",
            "places.servesBeer",
            "places.servesWine",
            "places.servesCocktails",
            "places.takeout",
            "places.businessStatus",
            "places.googleMapsUri",
            "places.websiteUri",
            "places.reviews",
            "places.reservable",
            "places.dineIn",
            "places.internationalPhoneNumber",
            "places.nationalPhoneNumber",
            "places.goodForChildren",
            "places.goodForGroups",
            "places.goodForWatchingSports",
            "places.allowsDogs",
        ]


class GooglePlacesApi:
    """
    Class to wrap the google places API
    """

    def __init__(self):
        self.fields = PlacesGoogleFields()

    def google_api_wrapper(self, lat, long, distance):
        """
        Get the restaurants nearby using the nearby search places API
        :param lat:
        :param long:
        :param distance:
        :return:
        """
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": GMAPS_API_KEY,
            "X-Goog-FieldMask": ",".join(self.fields.mask),
        }

        data = {
            "includedTypes": ["place_index"],
            "maxResultCount": 20,
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": lat, "longitude": long},
                    "radius": distance,
                }
            },
        }

        return requests.post(GMAPS_URL, headers=headers, data=json.dumps(data))


def gmaps_place_nearby_handler(response):
    local_restaurants = []
    not_exploitable = 0
    if not response.ok:
        return []
    try:
        places = response.json()["places"]
        for place in places:
            current_restaurant: Restaurant = gmaps_place_convertor(place)
            if current_restaurant.is_exploitable():
                local_restaurants.append(current_restaurant)
            else:
                not_exploitable += 1
    except KeyError as e:
        print(e)

    print(f"Number of not exploitable restaurants: {not_exploitable}")

    return local_restaurants


def google_matrix_distance(src, dst):
    """
    Get the distance by walk between two points using the google maps distance matrix api
    :param src:
    :param dst:
    :return:
    """
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GMAPS_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.id,places.types,places.rating,places.priceLevel,places.formattedAddress,places.types",
    }

    URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

    response = requests.post(
        URL,
        headers=headers,
        params={
            "origins": src,
            "destinations": dst,
            "mode": "walking",
            "units": "metric",
            "key": GMAPS_API_KEY,
        },
    )

    return response.json()
