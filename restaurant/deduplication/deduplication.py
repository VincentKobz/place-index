from dataclasses import dataclass
from vectordb import Memory

from restaurant.generic_places import Restaurant

@dataclass
class QueryResult:
    chunk: str
    metadata: dict
    distance: float

    @classmethod
    def from_json(cls, json):
        return cls(**json)


class VectorDb:
    """
    Class to handle the deduplication of restaurants using a vector database
    """
    memory = Memory()
    nb_items = 0

    def add_restaurant(self, restaurant: Restaurant):
        """
        Add a restaurant to the vector db
        @param restaurant:
        @return:
        """
        self.memory.save(restaurant.name, [restaurant.id])
        self.nb_items += 1

    def get_restaurant(self, restaurant: Restaurant) -> QueryResult:
        """
        Get a restaurant from the vector db
        @param restaurant:
        @return:
        """
        if self.nb_items == 0:
            return QueryResult(chunk="", metadata={}, distance=1.0)
        result = self.memory.search(restaurant.name, top_n=1)
        return QueryResult.from_json(result[0])

