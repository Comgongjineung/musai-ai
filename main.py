from fastapi import FastAPI
from routes.vision_routes import router as vision_router
from routes.gpt_routes    import router as gpt_router
from routes.jemi_routes import router as jemi_router
from routes.tts_routes import router as tts_router
from routes.ar_routes     import router as ar_router
from routes.difficulty_routes import router as difficulty_routes
from routes.color_routes import router as color_router

app = FastAPI()

app.include_router(vision_router, prefix="/web-detection")
app.include_router(jemi_router, prefix="/jemi")
app.include_router(gpt_router,    prefix="/gpt")      
# app.include_router(jemi_router, prefix="/jemi")
app.include_router(tts_router, prefix="/tts")
app.include_router(ar_router, prefix="/ar")
app.include_router(difficulty_routes, prefix="/difficulty")
app.include_router(color_router, prefix="/color")

