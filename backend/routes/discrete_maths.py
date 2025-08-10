from fastapi import APIRouter

router = APIRouter()

@router.get("/discrete_maths")
def read_discrete_maths():
    return {"message": "This is the discrete maths page"}
