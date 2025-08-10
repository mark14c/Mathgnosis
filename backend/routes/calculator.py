from fastapi import APIRouter

router = APIRouter()

@router.get("/calculator")
def read_calculator():
    return {"message": "This is the calculator page"}
