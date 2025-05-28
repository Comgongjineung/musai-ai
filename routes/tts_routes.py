from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
import io
from api.tts import synthesize_text

router = APIRouter()

@router.get("/tts/")
@router.post("/tts/")
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