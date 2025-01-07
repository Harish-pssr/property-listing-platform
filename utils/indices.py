import bisect

def add_to_indices(price_index, location_index, property_obj):
    """
    Adds a property to the price and location indices.
    Args:
        price_index (list): The sorted list of (price, property_id) tuples.
        location_index (dict): The dictionary mapping locations to property IDs.
        property_obj: The property object to add to the indices.
    """
    # Add to price index
    bisect.insort(price_index, (property_obj.price, property_obj.property_id))

    # Add to location index
    if property_obj.location not in location_index:
        location_index[property_obj.location] = []
    location_index[property_obj.location].append(property_obj.property_id)

def remove_from_indices(price_index, location_index, property_obj):
    """
    Removes a property from the price and location indices.
    Args:
        price_index (list): The sorted list of (price, property_id) tuples.
        location_index (dict): The dictionary mapping locations to property IDs.
        property_obj: The property object to remove from the indices.
    """
    # Remove from price index using bisect to find the position
    index = bisect.bisect_left(price_index, (property_obj.price, property_obj.property_id))

    # Check if the element exists at the found position
    if index < len(price_index) and price_index[index] == (property_obj.price, property_obj.property_id):
        del price_index[index]  # Remove the element efficiently

    # Remove from location index
    if property_obj.location in location_index:
        location_index[property_obj.location].remove(property_obj.property_id)
        # Clean up empty lists
        if not location_index[property_obj.location]:
            del location_index[property_obj.location]
