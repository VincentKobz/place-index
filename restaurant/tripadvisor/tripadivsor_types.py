from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class BaseTripadvisorContent:
    location_id: int

@dataclass
class TripadvisorNearbyHandler(BaseTripadvisorContent):
    name: str

    @classmethod
    def from_place(cls, place):
        return cls(place["location_id"], place["name"])

@dataclass
class TripadvisorLocationDetailsHandler(BaseTripadvisorContent):
    name: str
    website: str
    tripadvisor_uri: str
    email: str
    phone: str
    address: str
    rating: float
    price_level: str
    features: List[str]
    types: List[str]
    trip_types: List[str]

    @classmethod
    def from_place(cls, place_details):
        return cls(
            place_details["location_id"],
            place_details["name"],
            place_details.get("website", ""),
            place_details.get("web_url", ""),
            place_details.get("email", ""),
            place_details.get("phone", ""),
            place_details.get("address_obj", "").get("address_string", ""),
            place_details.get("rating", -1),
            place_details.get("price_level", ""),
            cls.merge_features(place_details.get("features", []), place_details.get("subcategory", [])),
            [cuisine["localized_name"] for cuisine in place_details.get("cuisine", []) if "localized_name" in cuisine],
            [trip_type["localized_name"] for trip_type in place_details.get("trip_types", []) if "localized_name" in trip_type]
        )

    @staticmethod
    def merge_features(features, subcategories):
        """
        Merge the features with the subcategory
        :param features:
        :param subcategories:
        :return:
        """
        return features + [subcategory["localized_name"] for subcategory in subcategories if "localized_name" in subcategory]


class TripType(Enum):
    """
    Enum to represent the trip type
    """
    SOLO = "Solo travel"
    COUPLES = "Couples"
    FAMILY = "Family"
    FRIENDS = "Friends getaway"
    Business = "Business"
    UNKNOWN = "Unknown"

@dataclass
class TripadvisorReview:
    lang: str
    publication_date: str
    rating: float
    url: str
    title: str
    content: str
    trip_type: TripType

    @classmethod
    def from_place(cls, review):
        trip_type = review.get("trip_type", "")
        trip_type_enum = TripType(trip_type) if trip_type in TripType else TripType.UNKNOWN
        if trip_type_enum == TripType.UNKNOWN:
            print(f"Unknown trip type: {trip_type}")

        return cls(
            review["lang"],
            review["published_date"],
            review["rating"],
            review["url"],
            review["title"],
            review["text"],
            trip_type_enum,
        )

@dataclass
class TripadvisorReviewHandler(BaseTripadvisorContent):
    reviews: List[TripadvisorReview]

    @classmethod
    def from_place(cls, location_id: int, place_reviews):
        return cls(
            location_id,
            [TripadvisorReview.from_place(review) for review in place_reviews["data"]]
        )

@dataclass
class TripadvisorFullContent:
    details: TripadvisorLocationDetailsHandler
    reviews: TripadvisorReviewHandler
