from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any
import numpy as np
import sympy as sp

router = APIRouter(
    prefix="/matrices",
    tags=["matrices"],
)

class MatrixRequest(BaseModel):
    matrices: List[List[List[float]]]
    operation: str
    scalar: float = 1.0

class MatrixResponse(BaseModel):
    result: Any

def to_sympy_matrix(matrix_list):
    return sp.Matrix(matrix_list)

def to_numpy_array(matrix_list):
    return np.array(matrix_list)

@router.post("/calculate", response_model=MatrixResponse)
def calculate_matrix_operation(req: MatrixRequest):
    if not req.matrices:
        raise HTTPException(400, "At least one matrix is required.")

    try:
        # Convert to numpy for numerical ops, sympy for symbolic ops
        np_matrices = [to_numpy_array(m) for m in req.matrices]
        sp_matrices = [to_sympy_matrix(m) for m in req.matrices]
        op = req.operation.lower()
        result = None

        # Operations requiring one matrix
        if op in ["transpose", "adjoint", "inverse", "determinant", "rref", "null_space", "range_space", "eigen", "norm", "exponentiation"]:
            A_np = np_matrices[0]
            A_sp = sp_matrices[0]
            
            if op == "transpose":
                result = A_np.T.tolist()
            elif op == "determinant":
                result = np.linalg.det(A_np)
            elif op == "inverse":
                result = np.linalg.inv(A_np).tolist()
            elif op == "adjoint":
                result = sp.det(A_sp) * A_sp.inv().tolist()
            elif op == "rref":
                result = A_sp.rref()[0].tolist()
            elif op == "null_space":
                result = [list(vec) for vec in A_sp.nullspace()]
            elif op == "range_space":
                result = [list(vec) for vec in A_sp.columnspace()]
            elif op == "eigen":
                eigenvalues, eigenvectors = np.linalg.eig(A_np)
                result = {
                    "eigenvalues": eigenvalues.tolist(),
                    "eigenvectors": eigenvectors.tolist()
                }
            elif op == "norm":
                result = np.linalg.norm(A_np)
            elif op == "exponentiation":
                # Matrix exponentiation (e^A)
                from scipy.linalg import expm
                result = expm(A_np).tolist()

        # Operations requiring two or more matrices
        elif op in ["add", "subtract", "multiply"]:
            res_matrix = np_matrices[0]
            for m in np_matrices[1:]:
                if op == "add":
                    res_matrix = np.add(res_matrix, m)
                elif op == "subtract":
                    res_matrix = np.subtract(res_matrix, m)
                elif op == "multiply":
                    res_matrix = np.dot(res_matrix, m)
            result = res_matrix.tolist()

        # Scalar operations
        elif op == "scalar_multiply":
            result = (np_matrices[0] * req.scalar).tolist()
        
        # Element-wise operations
        elif op == "dot_product":
            if len(np_matrices) < 2:
                raise HTTPException(400, "Dot product requires at least two matrices.")
            result = np.multiply(np_matrices[0], np_matrices[1]).tolist()

        else:
            raise HTTPException(400, f"Unknown operation: {op}")

        return {"result": result}

    except Exception as e:
        raise HTTPException(500, f"An error occurred: {e}")