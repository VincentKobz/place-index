# Place index 📍🗺️

## What is it?

**Place index** is a *Python* library to search, index and merge places from different providers.

>For instance, if you want to search for specific places in an area, you can use this library to search on Google Maps, TripAdvisor and OpenStreet Map to get the best results, and aggregate / merge them into a single list of places.

## Why?

I wanted an easy way to look for restaurants near my workplace, and I needed an exhaustive list of places to choose from.

## Get started

Create a `.env` file in the `place_index` folder with the following content:

```bash
GMAPS_API_KEY=your_google_maps_api_key
TRIP_API_KEY=your_tripadvisor_api_key
OPEN_AI_API_KEY=your_openai_api_key
```

## Usage

### Setup and fetch data from providers

In this code snippet, we fetch restaurants around the Eiffel Tower, using Google Maps and TripAdvisor as providers.
```python
from place_index.fetcher.fetcher import Fetcher
from place_index.fetcher.provider import ProviderSource

# Add the providers you want to use (ex Google Maps or TripAdvisor)
fetcher = Fetcher(ProviderSource.GOOGLE_MAPS, ProviderSource.TRIPADVISOR)
generic_places = fetcher.fetch_all(coordinates=[(48.858265, 2.294494)])
```

### Merge the data

The data previously fetched may contain duplicates.
We are using a *nearest neighbor algorithm* to merge the data, with the optional help of a LLM (Large Language Model).

>Note: The LLM is not required, but it helps to improve the quality of the merged data, especially for places tags.
```python
from place_index.merger.merger import Merger

merger = Merger(use_llm=False)
merger.add_restaurants(generic_places)

print(merger.places)
```

Data can be easily exported to **JSON** format.
```python
import json
from dataclasses import asdict

with open("output.json", "w") as f:
    json.dump(
        {restaurant.name: asdict(restaurant) for restaurant in merger.places.values()},
        f,
    )
```
