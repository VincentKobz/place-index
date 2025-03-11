from restaurant.generic_places import Contact, Features

tags_data = [
    (["italian", "pasta"], ["italian", "pizza"], ["italian", "pasta", "pizza"]),
    (["italian", "pasta"], ["italian", "pasta"], ["italian", "pasta"]),
    (["italian", "pasta"], ["pizza"], ["italian", "pasta", "pizza"]),
    ([], ["pizza"], ["pizza"]),
    (["pizza"], [], ["pizza"]),
    ([], [], []),
]

contact_data = [
    (
        Contact(
            phone="123",
            email="test@test.com",
            website="www.website.com",
            address="123 test rue du test",
            gmaps_uri="gmaps_uri",
            tripadvisor_uri="tripadvisor uri",
            specific_uri="",
        ),
        Contact(
            phone="123",
            email="test@test.com",
            website="www.website.com",
            address="123 test rue du test",
            gmaps_uri="gmaps_uri",
            tripadvisor_uri="tripadvisor uri",
            specific_uri="",
        ),
        Contact(
            phone="123",
            email="test@test.com",
            website="www.website.com",
            address="123 test rue du test",
            gmaps_uri="gmaps_uri",
            tripadvisor_uri="tripadvisor uri",
            specific_uri="",
        ),
    ),
    (
        Contact(
            phone="",
            email="test@test.com",
            website="",
            address="123 test rue du test",
            gmaps_uri="gmaps_uri",
            tripadvisor_uri="tripadvisor uri",
            specific_uri="",
        ),
        Contact(
            phone="123",
            email="",
            website="www.website.com",
            address="test rue du test",
            gmaps_uri="",
            tripadvisor_uri="tripadvisor uri",
            specific_uri="",
        ),
        Contact(
            phone="123",
            email="test@test.com",
            website="www.website.com",
            address="123 test rue du test",
            gmaps_uri="gmaps_uri",
            tripadvisor_uri="tripadvisor uri",
            specific_uri="",
        ),
    ),
    (
        Contact(
            phone="",
            email="",
            website="",
            address="",
            gmaps_uri="",
            tripadvisor_uri="",
            specific_uri="",
        ),
        Contact(
            phone="123",
            email="test@test.com",
            website="www.website.com",
            address="test rue du test",
            gmaps_uri="gmaps_uri",
            tripadvisor_uri="tripadvisor uri",
            specific_uri="",
        ),
        Contact(
            phone="123",
            email="test@test.com",
            website="www.website.com",
            address="test rue du test",
            gmaps_uri="gmaps_uri",
            tripadvisor_uri="tripadvisor uri",
            specific_uri="",
        ),
    ),
]

feature_data = [
    (
        Features(
            credit_card=True,
            serve_alcohol=True,
            is_accessible=True,
            takeout=True,
            seating=True,
            wifi=True,
            reservation=True,
            parking=True,
            dog_allowed=True,
        ),
        Features(
            credit_card=True,
            serve_alcohol=True,
            is_accessible=True,
            takeout=True,
            seating=True,
            wifi=True,
            reservation=True,
            parking=True,
            dog_allowed=True,
        ),
        Features(
            credit_card=True,
            serve_alcohol=True,
            is_accessible=True,
            takeout=True,
            seating=True,
            wifi=True,
            reservation=True,
            parking=True,
            dog_allowed=True,
        ),
    ),
    (
        Features(
            credit_card=True,
            serve_alcohol=True,
            is_accessible=True,
            takeout=True,
            seating=True,
            wifi=True,
            reservation=True,
            parking=True,
            dog_allowed=True,
        ),
        Features(
            credit_card=False,
            serve_alcohol=False,
            is_accessible=False,
            takeout=False,
            seating=False,
            wifi=False,
            reservation=False,
            parking=False,
            dog_allowed=False,
        ),
        Features(
            credit_card=True,
            serve_alcohol=True,
            is_accessible=True,
            takeout=True,
            seating=True,
            wifi=True,
            reservation=True,
            parking=True,
            dog_allowed=True,
        ),
    ),
    (
        Features(
            credit_card=False,
            serve_alcohol=False,
            is_accessible=False,
            takeout=False,
            seating=False,
            wifi=False,
            reservation=False,
            parking=False,
            dog_allowed=False,
        ),
        Features(
            credit_card=True,
            serve_alcohol=True,
            is_accessible=True,
            takeout=True,
            seating=True,
            wifi=True,
            reservation=True,
            parking=True,
            dog_allowed=True,
        ),
        Features(
            credit_card=True,
            serve_alcohol=True,
            is_accessible=True,
            takeout=True,
            seating=True,
            wifi=True,
            reservation=True,
            parking=True,
            dog_allowed=True,
        ),
    ),
    (
        Features(
            credit_card=True,
            serve_alcohol=False,
            is_accessible=True,
            takeout=False,
            seating=True,
            wifi=False,
            reservation=True,
            parking=False,
            dog_allowed=True,
        ),
        Features(
            credit_card=False,
            serve_alcohol=True,
            is_accessible=False,
            takeout=True,
            seating=False,
            wifi=True,
            reservation=False,
            parking=True,
            dog_allowed=False,
        ),
        Features(
            credit_card=True,
            serve_alcohol=True,
            is_accessible=True,
            takeout=True,
            seating=True,
            wifi=True,
            reservation=True,
            parking=True,
            dog_allowed=True,
        ),
    ),
]

list_data = [
    (["a", "b", "c"], ["b", "c", "d"], ["a", "b", "c", "d"]),
    (["a", "b", "c", "a", "a"], ["b", "c", "d"], ["a", "b", "c", "d"]),
    (["a", "b", "c"], ["a", "b", "c"], ["a", "b", "c"]),
    (["a", "b", "c"], [], ["a", "b", "c"]),
    ([], ["a", "b", "c"], ["a", "b", "c"]),
    ([], [], []),
]
