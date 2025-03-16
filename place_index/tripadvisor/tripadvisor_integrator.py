from typing import List

from place_index.generic_places import Restaurant, Contact, Features, Reviews
from place_index.metadatas import PriceLevel
from place_index.tripadvisor.tripadvisor_api_handler import (
    TripadvisorFullContent,
    TripadvisorLocationDetailsHandler,
)

trip_advisor_price_level_mapper = {
    "": PriceLevel.UNKNOWN,
    "$": PriceLevel.LOW,
    "$$": PriceLevel.MEDIUM,
    "$$$": PriceLevel.HIGH,
    "$$$$": PriceLevel.VERY_HIGH,
}


def parse_tripadvisor_price_level(price_level: str) -> List[PriceLevel]:
    """
    Parse the price level from tripadvisor
    :param price_level:
    :return:
    """
    return list(
        map(trip_advisor_price_level_mapper.get, map(str.strip, price_level.split("-")))
    )


class TripadvisorFeatures:
    """
    Class to check the features of a tripadvisor place
    """

    TYPES_OF_ACCESSIBILITY = ["Wheelchair Accessible"]
    CARD_PAYMENT_OPTIONS = [
        "American Express",
        "Accepts Credit Cards",
        "Mastercard",
        "Visa",
        "Digital Payments",
    ]
    ALCOHOL_SERVING_OPTIONS = ["Serves Alcohol", "Wine and Beer", "Full Bar"]
    WIFI_OPTIONS = ["Free Wifi"]
    RESERVABLE_OPTIONS = ["Reservations"]
    SEATING_OPTIONS = ["Seating", "Outdoor Seating", "Sit down"]
    DOG_FRIENDLY_OPTIONS = ["Dog Friendly"]
    PARKING_OPTIONS = ["Parking Available"]
    TAKEOUT_OPTIONS = ["Takeout"]

    def __init__(self, trip_place: TripadvisorLocationDetailsHandler):
        self.trip_place = trip_place
        self.is_accessible = any(
            accessibility_option in trip_place.features
            for accessibility_option in self.TYPES_OF_ACCESSIBILITY
        )
        self.is_credit_card_accepted = any(
            card_option in trip_place.features
            for card_option in self.CARD_PAYMENT_OPTIONS
        )
        self.is_alcohol_served = any(
            alcohol_option in trip_place.features
            for alcohol_option in self.ALCOHOL_SERVING_OPTIONS
        )
        self.wifi = any(
            wifi_option in trip_place.features for wifi_option in self.WIFI_OPTIONS
        )
        self.is_reservable = any(
            reservable_option in trip_place.features
            for reservable_option in self.RESERVABLE_OPTIONS
        )
        self.seating = any(
            seating_option in trip_place.features
            for seating_option in self.SEATING_OPTIONS
        )
        self.dog_friendly = any(
            dog_friendly_option in trip_place.features
            for dog_friendly_option in self.DOG_FRIENDLY_OPTIONS
        )
        self.parking = any(
            parking_option in trip_place.features
            for parking_option in self.PARKING_OPTIONS
        )
        self.takeout = any(
            takeout_option in trip_place.features
            for takeout_option in self.TAKEOUT_OPTIONS
        )


def tripadvisor_place_convertor(
    tripadvisor_place: TripadvisorFullContent,
) -> Restaurant:
    """
    Convert a tripadvisor place to a Restaurant object.
    :return:
    """
    trip_details = tripadvisor_place.details
    trip_reviews = tripadvisor_place.reviews
    trip_features = TripadvisorFeatures(trip_details)

    place_contact = Contact(
        phone=trip_details.phone,
        email=trip_details.email,
        website=trip_details.website,
        address=trip_details.address,
        gmaps_uri=None,
        tripadvisor_uri=trip_details.tripadvisor_uri,
        specific_uri=trip_details.tripadvisor_uri,
    )

    place_features = Features(
        reservation=trip_features.is_reservable,
        is_accessible=trip_features.is_accessible,
        credit_card=trip_features.is_credit_card_accepted,
        serve_alcohol=trip_features.is_alcohol_served,
        takeout=trip_features.takeout,
        seating=trip_features.seating,
        wifi=trip_features.wifi,
        parking=trip_features.parking,
        dog_allowed=trip_features.dog_friendly,
    )

    place_reviews = [
        Reviews(
            rating=review.rating,
            lang=review.lang,
            title=review.title,
            content=review.content,
            publication_date=review.publication_date,
        )
        for review in trip_reviews.reviews
    ]

    return Restaurant(
        id=str(trip_details.location_id),
        name=trip_details.name,
        rating=float(trip_details.rating),
        types=trip_details.types,
        price_level=parse_tripadvisor_price_level(trip_details.price_level),
        contact=place_contact,
        features=place_features,
        reviews=place_reviews,
        atmosphere_target=trip_details.trip_types,
        number_of_reviews=trip_details.number_of_reviews,
    )
