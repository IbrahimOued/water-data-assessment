from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import water_points, consumption


app = FastAPI()

# CORS issue prevention while calling from frontend
origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:80",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(water_points.router, prefix="/water_points", tags=["water_points"])
app.include_router(consumption.router, prefix="/consumption", tags=["consumption"])
