import logging
from typing import Dict, List, TypedDict

from place_index.deduplication.deduplication import VectorDb, QueryResult
from place_index.fetcher.provider import ProviderSource
from place_index.merger.llm_handler import LLMHandler
from place_index.generic_places import Restaurant


class PlaceSource(TypedDict):
    gmaps_id: str
    tripadvisor_id: str
    source_provider: ProviderSource


class Merger:
    places: Dict[str, Restaurant] = {}
    merged_places: Dict[str, PlaceSource] = {}
    vector_db = VectorDb()

    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.llm_handler = LLMHandler() if use_llm else None
        self.match_threshold = 0.35

    def add_restaurants(self, restaurants: Dict[int, Restaurant]):
        """
        Add a list of restaurants to the merger
        :param restaurants:
        :return:
        """
        for restaurant in restaurants.values():
            self.add_restaurant(restaurant)

    def merge_tags(self, existing_restaurant: Restaurant, new_restaurant: Restaurant):
        if self.use_llm:
            new_tags = self.llm_handler.merge_tags(
                existing_restaurant.types, new_restaurant.types
            )
        else:
            new_tags = self.merge_list_unique(
                existing_restaurant.types, new_restaurant.types
            )

        logging.debug(
            f"Merging tags: {existing_restaurant.types} with {new_restaurant.types} -> {new_tags}"
        )
        existing_restaurant.types = new_tags

    @staticmethod
    def merge_contacts(existing_restaurant: Restaurant, new_restaurant: Restaurant):
        """
        Merge the contact information of two restaurants
        @param existing_restaurant:
        @param new_restaurant:
        @return:
        """
        existing_restaurant.contact.phone = (
            existing_restaurant.contact.phone or new_restaurant.contact.phone
        )
        existing_restaurant.contact.email = (
            existing_restaurant.contact.email or new_restaurant.contact.email
        )
        existing_restaurant.contact.website = (
            existing_restaurant.contact.website or new_restaurant.contact.website
        )
        existing_restaurant.contact.address = (
            existing_restaurant.contact.address or new_restaurant.contact.address
        )
        existing_restaurant.contact.gmaps_uri = (
            existing_restaurant.contact.gmaps_uri or new_restaurant.contact.gmaps_uri
        )
        existing_restaurant.contact.tripadvisor_uri = (
            existing_restaurant.contact.tripadvisor_uri
            or new_restaurant.contact.tripadvisor_uri
        )

    @staticmethod
    def merge_list_unique(first_list: List, second_list: List) -> List:
        """
        Merge two lists without duplicates
        @param first_list:
        @param second_list:
        @return:
        """
        return list(set(first_list + second_list))

    @staticmethod
    def merge_features(existing_restaurant: Restaurant, new_restaurant: Restaurant):
        """
        Merge the features of two restaurants
        @param existing_restaurant:
        @param new_restaurant:
        @return:
        """
        existing_restaurant.features.credit_card = (
            existing_restaurant.features.credit_card
            or new_restaurant.features.credit_card
        )
        existing_restaurant.features.serve_alcohol = (
            existing_restaurant.features.serve_alcohol
            or new_restaurant.features.serve_alcohol
        )
        existing_restaurant.features.is_accessible = (
            existing_restaurant.features.is_accessible
            or new_restaurant.features.is_accessible
        )
        existing_restaurant.features.takeout = (
            existing_restaurant.features.takeout or new_restaurant.features.takeout
        )
        existing_restaurant.features.seating = (
            existing_restaurant.features.seating or new_restaurant.features.seating
        )
        existing_restaurant.features.wifi = (
            existing_restaurant.features.wifi or new_restaurant.features.wifi
        )
        existing_restaurant.features.reservation = (
            existing_restaurant.features.reservation
            or new_restaurant.features.reservation
        )
        existing_restaurant.features.parking = (
            existing_restaurant.features.parking or new_restaurant.features.parking
        )
        existing_restaurant.features.dog_allowed = (
            existing_restaurant.features.dog_allowed
            or new_restaurant.features.dog_allowed
        )

    @staticmethod
    def merge_reviews(existing_restaurant: Restaurant, new_restaurant: Restaurant):
        """
        Merge the reviews of two restaurants
        @param existing_restaurant:
        @param new_restaurant:
        @return:
        """
        existing_restaurant.reviews += new_restaurant.reviews

    @staticmethod
    def get_provider_type(restaurant: Restaurant) -> ProviderSource:
        """
        Get the provider of a place_index
        @param restaurant:
        @return:
        """
        match restaurant:
            case restaurant.contact.gmaps_uri:
                return ProviderSource.GOOGLE_MAPS
            case restaurant.contact.tripadvisor_uri:
                return ProviderSource.TRIPADVISOR

    @staticmethod
    def merge_rating(
        rating: float, new_rating: float, nb_reviews: int, new_nb_reviews: int
    ) -> float:
        """
        Merge the rating of two restaurants
        @param new_nb_reviews:
        @param nb_reviews:
        @param rating:
        @param new_rating:
        @return:
        """
        total_number_reviews = nb_reviews + new_nb_reviews

        existing_rating_ratio = nb_reviews / total_number_reviews
        restaurant_rating_ratio = new_nb_reviews / total_number_reviews

        return rating * existing_rating_ratio + new_rating * restaurant_rating_ratio

    def add_restaurant(self, restaurant: Restaurant):
        """
        Add a place to the merger
        :param restaurant:
        :return:
        """
        logging.debug(f"Trying to add {restaurant.name}")

        query_result: QueryResult = self.vector_db.get_restaurant(restaurant)

        if query_result.distance < self.match_threshold:
            existing_restaurant = self.places[query_result.match]
            logging.info(
                f"Found a match with {existing_restaurant.name} with {restaurant.name}. Distance: {query_result.distance}"
                f"Address: {existing_restaurant.contact.address} -> {restaurant.contact.address}"
            )

            self.merge_tags(existing_restaurant, restaurant)
            self.merge_contacts(existing_restaurant, restaurant)
            self.merge_features(existing_restaurant, restaurant)
            self.merge_reviews(existing_restaurant, restaurant)

            existing_restaurant.atmosphere_target = self.merge_list_unique(
                existing_restaurant.atmosphere_target, restaurant.atmosphere_target
            )
            existing_restaurant.price_level = self.merge_list_unique(
                existing_restaurant.price_level, restaurant.price_level
            )

            existing_restaurant.rating = self.merge_rating(
                existing_restaurant.rating,
                restaurant.rating,
                existing_restaurant.number_of_reviews,
                restaurant.number_of_reviews,
            )

            existing_restaurant.number_of_reviews += restaurant.number_of_reviews

            source_provider = self.get_provider_type(restaurant)
            self.merged_places[restaurant.id] = PlaceSource(
                gmaps_id=existing_restaurant.contact.gmaps_uri,
                tripadvisor_id=existing_restaurant.contact.tripadvisor_uri,
                source_provider=source_provider,
            )
        else:
            logging.debug(
                f"Adding {restaurant.name} to the database, no relevant match found. Distance: {query_result.distance}"
            )

            self.vector_db.add_restaurant(restaurant)
            self.places[restaurant.name] = restaurant
