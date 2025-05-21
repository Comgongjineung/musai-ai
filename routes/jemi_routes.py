from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from api.jemini import get_artwork_title_from_bytes  # 실제 함수가 있는 모듈 경로로 바꾸세요

router = APIRouter()

@router.post("/artwork-info")
async def artwork_info(file: UploadFile = File(...), best_guess: str = Form("")):
    try:
        image_bytes = await file.read()
        result = get_artwork_title_from_bytes(image_bytes, best_guess)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
