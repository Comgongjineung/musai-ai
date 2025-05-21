from fastapi import FastAPI
from routes.vision_routes import router as vision_router
from routes.jemi_routes import router as jemi_router

app = FastAPI()

app.include_router(vision_router, prefix="/web-detection")
app.include_router(jemi_router, prefix="/jemi")