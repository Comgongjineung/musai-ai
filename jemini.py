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

        prompt = (
            f"이 작품은 '{best_guess}'라는 이름으로 Vision API에서 추정된 이미지입니다.\n"
            f"이 작품의 정식 정보를 아래 형식에 맞춰 한국어로 알려주세요.\n"
            f"특히 '작품 해설'은 반드시 **최소 10문장 이상**, 구체적이고 서술적인 문단으로 작성해주세요.\n\n"
            f"작품 이름 :\n"
            f"작가명 :\n"
            f"제작 년도 :\n"
            f"예술사조 :\n"
            f"작품 해설 :"
        )

        response = model.generate_content([prompt, image], stream=False)
        result = response.text.strip()

        parsed = {
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
