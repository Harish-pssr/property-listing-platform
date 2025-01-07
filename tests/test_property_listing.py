import pytest

@pytest.mark.order(1)
def test_create_property(client):
    """
    Test creating a property.
    """
    response = client.post(
        "/api/v1/properties",
        json={
            "location": "New York",
            "price": 5000,
            "property_type": "Apartment",
            "description": "A beautiful 2BHK apartment",
            "amenities": ["Pool", "Gym"]
        },
        params={"user_id": "user_1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "New York"
    assert data["price"] == 5000


@pytest.mark.order(2)
def test_update_property_status(client):
    """
    Test updating the status of a property.
    """
    property_id = "property_1"

    # Update property status to 'Sold'
    response = client.patch(
        f"/api/v1/properties/{property_id}",
        params={"status": "Sold", "user_id": "user_1"}
    )
    assert response.status_code == 200

    # Try updating with an invalid status
    invalid_response = client.patch(
        f"/api/v1/properties/{property_id}",
        params={"status": "InvalidStatus", "user_id": "user_1"}
    )
    assert invalid_response.status_code == 422

    # Attempt unauthorized update
    unauthorized_response = client.patch(
        f"/api/v1/properties/{property_id}",
        params={"status": "Available", "user_id": "user_2"}
    )
    assert unauthorized_response.status_code == 403


@pytest.mark.order(3)
def test_get_user_properties(client):
    """
    Test retrieving properties owned by a user.
    """
    # Add a property for user_1
    client.post(
        "/api/v1/properties",
        json={
            "location": "Washington",
            "price": 4000,
            "property_type": "Flat",
            "description": "A beautiful 1BHK Flat",
            "amenities": ["Pool", "AC"]
        },
        params={"user_id": "user_1"}
    )

    # Fetch properties for user_1
    response = client.get("/api/v1/user/properties", params={"user_id": "user_1"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # One property is already sold

    # Add another property for user_1
    client.post(
        "/api/v1/properties",
        json={
            "location": "America",
            "price": 9600,
            "property_type": "Apartment",
            "description": "Spacious 2 BHK",
            "amenities": ["Fridge", "AC"]
        },
        params={"user_id": "user_1"}
    )

    # Fetch updated properties
    response = client.get("/api/v1/user/properties", params={"user_id": "user_1"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2  # Two available properties


@pytest.mark.order(4)
def test_add_shortlist_property(client):
    """
    Test adding a property to the user's shortlist.
    """
    property_id = "property_3"
    response = client.post(
        f"/api/v1/user/shortlist/{property_id}",
        params={"user_id": "user_1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Property {property_id} has been successfully added to your shortlist."


@pytest.mark.order(5)
def test_get_shortlist_properties(client):
    """
    Test retrieving shortlisted properties for a user.
    """
    response = client.get("/api/v1/user/shortlist", params={"user_id": "user_1"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # One property is shortlisted


@pytest.mark.order(6)
def test_remove_shortlist_property(client):
    """
    Test removing a property from the user's shortlist.
    """
    property_id = "property_3"

    # Remove the property from the shortlist
    response = client.delete(
        f"/api/v1/user/shortlist/{property_id}",
        params={"user_id": "user_1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Property {property_id} has been successfully removed from your shortlist."

    # Verify the shortlist is now empty
    response = client.get("/api/v1/user/shortlist", params={"user_id": "user_1"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.order(7)
def test_search_properties(client):
    """
    Test searching for properties within a price range.
    """
    response = client.get(
        "/api/v1/properties/search",
        params={"min_price": 5000, "max_price": 10000}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # Out of three properties, only one is within the range (9600)
