from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from api.jemini import get_artwork_title_from_bytes
from api.vision import get_image_analysis

router = APIRouter()

@router.post("/")
async def web_detection(
    file: UploadFile = File(...),
    level: str = Form("중"),
    best_guess: str = Form("")
):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="파일이 없습니다.")

        image_data = await file.read()

        # Vision API 1회 호출
        image_url, api_best_guess, title_candidate = get_image_analysis(image_data)

        # label 결정: 사용자 입력 > Vision API title 후보 > Vision API best_guess
        label = best_guess or title_candidate or api_best_guess

        # Gemini로 작품 해설 생성
        gemini_result = get_artwork_title_from_bytes(image_data, best_guess=label, level=level)

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