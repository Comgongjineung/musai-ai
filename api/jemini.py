import base64
import os
from dotenv import load_dotenv
from PIL import Image
import io
import re
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_artwork_title_from_bytes(image_bytes: bytes, best_guess: str = "") -> dict:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # 원본 크기
        original_width, original_height = image.size

        # 목표 가로 길이
        target_width = 342
        # 비율 유지하며 세로 길이 계산
        target_height = int((target_width / original_width) * original_height)

        # Pillow 10 이상이면 이렇게 리샘플링 모드 선택
        try:
            resample_mode = Image.Resampling.LANCZOS
        except AttributeError:
            resample_mode = Image.ANTIALIAS

        # 이미지 크기 조절 (비율 유지)
        image = image.resize((target_width, target_height), resample_mode)

        # ✅ 이미지 JPG로 변환해서 base64 인코딩
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        image_url = "data:image/jpeg;base64," + image_base64

        prompt = (
            f"당신은 AI 기반 도슨트 앱입니다. \n"
            f"이 작품은 '{best_guess}'라는 이름으로 Vision API에서 추정된 이미지입니다.\n"
            f"이 작품의 정식 정보를 아래 형식에 맞춰 한국어로 알려주세요.\n"
            f"특히 '작품 해설'은 반드시 **최소 10문장 이상**, 구체적이고 서술적인 문단으로 작성해주세요.\n\n"
            f"작품 이미지는 342 x 514 이 픽셀에 맞춰서 보내주세요 \n"
            f"작품 이미지: \n"
            f"작품 이름 :\n"
            f"작가명 :\n"
            f"제작 년도 :\n"
            f"예술사조 :\n"
            f"작품 해설 :"
        )

        response = model.generate_content([prompt, image], stream=False)
        result = response.text.strip()

        parsed = {
            "image_url": image_url,
            "title": _extract_field(result, r"작품\s*이름\s*:\s*(.*)"),
            "artist": _extract_field(result, r"작가명\s*:\s*(.*)"),
            "year": _extract_field(result, r"제작\s*년도\s*:\s*(.*)"),
            "style": _extract_field(result, r"예술사조\s*:\s*(.*)"),
            "description": _extract_description(result)
        }

        return parsed

    except Exception as e:
        return {"error": f"[Gemini 오류]: {e}"}


def _extract_field(text: str, pattern: str) -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else "정보 없음"


def _extract_description(text: str) -> str:
    match = re.search(r"작품\s*해설\s*:\s*(.*)", text, re.DOTALL)
    return match.group(1).strip() if match else "설명 없음"
