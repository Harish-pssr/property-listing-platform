from datetime import datetime
from typing import List, Dict, Tuple
import threading
from models.property import Property
from models.schemas import StatusEnum, PropertyDetail
from utils.indices import add_to_indices, remove_from_indices
from config.errors import ERROR_MESSAGES 


class PropertyManager:
    def __init__(self):
        """
        Initialize Property storage, User Shortlists, Search indices
        """
        self.properties: Dict[str, Property] = {}  # Dictionary of property_id -> Property
        self.user_shortlists: Dict[str, List[Tuple[datetime,str]]] = {}  # Dictionary of user_id -> List of shortlisted (timestamp,property ID)
        self.price_index: List[tuple] = []  # Sorted list of (price, property_id) for efficient range filtering
        self.location_index: Dict[str, List[str]] = {}  # Dictionary of location -> List of property IDs
        self.lock = threading.Lock()  # Lock for concurrent write operations

    def add_property(self, user_id: str, property_details: dict) -> PropertyDetail:
        """
        Add a new property listing
        Returns:
            created property object
        """
        with self.lock:  # Lock the critical section
            # Generate unique property ID
            property_id = f"property_{len(self.properties) + 1}"

            # Create a new Property instance
            new_property = Property(
                property_id=property_id,
                user_id=user_id,
                location=property_details["location"],
                price=property_details["price"],
                property_type=property_details["property_type"],
                status="Available",
                timestamp=datetime.now(),
                description=property_details.get("description"),
                amenities=property_details.get("amenities")
            )

            # Store the property
            self.properties[property_id] = new_property

            # Update indices
            add_to_indices(self.price_index,self.location_index,new_property)

            return new_property

    def update_property_status(self, property_id: str, status: str, user_id: str) -> Tuple[bool,str]:
        """
        Update property status:
        Returns:
        - True if successful, False otherwise with a message
        """
        with self.lock:  # Lock the critical section
            if property_id not in self.properties:
                return False, ERROR_MESSAGES["PROPERTY_NOT_EXIST"]   # Property does not exist

            property_obj = self.properties[property_id]

            if property_obj.user_id != user_id:
                return False, ERROR_MESSAGES["UNAUTHORIZED"]  # User does not own this property
            
            if property_obj.status == status:
                return False, ERROR_MESSAGES["STATUS_UNCHANGED"]  # Property is already in required status

            # Remove property from indices if changing to 'Sold'
            if property_obj.status == StatusEnum.AVAILABLE and status == StatusEnum.SOLD:
                remove_from_indices(self.price_index,self.location_index,property_obj)

            # Add property back to indices if changing to 'Available'
            if property_obj.status == StatusEnum.SOLD and status == StatusEnum.AVAILABLE:
                add_to_indices(self.price_index,self.location_index,property_obj)

            # Update the status
            property_obj.status = status
            return True, ""

    def get_user_properties(self, user_id: str) -> List[Property]:
        """
        Retrieve all available properties for a user:
        Returns:
            List of Property objects
        """
        
        user_properties = []
        for _, prop in self.properties.items():
            if prop.user_id == user_id and prop.status == StatusEnum.AVAILABLE :
                user_properties.append(prop)

        # Sort by timestamp (most recent first)
        return sorted(user_properties, key=lambda x: x.timestamp, reverse=True)
