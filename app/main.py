from fastapi import FastAPI
from app.api.density import router as density_router

app = FastAPI(title="Toronto Public Resource Density API")

app.include_router(density_router)
