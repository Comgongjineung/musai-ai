# main.py
from fastapi import FastAPI, UploadFile, File
from api.vision import  get_best_guess_label
app = FastAPI()

@app.post("/web-detection/")
async def web_detection(file: UploadFile = File(...)):
    image_data = await file.read()
    try:
        label = get_best_guess_label(image_data)
        if label:
            return {
                "artwork_name": label
            }
        else:
            return {"message": "작품 인식에 실패하였습니다."}
    except Exception as e:
        return {"error": str(e)}
