from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import sympy

router = APIRouter(
    prefix="/calculus",
    tags=["calculus"],
)

# --- Pydantic Models ---
class DifferentiationRequest(BaseModel):
    function_str: str
    variables: List[str]

class GradientRequest(BaseModel):
    function_str: str

class CalculusResponse(BaseModel):
    result: str | Dict[str, str]

# --- Helper Functions ---
def parse_function(function_str: str):
    """Parses the function string and extracts symbols."""
    try:
        # Replace common math functions for sympy compatibility
        safe_function_str = function_str.replace('^', '**')
        # Define allowed functions for eval
        allowed_funcs = {
            'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
            'asin': sympy.asin, 'acos': sympy.acos, 'atan': sympy.atan,
            'exp': sympy.exp, 'log': sympy.log, 'sqrt': sympy.sqrt
        }
        
        # Extract symbols from the function string to define them
        symbols = sympy.symbols(' '.join(sorted(list(set(c for c in safe_function_str if c.isalpha() and c not in allowed_funcs)))))
        
        # Create a local dict for eval
        eval_dict = {**allowed_funcs, **{str(s): s for s in symbols}}

        expr = sympy.sympify(safe_function_str, locals=eval_dict)
        return expr, symbols
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Function parsing error: {e}")

# --- API Endpoints ---
@router.post("/differentiate", response_model=CalculusResponse)
def differentiate(req: DifferentiationRequest):
    """
    Calculates the partial derivative of a function with respect to given variables.
    """
    try:
        expr, _ = parse_function(req.function_str)
        
        if not req.variables:
            raise HTTPException(status_code=400, detail="Please specify variable(s) for differentiation.")

        results = {}
        for var_str in req.variables:
            var_symbol = sympy.Symbol(var_str)
            derivative = sympy.diff(expr, var_symbol)
            results[f"d/d{var_str}"] = str(derivative)
        
        if len(results) == 1:
             return {"result": list(results.values())[0]}
        return {"result": results}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/gradient", response_model=CalculusResponse)
def gradient(req: GradientRequest):
    """
    Calculates the gradient of a function.
    """
    try:
        expr, symbols = parse_function(req.function_str)
        
        if not symbols:
             # Handle case of constant function e.g. "2"
            return {"result": "0"}

        grad_vector = sympy.Matrix([sympy.diff(expr, s) for s in symbols])
        
        # Format the result as a string vector
        result_str = " + ".join([f"({grad_vector[i]})*{symbols[i]}" for i in range(len(symbols))])
        
        return {"result": str(grad_vector.T)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Placeholder endpoints for other sections
@router.post("/limits")
def limits():
    return {"result": "Limits endpoint is not yet implemented."}

@router.post("/integrate/definite")
def definite_integration():
    return {"result": "Definite Integration endpoint is not yet implemented."}

@router.post("/integrate/indefinite")
def indefinite_integration():
    return {"result": "Indefinite Integration endpoint is not yet implemented."}