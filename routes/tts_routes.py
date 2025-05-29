from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import io
from api.tts import synthesize_text
from mutagen.mp3 import MP3

router = APIRouter()

@router.get("/")
@router.post("/")
async def tts_endpoint(text: str = Query(..., description="변환할 텍스트")):
    try:
        audio_content = synthesize_text(text)
        if not audio_content:
            raise HTTPException(status_code=500, detail="TTS 변환에 실패했습니다.")

        # 스트림 응답으로 변경
        return StreamingResponse(
            io.BytesIO(audio_content),
            media_type="audio/mpeg",
            headers={
                "Cache-Control": "no-store, no-cache, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS 오류: {str(e)}")