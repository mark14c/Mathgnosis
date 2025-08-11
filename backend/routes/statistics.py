from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)

# --- Pydantic Models ---
class DescriptiveStatsRequest(BaseModel):
    data1: List[float]
    data2: Optional[List[float]] = None

class RegressionRequest(BaseModel):
    x_data: List[List[float]]
    y_data: List[float]
    model_type: str
    params: Optional[Dict[str, float]] = {}

class GenericResponse(BaseModel):
    result: Any

# --- Helper Functions ---
def concordant_discordant_pairs(data1, data2):
    if len(data1) != len(data2):
        return {"error": "Datasets must have the same length."}
    concordant = 0
    discordant = 0
    ties = 0
    for i in range(len(data1)):
        for j in range(i + 1, len(data1)):
            x_tie = data1[i] == data1[j]
            y_tie = data2[i] == data2[j]
            if x_tie or y_tie:
                ties += 1
                continue
            if (data1[i] < data1[j] and data2[i] < data2[j]) or \
               (data1[i] > data1[j] and data2[i] > data2[j]):
                concordant += 1
            else:
                discordant += 1
    return {"concordant": concordant, "discordant": discordant, "ties": ties}

# --- API Endpoints ---
@router.post("/descriptive", response_model=GenericResponse)
def get_descriptive_stats(req: DescriptiveStatsRequest):
    data = np.array(req.data1)
    results = {
        "count": len(data),
        "sum": np.sum(data),
        "mean": np.mean(data),
        "median": np.median(data),
        "mode": stats.mode(data)[0].tolist(),
        "population_variance": np.var(data),
        "population_std": np.std(data),
        "sample_variance": np.var(data, ddof=1),
        "sample_std": np.std(data, ddof=1),
    }
    if req.data2:
        results["concordance"] = concordant_discordant_pairs(req.data1, req.data2)
    
    return {"result": results}

@router.post("/regression", response_model=GenericResponse)
def perform_regression(req: RegressionRequest):
    X = np.array(req.x_data)
    y = np.array(req.y_data)

    if X.ndim == 1:
        X = X.reshape(-1, 1)
    if y.ndim != 1:
        raise HTTPException(400, "Y data must be a 1D list.")
    if X.shape[0] != len(y):
        raise HTTPException(400, "Number of samples in X and Y must match.")

    model_type = req.model_type.lower()
    params = req.params or {}
    
    try:
        if model_type in ["linear", "multiple_linear"]:
            model = LinearRegression()
        elif model_type == "polynomial":
            degree = int(params.get("degree", 2))
            model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        elif model_type == "logistic":
            model = LogisticRegression()
        elif model_type == "lasso":
            alpha = params.get("alpha", 1.0)
            model = Lasso(alpha=alpha)
        elif model_type == "ridge":
            alpha = params.get("alpha", 1.0)
            model = Ridge(alpha=alpha)
        else:
            raise HTTPException(400, f"Unknown model type: {model_type}")

        model.fit(X, y)
        
        # Extract results
        results = {"score": model.score(X, y)}
        if model_type == "polynomial":
            # For pipeline, get final estimator's attributes
            final_model = model.steps[-1][1]
            results["coefficients"] = final_model.coef_.tolist()
            results["intercept"] = final_model.intercept_
        else:
            results["coefficients"] = model.coef_.tolist()
            results["intercept"] = model.intercept_

        return {"result": results}
    except Exception as e:
        raise HTTPException(500, f"Error during regression analysis: {e}")