from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import cmath

router = APIRouter(
    prefix="/complex",
    tags=["complex"],
)

class PolarToRectangularRequest(BaseModel):
    r: float
    theta: float # in degrees

class RectangularResponse(BaseModel):
    result: str

@router.post("/polar_to_rectangular", response_model=RectangularResponse)
def polar_to_rectangular(req: PolarToRectangularRequest):
    theta_rad = cmath.pi * req.theta / 180
    z = cmath.rect(req.r, theta_rad)
    return {"result": f"{z.real:.4f} + {z.imag:.4f}j"}

class RectangularToPolarRequest(BaseModel):
    rect_str: str

class PolarResponse(BaseModel):
    result: str

@router.post("/rectangular_to_polar", response_model=PolarResponse)
def rectangular_to_polar(req: RectangularToPolarRequest):
    try:
        z = complex(req.rect_str.replace('i', 'j'))
        r, theta_rad = cmath.polar(z)
        theta_deg = theta_rad * 180 / cmath.pi
        return {"result": f"{r:.4f}, {theta_deg:.4f}°"}
    except Exception as e:
        return {"result": f"Error: {e}"}

class ArithmeticRequest(BaseModel):
    numbers: List[str]
    operation: str

class ArithmeticResponse(BaseModel):
    result: str

@router.post("/arithmetic", response_model=ArithmeticResponse)
def complex_arithmetic(req: ArithmeticRequest):
    try:
        if len(req.numbers) < 2:
            return {"result": "Error: At least two complex numbers are required."}

        numbers = [complex(s.strip().replace('i', 'j')) for s in req.numbers]
        
        result = numbers[0]
        if req.operation == "add":
            for i in range(1, len(numbers)):
                result += numbers[i]
        elif req.operation == "subtract":
            for i in range(1, len(numbers)):
                result -= numbers[i]
        elif req.operation == "multiply":
            for i in range(1, len(numbers)):
                result *= numbers[i]
        elif req.operation == "divide":
            for i in range(1, len(numbers)):
                if numbers[i] == 0:
                    return {"result": "Error: Division by zero."}
                result /= numbers[i]
        
        return {"result": f"{result.real:.4f} + {result.imag:.4f}j"}

    except Exception as e:
        return {"result": f"Error: {e}"}

@router.get("/")
def read_complex():
    return {"message": "This is the complex numbers page"}
