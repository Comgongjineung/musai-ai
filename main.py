from fastapi import FastAPI, UploadFile, File
from api.vision import get_best_guess_label
from jemini import get_artwork_title_from_bytes

app = FastAPI()

@app.post("/web-detection/")
async def web_detection(file: UploadFile = File(...)):
    image_data = await file.read()

    try:
        # Vision API로 best guess 추출
        label = get_best_guess_label(image_data)

        # Gemini에 best guess를 프롬프트 힌트로 함께 전달
        gemini_label = get_artwork_title_from_bytes(image_data, best_guess=label)

        return {
            "vision_result": label if label else "작품 인식 실패",
            "gemini_result": gemini_label
        }

    except Exception as e:
        return {"error": str(e)}
