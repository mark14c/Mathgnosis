from fastapi import APIRouter

router = APIRouter()

@router.get("/probability")
def read_probability():
    return {"message": "This is the probability page"}
