from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    AVAILABLE = "Available"
    SOLD = "Sold"

class SortKeyEnum(str, Enum):  # for sorting search results
    PRICE = "price"
    TIMESTAMP = "timestamp"

class PropertyCreate(BaseModel):
    location: str
    price: float = Field(..., gt=0, description="Price must be a positive number")
    property_type: str
    description: str
    amenities: List[str]

class PropertyDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    property_id: str
    user_id: str
    location: str
    price: float
    property_type: str
    status: StatusEnum  # Restrict to enum values
    timestamp: datetime
    description: str
    amenities: List[str]
