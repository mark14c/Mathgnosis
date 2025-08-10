from fastapi import APIRouter

router = APIRouter()

@router.get("/statistics")
def read_statistics():
    return {"message": "This is the statistics page"}
