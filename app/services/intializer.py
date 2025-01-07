from services.property_manager import PropertyManager
from services.search_manager import PropertySearch

# Shared PropertyManager instance
property_manager = PropertyManager()

# Shared PropertySearch instance, initialized with the PropertyManager's data
property_search = PropertySearch(
    properties=property_manager.properties,
    price_index=property_manager.price_index,
    location_index=property_manager.location_index,
)