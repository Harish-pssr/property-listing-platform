from fastapi import APIRouter, HTTPException
from typing import List
from services.intializer import property_manager, property_search
from models.schemas import PropertyDetail

router = APIRouter()

@router.get("/user/properties", response_model=List[PropertyDetail])
async def get_user_properties(user_id: str):
    """
    Retrieves all available properties owned by a specific user.
    Args:
        user_id (str): The ID of the user whose properties are to be retrieved.
    Returns:
        List[PropertyDetail]: A list of properties owned by the user, sorted by creation date in descending order.
    """
    try:
        user_properties = property_manager.get_user_properties(user_id)
        return user_properties
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/shortlist", response_model=List[PropertyDetail])
async def get_shortlisted_properties(user_id: str):
    """
    Retrieves all properties shortlisted by a specific user.
    Args:
        user_id (str): The ID of the user whose shortlisted properties are to be retrieved.
    Returns:
        List[PropertyDetail]: A list of properties owned by the user, sorted by creation date in descending order.
    """
    try:
        shortlisted_properties = property_search.get_shortlisted(
            user_id=user_id,
            user_shortlists=property_manager.user_shortlists
        )
        return shortlisted_properties
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/user/shortlist/{property_id}")
async def shortlist_property(
    property_id: str,
    user_id: str
):
    """
    Adds a property to the user's shortlist.
    Args:
        property_id (str): The ID of the property to be added to the user's shortlist.
        user_id (str): The ID of the user adding the property to their shortlist.
    Returns:
        dict: A success message confirming the property was added to the shortlist.
    """
    try:
        success, message = property_search.shortlist_property(
            user_id=user_id,
            property_id=property_id,
            user_shortlists=property_manager.user_shortlists
        )
        if not success:
            raise HTTPException(
                status_code=400,
                detail=message
            )
        return {"message": f"Property {property_id} has been successfully added to your shortlist."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/user/shortlist/{property_id}")
async def remove_from_shortlist(
    property_id: str,
    user_id: str
):
    """
    Removes a property from the user's shortlist.
    Args:
        property_id (str): The ID of the property to be removed from the user's shortlist.
        user_id (str): The ID of the user removing the property to their shortlist.
    Returns:
        dict: A success message confirming the property was rmeoved from the shortlist.
    """
    try:
        success, message = property_search.remove_shortlist_property(
            user_id=user_id,
            property_id=property_id,
            user_shortlists=property_manager.user_shortlists
        )
        if not success:
            raise HTTPException(
                status_code=400,
                detail=message
            )
        return {"message": f"Property {property_id} has been successfully removed from your shortlist."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))