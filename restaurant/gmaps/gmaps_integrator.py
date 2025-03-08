from restaurant.generic_places import Restaurant, Contact, Features, Reviews
from restaurant.metadatas import PriceLevel, Atmosphere

gmaps_price_level_mapper = {
    "": PriceLevel.UNKNOWN,
    "PRICE_LEVEL_UNSPECIFIED": PriceLevel.UNKNOWN,
    "PRICE_LEVEL_FREE": PriceLevel.FREE,
    "PRICE_LEVEL_INEXPENSIVE": PriceLevel.LOW,
    "PRICE_LEVEL_MODERATE": PriceLevel.MEDIUM,
    "PRICE_LEVEL_EXPENSIVE": PriceLevel.HIGH,
    "PRICE_LEVEL_VERY_EXPENSIVE": PriceLevel.VERY_HIGH
}

ATMOSPHERE_MAPPER = {
    "goodForChildren": Atmosphere.FAMILY,
    "goodForGroups": Atmosphere.GROUPS,
    "goodForWatchingSports": Atmosphere.SPORT
}

class GmapsFeaturesChecker:
    """
    Class to check the features of a google maps place
    """
    TYPES_OF_ACCESSIBILITY = ["wheelchairAccessibleParking", "wheelchairAccessibleEntrance", "wheelchairAccessibleRestroom", "wheelchairAccessibleSeating"]
    CARD_PAYMENT_OPTIONS = ["acceptsCreditCards", "acceptsDebitCards", "acceptsNfc"]
    ALCOHOL_SERVING_OPTIONS = ["servesBeer", "servesWine", "servesCocktails"]
    DOG_FRIENDLY_OPTIONS = ["allowsDogs"]
    SEATING_OPTIONS = ["outdoorSeating", "dineIn"]

    def __init__(self, gmaps_place: dict):
        self.gmaps_place = gmaps_place
        self.seating = any(gmaps_place.get(seating_option, False) for seating_option in self.SEATING_OPTIONS)
        self.dog_friendly = any(gmaps_place.get(dog_friendly_option, False) for dog_friendly_option in self.DOG_FRIENDLY_OPTIONS)

    def is_accessible(self) -> bool:
        """
        Check if the place is accessible
        :return:
        """
        if "accessibilityOptions" not in self.gmaps_place:
            return False

        accessibility_options = self.gmaps_place["accessibilityOptions"]
        return any([accessibility in accessibility_options and accessibility_options[accessibility] for accessibility in self.TYPES_OF_ACCESSIBILITY])


    def is_credit_card_accepted(self) -> bool:
        """
        Check if the place accepts credit or debit card
        :return:
        """
        if "paymentOptions" not in self.gmaps_place:
            return False

        payment_options = self.gmaps_place["paymentOptions"]
        return any([card_option in payment_options and payment_options[card_option] for card_option in self.CARD_PAYMENT_OPTIONS])

    def is_alcohol_served(self) -> bool:
        """
        Check if the place serves alcohol
        :return:
        """
        return any(alcohol_option in self.gmaps_place and self.gmaps_place[alcohol_option] for alcohol_option in self.ALCOHOL_SERVING_OPTIONS)

def gmaps_place_convertor(gmaps_place: dict) -> Restaurant:
    """
    Convert a google maps place (https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places)
    to a Restaurant object.
    :param gmaps_place:
    :return:
    """
    features_checker = GmapsFeaturesChecker(gmaps_place)

    place_contact = Contact(
        phone=gmaps_place.get("internationalPhoneNumber", gmaps_place.get("nationalPhoneNumber", "")),
        email="",
        website=gmaps_place.get("website", ""),
        address=gmaps_place.get("formattedAddress", ""),
        gmaps_uri=gmaps_place.get("googleMapsUri", ""),
        tripadvisor_uri="",
        specific_uri=gmaps_place.get("googleMapsUri", "")
    )

    place_features = Features(
        reservation=gmaps_place.get("reservable", False),
        is_accessible=features_checker.is_accessible(),
        credit_card=features_checker.is_credit_card_accepted(),
        serve_alcohol=features_checker.is_alcohol_served(),
        takeout=gmaps_place.get("takeout", False),
        seating=features_checker.seating,
        wifi=False,
        parking=False,
        dog_allowed=features_checker.dog_friendly
    )

    place_reviews = [
        Reviews(
            rating=review.get("rating", -1),
            lang=review["text"].get("languageCode", ""),
            title="",
            content=review["text"].get("text", ""),
            publication_date=review.get("publishTime", "")
        ) for review in gmaps_place.get("reviews", []) if "text" in review
    ]

    restaurant_atmosphere = [value for key, value in ATMOSPHERE_MAPPER.items() if gmaps_place.get(key, False)]

    return Restaurant(
        id=gmaps_place["id"],
        name=gmaps_place["displayName"].get("text", ""),
        rating=gmaps_place.get("rating", -1),
        types=gmaps_place.get("types", []) + [gmaps_place.get("primaryType", "")],
        price_level=[gmaps_price_level_mapper[gmaps_place.get("priceLevel", "")]],
        contact=place_contact,
        features=place_features,
        reviews=place_reviews,
        atmosphere_target=restaurant_atmosphere
    )
