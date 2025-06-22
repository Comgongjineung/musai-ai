# routes/gpt_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from api.vision import get_best_guess_label
from api.gpt import get_artwork_title_from_bytes

router = APIRouter(prefix="/gpt")

@router.post("/")
async def detect_and_describe(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="파일이 없습니다.")

        image_bytes = await file.read()
        label = get_best_guess_label(image_bytes)
        gpt_result = get_artwork_title_from_bytes(image_bytes, best_guess=label)

        return {
            "vision_result": label or "작품 인식 실패",
            "gpt_result": gpt_result
        }

    except HTTPException as exc:
        raise exc

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "error": "Internal Server Error",
                "message": f"AI 서버 오류: {e}"
            }
        )
