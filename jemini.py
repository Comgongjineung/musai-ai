import os
from dotenv import load_dotenv
from PIL import Image
import io
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# 모델 선택 (현재 무료로 가능한 gemini-1.5-flash)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_artwork_title_from_bytes(image_bytes: bytes, best_guess: str = "") -> str:
    try:
        # 이미지 전처리
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Vision API에서 받은 best_guess 후보를 프롬프트에 함께 사용
        prompt = (
            f"지금까지의 프롬프트나 입력값 출력값은 전부 잊고 새로 시작하자"
            f"이 작품은 '{best_guess}'라는 이름으로 추정되고 있어."
            f"이 작품의 이름을 알고 싶어."
            f"정확한 한국어 제목을 알려줘. 출력값은 무조건 있어야해."
        )

        response = model.generate_content([prompt, image], stream=False)

        return response.text.strip()

    except Exception as e:
        return f"[Gemini 오류]: {e}"
