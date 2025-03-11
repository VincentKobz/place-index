from typing import List

import mrpt
import numpy as np
from fastembed import TextEmbedding

from dataclasses import dataclass

from restaurant.generic_places import Restaurant


@dataclass
class QueryResult:
    match: str
    distance: float

    @classmethod
    def from_json(cls, json):
        return cls(**json)


class VectorDb:
    """
    Class to handle the deduplication of restaurants using a vector database
    """

    def __init__(self):
        # Use the default model to perform text embedding
        self.embedding_memory: List[dict] = []
        self.embedding_model = TextEmbedding()

    def embed_restaurants(self, restaurant: Restaurant):
        embedded_vector_place_name = list(self.embedding_model.embed(restaurant.name))[
            0
        ]

        return np.array(embedded_vector_place_name).astype(np.float32)

    def add_restaurant(self, restaurant: Restaurant):
        """
        Add a restaurant to the vector db
        @param restaurant:
        @return:
        """
        self.embedding_memory.append(
            {
                "embedded_vector": self.embed_restaurants(restaurant),
                "restaurant": restaurant.name,
            }
        )

    def get_restaurant(self, restaurant: Restaurant) -> QueryResult:
        """
        Get a restaurant from the vector db
        @param restaurant:
        @return:
        """
        if len(self.embedding_memory) == 0:
            return QueryResult("", 1)

        embedded_vector_place_name = self.embed_restaurants(restaurant)
        embedded_vectors = [
            self.embedding_memory[i]["embedded_vector"]
            for i in range(len(self.embedding_memory))
        ]
        index = mrpt.MRPTIndex(np.array(embedded_vectors).astype(np.float32))
        indexes, distances = index.exact_search(
            embedded_vector_place_name, 1, return_distances=True
        )

        return QueryResult.from_json(
            {
                "match": self.embedding_memory[indexes[0]]["restaurant"],
                "distance": distances[0].astype(float),
            }
        )
