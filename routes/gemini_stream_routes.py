from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from api.gemini_stream import generate_artwork_stream

router = APIRouter()

@router.post("/artwork-info")
async def artwork_info(file: UploadFile = File(...), best_guess: str = Form(""), level: str = Form("중")):
    image_bytes = await file.read()
    # StreamingResponse로 스트리밍 반환
    return StreamingResponse(generate_artwork_stream(image_bytes, best_guess, level), media_type="text/plain")
