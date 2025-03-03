from enum import Enum

GMAPS_URL = "https://places.googleapis.com/v1/places:searchNearby"
TRIPADVISOR_URL = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"

class PriceLevel(str, Enum):
    LOW: str = "LOW"
    MEDIUM: str = "MEDIUM"
    HIGH: str = "HIGH"
    VERY_HIGH: str = "VERY_HIGH"
    UNKNOWN: str = "UNKNOWN"
    FREE: str = "FREE"

class Atmosphere(str, Enum):
    SOLO = "Solo travel"
    COUPLES = "Couples"
    FAMILY = "Family"
    FRIENDS = "Friends getaway"
    GROUPS = "Groups"
    BUSINESS = "Business"
    SPORT = "Sport"
    UNKNOWN = "Unknown"
