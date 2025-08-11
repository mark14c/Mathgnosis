import math
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Expression(BaseModel):
    expression: str

def nCr(n, r):
    if r < 0 or r > n:
        return 0
    f = math.factorial
    return f(n) // f(r) // f(n-r)

def nPr(n, r):
    if r < 0 or r > n:
        return 0
    f = math.factorial
    return f(n) // f(n-r)

@router.post("/api/calculator/eval")
def eval_expression(expression: Expression):
    try:
        # Add math functions and constants to the eval context
        allowed_names = {
            "acos": math.acos,
            "asin": math.asin,
            "atan": math.atan,
            "atan2": math.atan2,
            "ceil": math.ceil,
            "cos": math.cos,
            "cosh": math.cosh,
            "degrees": math.degrees,
            "e": math.e,
            "exp": math.exp,
            "fabs": math.fabs,
            "floor": math.floor,
            "fmod": math.fmod,
            "frexp": math.frexp,
            "hypot": math.hypot,
            "ldexp": math.ldexp,
            "log": math.log,
            "log10": math.log10,
            "modf": math.modf,
            "pi": math.pi,
            "pow": math.pow,
            "radians": math.radians,
            "sin": math.sin,
            "sinh": math.sinh,
            "sqrt": math.sqrt,
            "tan": math.tan,
            "tanh": math.tanh,
            "nCr": nCr,
            "nPr": nPr,
        }
        
        result = eval(expression.expression, {"__builtins__": None}, allowed_names)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))