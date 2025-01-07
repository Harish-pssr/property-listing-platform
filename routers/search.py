from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.schemas import PropertyDetail, StatusEnum, SortKeyEnum
from services.intializer import property_search

router = APIRouter()

@router.get("/properties/search", response_model=List[PropertyDetail])
async def search_properties(
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    location: Optional[str] = Query(None, description="Location filter"),
    property_type: Optional[str] = Query(None, description="Type of property (e.g., Apartment, Villa)"),
    sort_key: Optional[SortKeyEnum] = Query("price", description="Field to sort by (price or timestamp)"),
    descending: Optional[bool] = Query(False, description="Sort in descending order"),
    page: Optional[int] = Query(1, description="Page number for pagination"),
    limit: Optional[int] = Query(10, description="Number of items per page")
):
    """
    Searches for properties based on various filters and sorting criteria.
    Args:
        min_price (Optional[float]): The minimum price filter for the search. Defaults to None.
        max_price (Optional[float]): The maximum price filter for the search. Defaults to None.
        location (Optional[str]): Filter properties by location. Defaults to None.
        property_type (Optional[str]): Filter properties by type (e.g., Apartment, Villa). Defaults to None.
        sort_key (Optional[SortKeyEnum]): The field to sort results by price or timestamp. Defaults to 'price'.
        descending (Optional[bool]): Whether to sort results in descending order. Defaults to False.
        page (Optional[int]): The page number for paginated results. Defaults to 1.
        limit (Optional[int]): The number of items per page. Defaults to 10.
    Returns:
        List[PropertyDetail]: A list of properties matching the specified filters and criteria.
    """
    try:
        criteria = {
            "min_price": min_price,
            "max_price": max_price,
            "location": location,
            "property_type": property_type,
            "status": StatusEnum.AVAILABLE,
            "sort_key": sort_key,
            "descending": descending,
            "page": page,
            "limit": limit,
        }
        result = property_search.search_properties(criteria)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
