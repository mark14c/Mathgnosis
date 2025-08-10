from fastapi import APIRouter

router = APIRouter()

@router.get("/calculus")
def read_calculus():
    return {"message": "This is the calculus page"}
