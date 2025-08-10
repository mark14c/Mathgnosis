from fastapi import APIRouter

router = APIRouter()

@router.get("/vectors")
def read_vectors():
    return {"message": "This is the vectors page"}
