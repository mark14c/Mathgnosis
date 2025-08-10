from fastapi import APIRouter

router = APIRouter()

@router.get("/history")
def read_history():
    return {"message": "This is the history page"}
