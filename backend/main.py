from fastapi import FastAPI
from backend.routes import calculator, complex, matrices, vectors, calculus, discrete_maths, statistics, probability, history, settings

app = FastAPI()

app.include_router(calculator.router)
app.include_router(complex.router)
app.include_router(matrices.router)
app.include_router(vectors.router)
app.include_router(calculus.router)
app.include_router(discrete_maths.router)
app.include_router(statistics.router)
app.include_router(probability.router)
app.include_router(history.router)
app.include_router(settings.router)
