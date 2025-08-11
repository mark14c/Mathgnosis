from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np

router = APIRouter(
    prefix="/vectors",
    tags=["vectors"],
)

# --- Pydantic Models ---
class VectorRequest(BaseModel):
    vectors: List[List[float]]
    operation: str
    scalar: Optional[float] = None
    matrix: Optional[List[List[float]]] = None

class GenericResponse(BaseModel):
    result: any

    class Config:
        arbitrary_types_allowed = True

# --- API Endpoint ---
@router.post("/calculate", response_model=GenericResponse)
def calculate_vector_operation(req: VectorRequest):
    if not req.vectors:
        raise HTTPException(400, "At least one vector is required.")

    try:
        np_vectors = [np.array(v) for v in req.vectors]
        op = req.operation.lower()
        result = None

        # Unary operations
        if op == "norm":
            result = np.linalg.norm(np_vectors[0])
        elif op == "orthonormalize":
            # Using QR decomposition for stable Gram-Schmidt
            q, _ = np.linalg.qr(np.array(np_vectors).T)
            result = q.T.tolist()
        
        # Scalar operations
        elif op == "scalar_multiplication":
            if req.scalar is None:
                raise HTTPException(400, "Scalar value is required.")
            result = (np_vectors[0] * req.scalar).tolist()

        # Binary operations
        elif len(np_vectors) >= 2:
            u, v = np_vectors[0], np_vectors[1]
            if op == "add":
                result = np.add(u, v).tolist()
            elif op == "subtract":
                result = np.subtract(u, v).tolist()
            elif op == "dot_product":
                result = np.dot(u, v)
            elif op == "cross_product":
                if u.shape != (3,) or v.shape != (3,):
                    raise HTTPException(400, "Cross product is only defined for 3D vectors.")
                result = np.cross(u, v).tolist()
            elif op == "projection": # Project u onto v
                result = (np.dot(u, v) / np.dot(v, v)) * v
                result = result.tolist()
            elif op == "cosine_similarity":
                result = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        
        # Transformation
        elif op == "linear_transformation":
            if not req.matrix:
                raise HTTPException(400, "Transformation matrix is required.")
            T = np.array(req.matrix)
            result = T.dot(np_vectors[0]).tolist()

        else:
            raise HTTPException(400, f"Invalid operation or insufficient vectors for '{op}'.")

        return {"result": result}

    except Exception as e:
        raise HTTPException(500, f"An error occurred: {e}")