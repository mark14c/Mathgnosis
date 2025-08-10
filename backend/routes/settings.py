from fastapi import APIRouter

router = APIRouter()

@router.get("/settings")
def read_settings():
    return {"message": "This is the settings page"}
