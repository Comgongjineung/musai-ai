from fastapi import FastAPI
from routes.vision_routes import router as vision_router
from routes.gpt_routes    import router as gpt_router
from routes.jemi_routes import router as jemi_router
from routes.tts_routes import router as tts_router

app = FastAPI()

app.include_router(vision_router, prefix="/web-detection")
app.include_router(jemi_router, prefix="/jemi")
app.include_router(gpt_router,    prefix="/gpt")      
# app.include_router(jemi_router, prefix="/jemi")
app.include_router(tts_router, prefix="/tts")