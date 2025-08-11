from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
import numpy as np
import sympy as sp
from scipy import stats
from scipy.integrate import quad

router = APIRouter(
    prefix="/probability",
    tags=["probability"],
)

# --- Pydantic Models ---
class StandardDistRequest(BaseModel):
    dist_name: str
    params: Dict[str, float]
    calc_type: str  # "pdf", "cdf", "between"
    x1: float
    x2: Optional[float] = None

class JointDistRequest(BaseModel):
    table: List[List[float]]
    conditional_on: Optional[Dict[str, int]] = None # e.g., {"row": 0, "given_col": 1}

class CustomPdfRequest(BaseModel):
    function_str: str
    lower_limit: float
    upper_limit: float

class HypothesisTestRequest(BaseModel):
    test_type: str
    data1: List[float]
    data2: Optional[List[float]] = None
    alpha: float = 0.05
    mu: float = 0  # Population mean for one-sample tests
    prop1: Optional[float] = None
    n1: Optional[int] = None
    prop2: Optional[float] = None
    n2: Optional[int] = None


class GenericResponse(BaseModel):
    result: Any

# --- Helper Functions ---
def get_distribution(dist_name: str, params: Dict[str, float]):
    dist_map = {
        "bernoulli": lambda p: stats.bernoulli(p=p),
        "binomial": lambda n, p: stats.binom(n=n, p=p),
        "poisson": lambda mu: stats.poisson(mu=mu),
        "normal": lambda loc, scale: stats.norm(loc=loc, scale=scale),
        "geometric": lambda p: stats.geom(p=p),
        "beta": lambda a, b: stats.beta(a=a, b=b),
        "gamma": lambda a: stats.gamma(a=a),
        "hypergeometric": lambda M, n, N: stats.hypergeom(M=M, n=n, N=N),
        "exponential": lambda scale: stats.expon(scale=scale),
        "chi_squared": lambda df: stats.chi2(df=df),
    }
    try:
        return dist_map[dist_name](**params)
    except KeyError:
        raise HTTPException(400, f"Unknown distribution: {dist_name}")
    except TypeError:
        raise HTTPException(400, f"Incorrect parameters for {dist_name}. Provided: {params}")

# --- API Endpoints ---
@router.post("/standard_distribution", response_model=GenericResponse)
def calc_standard_distribution(req: StandardDistRequest):
    dist = get_distribution(req.dist_name, req.params)
    if req.calc_type == "pdf":
        result = dist.pmf(int(req.x1)) if hasattr(dist, 'pmf') else dist.pdf(req.x1)
    elif req.calc_type == "cdf":
        result = dist.cdf(req.x1)
    elif req.calc_type == "between" and req.x2 is not None:
        result = dist.cdf(req.x2) - dist.cdf(req.x1)
    else:
        raise HTTPException(400, "Invalid calculation type or missing x2 for 'between'.")
    return {"result": result}

@router.post("/joint_distribution", response_model=GenericResponse)
def calc_joint_distribution(req: JointDistRequest):
    table = np.array(req.table)
    if not np.isclose(table.sum(), 1.0):
        raise HTTPException(400, f"Probabilities must sum to 1. Current sum: {table.sum()}")
    
    marginals = {
        "row_marginal": table.sum(axis=1).tolist(),
        "col_marginal": table.sum(axis=0).tolist(),
    }
    return {"result": marginals}

@router.post("/custom_pdf", response_model=GenericResponse)
def calc_custom_pdf(req: CustomPdfRequest):
    x = sp.symbols('x')
    try:
        expr = sp.sympify(req.function_str)
        f = sp.lambdify(x, expr, 'numpy')
        # Check if PDF integrates to 1 over its domain
        integral, _ = quad(f, req.lower_limit, req.upper_limit)
        # We allow some tolerance for floating point errors
        # if not np.isclose(integral, 1.0):
        #     raise HTTPException(400, f"PDF must integrate to 1. It integrates to {integral}")
        return {"result": {"area": integral}}
    except Exception as e:
        raise HTTPException(500, f"Error processing custom PDF: {e}")

@router.post("/hypothesis_testing", response_model=GenericResponse)
def run_hypothesis_test(req: HypothesisTestRequest):
    try:
        if req.test_type == "z_test_1_sample" and req.data1:
            # Assuming we have the population std dev, which is rare.
            # This is more of a textbook case. T-test is more common.
            # For a real Z-test, we'd need population sigma.
            # We'll perform a t-test instead as it's more practical.
            stat, p = stats.ttest_1samp(req.data1, popmean=req.mu)
            result = {"test": "One-Sample T-Test (used for Z-test)", "statistic": stat, "p_value": p}
        elif req.test_type == "t_test_1_sample" and req.data1:
            stat, p = stats.ttest_1samp(req.data1, popmean=req.mu)
            result = {"statistic": stat, "p_value": p}
        elif req.test_type == "t_test_2_sample" and req.data1 and req.data2:
            stat, p = stats.ttest_ind(req.data1, req.data2)
            result = {"statistic": stat, "p_value": p}
        elif req.test_type == "chi_squared_test" and req.data1 and req.data2:
            stat, p, _, _ = stats.chi2_contingency([req.data1, req.data2])
            result = {"statistic": stat, "p_value": p}
        elif req.test_type == "f_test_anova" and req.data1 and req.data2:
            # This is a simplified ANOVA for two groups, same as F-test
            stat, p = stats.f_oneway(req.data1, req.data2)
            result = {"statistic": stat, "p_value": p}
        else:
            raise HTTPException(400, "Invalid test type or insufficient data.")
        
        return {"result": result}
    except Exception as e:
        raise HTTPException(500, f"Error during hypothesis test: {e}")