from fastapi import APIRouter

router = APIRouter(
    prefix="/graphs",
    tags=["graphs"],
)

@router.get("/")
def read_graphs_root():
    return {"message": "Graphing endpoints are handled by the frontend state."}
