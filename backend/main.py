from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import (
    calculator, complex, matrices, vectors, calculus, discrete_maths, 
    statistics, probability, history, settings, equations, graphs, unit_converter
)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculator.router, prefix="/api")
app.include_router(complex.router, prefix="/api")
app.include_router(matrices.router, prefix="/api")
app.include_router(vectors.router, prefix="/api")
app.include_router(calculus.router, prefix="/api")
app.include_router(discrete_maths.router, prefix="/api")
app.include_router(statistics.router, prefix="/api")
app.include_router(probability.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(settings.router, prefix="/api")
app.include_router(equations.router, prefix="/api")
app.include_router(graphs.router, prefix="/api")
app.include_router(unit_converter.router, prefix="/api")
