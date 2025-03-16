import logging
from abc import ABC, abstractmethod
from typing import List

from place_index.generic_places import Restaurant
from place_index.gmaps.gmaps_api_handler import (
    GooglePlacesApi,
    gmaps_place_nearby_handler,
)
from place_index.metadatas import ProviderSource
from place_index.tripadvisor.tripadvisor_api_handler import (
    TripadvisorApiHandler,
    tripadvisor_place_handler,
)


class Provider(ABC):
    @abstractmethod
    def fetch(self, coordinates: List[int], distance: int) -> dict[int, Restaurant]:
        pass


class TripadvisorProvider(Provider):
    def fetch(self, coordinates: List[int], distance: int) -> dict[int, Restaurant]:
        """
        Fetch the data from the tripadvisor provider
        @param coordinates:
        @param distance:
        @return:
        """
        tripadvisor_restaurants = {}
        tripadvisor_api_handler = TripadvisorApiHandler()
        for idx, (latitude, longitude) in enumerate(coordinates):
            places = tripadvisor_api_handler.fetch_all(latitude, longitude, distance)
            local_restaurants = tripadvisor_place_handler(places)
            tripadvisor_restaurants.update(local_restaurants)

        return tripadvisor_restaurants


class GoogleMapsProvider(Provider):
    def fetch(self, coordinates: List[int], distance: int) -> dict[int, Restaurant]:
        """
        Fetch the data from the gmaps place provider
        @param coordinates:
        @param distance:
        @return:
        """
        gmaps_restaurants = {}
        gmaps_api = GooglePlacesApi()
        for idx, (latitude, longitude) in enumerate(coordinates):
            response = gmaps_api.google_api_wrapper(latitude, longitude, distance)
            if not response.ok:
                logging.warning(
                    f"Google Maps API request failed: {response.status_code}"
                )
                continue

            restaurants = gmaps_place_nearby_handler(response)

            for restaurant in restaurants:
                gmaps_restaurants[restaurant.id] = restaurant

        return gmaps_restaurants


class Fetcher:
    def __init__(self):
        self.providers = []

    def add_provider(self, provider: ProviderSource):
        """
        Add a place provider to the fetcher engine
        @param provider:
        @return:
        """
        logging.info(f"Adding provider: {provider.value}")

        match provider:
            case ProviderSource.GOOGLE_MAPS:
                self.providers.append(GoogleMapsProvider())
            case ProviderSource.TRIPADVISOR:
                self.providers.append(TripadvisorProvider())
            case _:
                logging.warning(f"Unknown provider: {provider.value}")

    def fetch_all(self, coordinates) -> dict[int, Restaurant]:
        """
        Fetch all the data place from the loaded providers
        @return:
        """
        if not self.providers:
            logging.warning("No providers added to fetcher.")

        results = {}
        for provider in self.providers:
            logging.info(f"Fetching data from provider: {provider.__class__.__name__}")
            results.update(provider.fetch(coordinates, 100))

        return results
