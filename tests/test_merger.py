import pytest
from pygments.lexer import default

from place_index.generic_places import Restaurant
from place_index.merger.merger import Merger
from tests.test_fixture import tags_data, contact_data, feature_data, list_data


@pytest.fixture
def no_llm_merger():
    return Merger(use_llm=False)


@pytest.mark.parametrize("first_list, second_list, expected", list_data)
def test_merge_list_unique(first_list, second_list, expected):
    result = Merger.merge_list_unique(first_list, second_list)
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize("existing_tags, new_tags, expected", tags_data)
def test_merge_tags_without_llm(no_llm_merger, existing_tags, new_tags, expected):
    existing_restaurant = Restaurant(
        id="",
        name="",
        rating=default,
        price_level=default,
        atmosphere_target=default,
        types=existing_tags,
        contact=default,
        features=default,
        reviews=default,
    )
    new_restaurant = Restaurant(
        id="",
        name="",
        rating=default,
        price_level=default,
        atmosphere_target=default,
        types=new_tags,
        contact=default,
        features=default,
        reviews=default,
    )
    no_llm_merger.merge_tags(existing_restaurant, new_restaurant)

    assert sorted(existing_restaurant.types) == sorted(expected)


@pytest.mark.parametrize("existing_contact, new_contact, expected", contact_data)
def test_merge_contacts(no_llm_merger, existing_contact, new_contact, expected):
    existing_restaurant = Restaurant(
        id="",
        name="",
        rating=default,
        price_level=default,
        atmosphere_target=default,
        types=default,
        contact=existing_contact,
        features=default,
        reviews=default,
    )
    new_restaurant = Restaurant(
        id="",
        name="",
        rating=default,
        price_level=default,
        atmosphere_target=default,
        types=default,
        contact=new_contact,
        features=default,
        reviews=default,
    )
    no_llm_merger.merge_contacts(existing_restaurant, new_restaurant)

    assert existing_restaurant.contact == expected


@pytest.mark.parametrize("existing_feature, new_feature, expected", feature_data)
def test_merge_features(no_llm_merger, existing_feature, new_feature, expected):
    existing_restaurant = Restaurant(
        id="",
        name="",
        rating=default,
        price_level=default,
        atmosphere_target=default,
        types=default,
        contact=default,
        features=existing_feature,
        reviews=default,
    )
    new_restaurant = Restaurant(
        id="",
        name="",
        rating=default,
        price_level=default,
        atmosphere_target=default,
        types=default,
        contact=default,
        features=new_feature,
        reviews=default,
    )
    no_llm_merger.merge_features(existing_restaurant, new_restaurant)

    assert existing_restaurant.features == expected
