from fastapi import APIRouter

router = APIRouter()

@router.get("/matrices")
def read_matrices():
    return {"message": "This is the matrices page"}
