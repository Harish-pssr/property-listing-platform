from fastapi import APIRouter, HTTPException
from services.intializer import property_manager
from models.schemas import PropertyCreate, PropertyDetail, StatusEnum

router = APIRouter()

@router.post("/properties", response_model=PropertyDetail)
async def create_property(
    property_data: PropertyCreate,
    user_id: str
):
    """
    Creates a new property listing.
    Args:
        property_data (PropertyCreate): The details of the property to be created.
        user_id (str): The ID of the user creating the property.
    Returns:
        PropertyDetail: The details of the created property.
    """

    try:
        created_property = property_manager.add_property(
            user_id=user_id,
            property_details=property_data.model_dump()
        )
        return created_property
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/properties/{property_id}")
async def update_property_status(
    property_id: str,
    status: StatusEnum,
    user_id: str 
):
    """
    Updates the status of a property.
    Args:
        property_id (str): The ID of the property to update.
        status (StatusEnum): The new status for the property (e.g., 'Available', 'Sold').
        user_id (str): The ID of the user making the request.
    Returns:
        dict: A message indicating the success or failure of the operation.
    """
    success, message = property_manager.update_property_status(property_id, status, user_id)
    if not success:
        raise HTTPException(
            status_code=403,
            detail=message
        )
    return {"message": f"Property {property_id} status updated to {status}"}
