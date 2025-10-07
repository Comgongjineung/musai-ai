from fastapi import APIRouter, UploadFile, File, HTTPException
from api.gemini_extract_ar_points import extract_points

router = APIRouter(tags=["AR Points (Gemini)"])

@router.post("/points-gemini")
async def ar_points(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(415, "jpg/png만 허용")
    return extract_points(await file.read())