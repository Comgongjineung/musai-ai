from fastapi import FastAPI, UploadFile, File
from api.vision import get_best_guess_label
from jemini import get_artwork_title_from_bytes
from fastapi import HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/web-detection/")
async def web_detection(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="파일이 없습니다.")

        image_data = await file.read()

        label = get_best_guess_label(image_data)
        gemini_result = get_artwork_title_from_bytes(image_data, best_guess=label)

        return {
            "vision_result": label if label else "작품 인식 실패",
            "gemini_result": gemini_result
        }


    except HTTPException as http_exc:
        # FastAPI가 자동으로 상태코드와 함께 응답함
        raise http_exc

    except Exception as e:
        # 알 수 없는 서버 오류
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "error": "Internal Server Error",
                "message": f"AI 서버 오류: {str(e)}"
            }
        )