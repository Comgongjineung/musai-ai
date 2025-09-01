from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from api.prompt_converter import convert_difficulty_prompt  # Gemini 호출 함수

router = APIRouter()

@router.post("/convert-difficulty")
async def convert_difficulty(
    original: str = Form(...),
    level: str = Form(...)
):
    try:
        result = convert_difficulty_prompt(original, level)
        return JSONResponse(content={"converted": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
