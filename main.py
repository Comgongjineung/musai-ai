from fastapi import FastAPI
from routes.vision_routes import router as vision_router
#from routes.gpt_routes    import router as gpt_router
from routes.jemi_routes import router as gemi_router
from routes.tts_routes import router as tts_router
from routes.ar_routes     import router as ar_router
from routes.difficulty_routes import router as difficulty_routes
from routes.color_routes import router as color_router
from routes.gemini_stream_routes import router as gemini_stream_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중엔 "*" 가능, 배포 시 Spring 주소만
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(vision_router, prefix="/web-detection")
app.include_router(gemi_router, prefix="/jemi")
#app.include_router(gpt_router,    prefix="/gpt")      
# app.include_router(jemi_router, prefix="/jemi")
app.include_router(tts_router, prefix="/tts")
app.include_router(ar_router, prefix="/ar")
app.include_router(difficulty_routes, prefix="/difficulty")
app.include_router(color_router, prefix="/color")
app.include_router(gemini_stream_router, prefix="/jemini-stream")

