from dataclasses import dataclass
from typing import List

from place_index.metadatas import PriceLevel, Atmosphere


@dataclass
class Contact:
    phone: str
    email: str
    website: str
    address: str
    gmaps_uri: str | None
    tripadvisor_uri: str | None
    specific_uri: str


@dataclass
class Features:
    credit_card: bool
    serve_alcohol: bool
    is_accessible: bool
    takeout: bool
    seating: bool
    wifi: bool
    reservation: bool
    parking: bool
    dog_allowed: bool


@dataclass
class Reviews:
    rating: float
    lang: str
    title: str
    content: str
    publication_date: str | None


@dataclass
class Restaurant:
    id: str
    name: str
    rating: float
    types: list
    price_level: List[PriceLevel]
    atmosphere_target: List[Atmosphere]
    contact: Contact
    features: Features
    reviews: List[Reviews]
    number_of_reviews: int

    @classmethod
    def from_json(cls, json):
        new_instance = cls(**json)
        new_instance.contact = Contact(**json["contact"])
        new_instance.features = Features(**json["features"])
        new_instance.reviews = [Reviews(**review) for review in json["reviews"]]

        return new_instance

    def is_exploitable(self):
        """
        Check if the place_index is exploitable (has enough basic information)
        :return:
        """
        return self.name != "" and self.rating != -1 and self.contact.address != ""

    def is_data_qualitative(self):
        """
        Check if the place_index has qualitative data (has enough qualitative information to be exploitable)
        :return:
        """
        return (
            self.is_exploitable()
            and self.price_level != PriceLevel.UNKNOWN
            and len(self.types) > 0
            and len(self.reviews) > 0
            and any(self.features.__dict__.values())
        )
