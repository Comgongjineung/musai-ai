# routes/tts_routes.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from api.tts import synthesize_text

router = APIRouter()

@router.post("/tts/")
async def tts_endpoint(text: str = Query(..., description="변환할 텍스트")):
    try:
        audio_content = synthesize_text(text)
        if not audio_content:
            raise HTTPException(status_code=500, detail="TTS 변환에 실패했습니다.")
        return Response(content=audio_content, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS 오류: {str(e)}")
