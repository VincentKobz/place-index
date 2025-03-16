import logging
from typing import List, Dict

from place_index.generic_places import Restaurant
from place_index.tripadvisor.tripadivsor_types import (
    TripadvisorFullContent,
    TripadvisorNearbyHandler,
    TripadvisorLocationDetailsHandler,
    TripadvisorReviewHandler,
)
from place_index.tripadvisor.tripadvisor_api import TripAdvisorApi
from place_index.tripadvisor.tripadvisor_integrator import tripadvisor_place_convertor


class TripadvisorApiHandler:
    def __init__(self):
        self.tripadvisor = TripAdvisorApi()
        self.location_reviews_error = 0
        self.location_details_error = 0
        self.location_search_error = 0

    def fetch_all(
        self, lat: float, long: float, distance: int
    ) -> dict[int, TripadvisorFullContent]:
        """
        Fetch all the data from the tripadvisor api
        :param lat:
        :param long:
        :param distance:
        :return:
        """
        tripadvisor_restaurants = {}
        nearby_places = self.search_nearby(lat, long, distance)
        location_details = self.location_details(list(nearby_places.keys()))
        location_reviews = self.location_reviews(list(nearby_places.keys()))

        for place in nearby_places.values():
            current_details = location_details.get(place.location_id, None)
            current_reviews = location_reviews.get(place.location_id, None)

            if not current_details or not current_reviews:
                logging.error(
                    f"Tripadvisor API request failed: {self.location_details_error}, {self.location_reviews_error}"
                )
                continue

            tripadvisor_restaurants[place.location_id] = TripadvisorFullContent(
                current_details, current_reviews
            )

        return tripadvisor_restaurants

    def search_nearby(
        self, lat, long, distance: int
    ) -> Dict[int, TripadvisorNearbyHandler]:
        """
        Get the restaurants nearby using the tripadvisor nearby search api
        :param lat:
        :param long:
        :param distance:
        :return:
        """
        self.location_search_error = 0
        response = self.tripadvisor.api_nearby_wrapper(lat, long, distance)
        if not response.ok:
            logging.error(
                f"Tripadvisor API request failed: {response.status_code}, response: {response.text}"
            )
            self.location_search_error += 1
            return {}

        places = [
            TripadvisorNearbyHandler.from_place(place)
            for place in response.json()["data"]
        ]

        return {place.location_id: place for place in places}

    def location_details(
        self, place_locations: List[int]
    ) -> Dict[int, TripadvisorLocationDetailsHandler]:
        """
        Get the details of a location using the tripadvisor details api
        :param place_locations:
        :return:
        """
        self.location_details_error = 0
        results = {}
        for location_id in place_locations:
            response = self.tripadvisor.api_details_wrapper(location_id)
            if not response.ok:
                logging.error(
                    f"Tripadvisor API request failed: {response.status_code}, response: {response.text}"
                )
                self.location_details_error += 1
                continue

            place_detail = TripadvisorLocationDetailsHandler.from_place(response.json())
            results[place_detail.location_id] = place_detail
        return results

    def location_reviews(
        self, place_details: List[int]
    ) -> Dict[int, TripadvisorReviewHandler]:
        """
        Get reviews from tripadvisor using the location id
        :param place_details:
        :return:
        """
        self.location_reviews_error = 0
        results = {}
        for location_id in place_details:
            response = self.tripadvisor.api_tripadvisor_reviews(location_id)
            if not response.ok:
                logging.error(
                    f"Tripadvisor API request failed: {response.status_code}, response: {response.text}"
                )
                self.location_reviews_error += 1
                continue

            response_content = response.json()
            if "data" not in response_content:
                self.location_reviews_error += 1
                continue

            place = TripadvisorReviewHandler.from_place(location_id, response_content)
            results[place.location_id] = place

        return results


def tripadvisor_place_handler(trip_places: Dict[int, TripadvisorFullContent]):
    local_restaurants = {}
    not_exploitable = 0
    for place in trip_places.values():
        current_restaurant: Restaurant = tripadvisor_place_convertor(place)
        if current_restaurant.is_exploitable():
            local_restaurants[current_restaurant.id] = current_restaurant
        else:
            not_exploitable += 1

    return local_restaurants
