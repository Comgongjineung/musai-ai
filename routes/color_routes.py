from fastapi import APIRouter, UploadFile, File, HTTPException
from api.color import extract_color_info

router = APIRouter()

@router.post("/recommend-color")
async def recommend_color(image: UploadFile = File(...)):
    try:
        result = extract_color_info(image)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
