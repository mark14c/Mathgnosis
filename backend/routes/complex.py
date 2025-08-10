from fastapi import APIRouter

router = APIRouter()

@router.get("/complex")
def read_complex():
    return {"message": "This is the complex numbers page"}
