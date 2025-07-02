from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from api.vision import get_best_guess_label, get_original_image_url
from api.jemini import get_artwork_title_from_bytes

router = APIRouter()

@router.post("/web-detection/")
async def web_detection(
    file: UploadFile = File(...),
    level: str = Form("중"),  # ✅ level 폼 추가
    best_guess: str = Form("")  # ✅ best_guess 폼도 수동 입력 허용
):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="파일이 없습니다.")

        image_data = await file.read()

        # 사용자가 best_guess를 직접 안 넣었으면 Vision API 결과로 보충
        label = best_guess or get_best_guess_label(image_data)
        gemini_result = get_artwork_title_from_bytes(image_data, best_guess=label, level=level)
        image_url = get_original_image_url(image_data)

        return {
            "vision_result": label if label else "작품 인식 실패",
            "gemini_result": gemini_result,
            "original_image_url": image_url if image_url else "원본 이미지 없음"
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "error": "Internal Server Error",
                "message": f"AI 서버 오류: {str(e)}"
            }
        )
