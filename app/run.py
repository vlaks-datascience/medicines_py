from fastapi import FastAPI
from app.routes.medicine import medicine_router

app = FastAPI()
app.include_router(medicine_router)
