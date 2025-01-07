import bisect
from datetime import datetime
from typing import List, Dict, Tuple
from models.property import Property
from models.schemas import StatusEnum
from config.errors import ERROR_MESSAGES
import threading


class PropertySearch:
    def __init__(self, properties: Dict[str, Property], price_index: List[tuple], location_index: Dict[str, List[str]]):
        """
        Initialize the search system with:
            `properties`: Central dictionary of all properties
            `price_index`: Sorted list of (price, property_id) tuples
            `location_index`: Dictionary of location -> List of property IDs
        """
        self.properties = properties
        self.price_index = price_index
        self.location_index = location_index
        self.lock = threading.Lock()  # Lock for concurrent write operations

    def search_properties(self, criteria: dict) -> List[Property]:
        """
        Search properties based on Price range, Location, Property type
        Parameters:
            `criteria`: A dictionary with search filters like `min_price`, `max_price`, `location`, `property_type`.
        Returns:
            List of filtered Property objects
        """
        # Initial result: all properties
        filtered_properties = set(self.properties.keys())

        # Apply price range filter
        min_price = float("-inf") if criteria.get("min_price",None) is None else criteria.get("min_price")
        max_price = float("inf") if criteria.get("max_price",None) is None else criteria.get("max_price")
        filtered_properties &= set(self._filter_by_price(min_price, max_price))

        # Apply location filter
        location = criteria.get("location")
        if location:
            filtered_properties &= set(self.location_index.get(location, []))

        # Apply property type filter
        property_type = criteria.get("property_type")
        if property_type:
            filtered_properties = set(
                prop_id for prop_id in filtered_properties
                if self.properties[prop_id].property_type == property_type
            )

        # Apply status filter
        status = criteria.get("status", StatusEnum.AVAILABLE)
        filtered_properties = set(
            prop_id for prop_id in filtered_properties
            if self.properties[prop_id].status == status
        )

        # Convert to list of Property objects
        result = [self.properties[prop_id] for prop_id in filtered_properties]

        # Apply sorting
        sort_key = criteria.get("sort_key", "price")  # Default sort by price
        descending = criteria.get("descending", False)
        result = sorted(result, key=lambda x: getattr(x, sort_key), reverse=descending)

        # Apply pagination
        page = criteria.get("page", 1)
        limit = criteria.get("limit", 10)
        start = (page - 1) * limit
        end = start + limit
        return result[start:end]

    def _filter_by_price(self, min_price: float, max_price: float) -> List[str]:
        """
        Filter property IDs by price range using binary search for efficiency.
        Returns:
            List of property IDs in the specified price range.
        """
        # Define the target ranges for binary search
        start_index = bisect.bisect_left(self.price_index, (min_price, ""))
        end_index = bisect.bisect_right(self.price_index, (max_price, ""))
        # bisect_right stops at the first element greater than or equal to the max price.
        while end_index < len(self.price_index) and self.price_index[end_index][0] == max_price:
            end_index += 1
        # Slice the range and extract property IDs
        return [property_id for _, property_id in self.price_index[start_index:end_index]]


    def get_shortlisted(self, user_id: str, user_shortlists: Dict[str, List[Tuple[datetime,str]]]) -> List[Property]:
        """
        Get the user's shortlisted properties:
        Parameters:
            `user_id`: ID of the user
            `user_shortlists`: Dictionary mapping user IDs to list of (timestamp,property IDs)
        Returns:
            List of Property objects
        """
        if user_id not in user_shortlists:
            return []

        shortlisted_properties = [
            self.properties[prop_id]
            for _, prop_id in reversed(user_shortlists[user_id])
            if self.properties[prop_id].status == StatusEnum.AVAILABLE
        ]

        return shortlisted_properties


    def shortlist_property(self, user_id: str, property_id: str, user_shortlists: Dict[str, List[Tuple[datetime,str]]]) -> Tuple[bool,str]:
        """
        Add a property to the user's shortlist:
        Parameters:
            `user_id`: ID of the user
            `property_id`: ID of the property to shortlist
            `user_shortlists`: Dictionary mapping user IDs to list of (timestamp,property IDs)
        Returns:
            `True` if successfully shortlisted, `False` otherwise with a message
        """
        with self.lock:  # Lock the critical section
            if property_id not in self.properties:
                return False, ERROR_MESSAGES["PROPERTY_NOT_EXIST"] # Property doesn't exist
    
            if user_id not in user_shortlists:
                user_shortlists[user_id] = []
    
            if any(prop_id == property_id for _, prop_id in user_shortlists[user_id]):
                return False, ERROR_MESSAGES["ALREADY_SHORTLISTED"]

            bisect.insort(user_shortlists[user_id], (datetime.now(), property_id))  # keep the shortlist in sorted order of shortlist time 
            return True, ""

    
    def remove_shortlist_property(self, user_id: str, property_id: str, user_shortlists: Dict[str, List[Tuple[datetime,str]]]) -> Tuple[bool,str]:
        """
        Remove a property from the user's shortlist:
        Parameters:
            `user_id`: ID of the user
            `property_id`: ID of the property to shortlist
            `user_shortlists`: Dictionary mapping user IDs to list of (timestamp,property IDs)
        Returns:
            `True` if successfully removed, `False` otherwise with a message
        """
        with self.lock:
            if user_id not in user_shortlists:
                return False, ERROR_MESSAGES["EMPTY_SHORTLIST"]

            # Check if the property exists in the shortlist
            user_shortlist = user_shortlists[user_id]
            if not any(prop_id == property_id for _,prop_id in user_shortlist):
                return False, ERROR_MESSAGES["NOT_IN_SHORTLIST"]
            
            # Remove the property from the shortlist
            user_shortlists[user_id] = [
                entry for entry in user_shortlist if entry[1] != property_id
            ]
    
            return True, ""