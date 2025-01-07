from datetime import datetime

class Property:
    def __init__(self, property_id: str, user_id: str, location: str, price: float, property_type: str,
                 status: str, timestamp: datetime, description: str, amenities: list[str]):
        """
        Initializes a property with the following attributes:
        - property_id: Unique identifier for the property
        - user_id: Owner's user ID
        - location: Property location
        - price: Property price
        - property_type: e.g., Apartment, Villa
        - status: Current status ('Available' or 'Sold')
        - timestamp: Datetime object representing the listing creation time
        - description: Brief description of the property
        - amenities: List of amenities (e.g., pool, gym)
        """
        self.property_id = property_id
        self.user_id = user_id
        self.location = location
        self.price = price
        self.property_type = property_type
        self.status = status
        self.timestamp = timestamp
        self.description = description
        self.amenities = amenities
