from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np

router = APIRouter(
    prefix="/equations",
    tags=["equations"],
)

# --- Pydantic Models ---
class PolynomialRequest(BaseModel):
    coefficients: List[float]

class SimultaneousRequest(BaseModel):
    a_matrix: List[List[float]] # Coefficient matrix
    b_vector: List[float]       # Constants vector

class GenericResponse(BaseModel):
    result: any

    class Config:
        arbitrary_types_allowed = True

# --- API Endpoints ---
@router.post("/solve_polynomial", response_model=GenericResponse)
def solve_polynomial(req: PolynomialRequest):
    """
    Solves a polynomial equation given its coefficients.
    Coefficients should be in order of decreasing power.
    e.g., for x^2 - 4x + 4 = 0, coefficients are [1, -4, 4]
    """
    if len(req.coefficients) < 2:
        raise HTTPException(400, "At least two coefficients are required (for a linear equation).")
    try:
        roots = np.roots(req.coefficients)
        # Convert complex numbers to strings for JSON compatibility
        result = [str(root) for root in roots]
        return {"result": result}
    except Exception as e:
        raise HTTPException(500, f"Could not solve polynomial: {e}")

@router.post("/solve_simultaneous", response_model=GenericResponse)
def solve_simultaneous(req: SimultaneousRequest):
    """
    Solves a system of linear equations Ax = b.
    """
    try:
        a = np.array(req.a_matrix)
        b = np.array(req.b_vector)
        solution = np.linalg.solve(a, b)
        return {"result": solution.tolist()}
    except np.linalg.LinAlgError as e:
        raise HTTPException(400, f"Matrix is singular or not square, cannot solve. {e}")
    except Exception as e:
        raise HTTPException(500, f"An error occurred: {e}")
