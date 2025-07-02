import base64
import os
from dotenv import load_dotenv
from PIL import Image
import io
import re

import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Literal

# ──────────────── 환경설정 ────────────────
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()


# ──────────────── 핵심 로직 함수 ────────────────
def get_artwork_title_from_bytes(
    image_bytes: bytes,
    best_guess: str = "",
    level: str = "중"
) -> dict:
    try:
        # 이미지 처리
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        original_width, original_height = image.size
        target_width = 342
        target_height = int((target_width / original_width) * original_height)

        try:
            resample_mode = Image.Resampling.LANCZOS
        except AttributeError:
            resample_mode = Image.ANTIALIAS

        image = image.resize((target_width, target_height), resample_mode)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        image_url = "data:image/jpeg;base64," + image_base64

        # ✅ 난이도별 프롬프트 문구 차별화
        if level == "하":
            level_prompt = (
                "7살도 이해할 수 있도록, 아주 쉬운 단어와 짧은 문장을 사용해주세요.\n"
                "전문 용어나 외래어는 풀어서 설명하고, 핵심 내용만 간단하게 요약해주세요.\n"
                "어려운 단어나 역사적 맥락은 설명하지 마세요.\n"
            )
        elif level == "상":
            level_prompt = (
                "예술사적 맥락, 작가의 철학, 시대적 배경, 작품 기법을 포함한 깊이 있는 설명을 해주세요.\n"
                "예술사 용어나 표현주의/추상주의와 같은 사조 용어를 적극적으로 사용해도 좋습니다.\n"
                "전공자나 큐레이터도 납득할 수 있는 해설이 되어야 합니다.\n"
            )
        else:  # 기본값 "중"
            level_prompt = (
                "일반인이 이해할 수 있도록, 친절하고 알기 쉬운 용어로 설명해주세요.\n"
                "작품의 배경과 작가의 의도 정도는 간단히 다루고, 너무 깊이 있는 분석은 피해주세요.\n"
            )

        # 프롬프트 구성
        prompt = (
            "당신은 AI 기반 미술 도슨트입니다.\n"
            f"다음 이미지는 Vision API에서 '{best_guess}'로 추정된 작품입니다. 실제 작품 정보는 추정과 다를 수 있습니다.\n"
            "이 이미지에 대해 다음 형식을 기준으로 한국어로 정확한 정보를 제공해주세요.\n\n"
            "감정적인 말투가 아닌 객관적이고 정확한 정보만을 출력해야합니다.\n"
            "이야기체가 아닌 정보 전달체여야만 합니다.\n"
            "작품에 대한 해설은 대중적으로 받아들여지는 정확한 정보여야만 합니다.\n\n"
            "제작 년도가 정확한지 다시 검색 후 정확한 제작 년도를 반환받아야 합니다.\n\n"
            "작품 해설은 최소 10문장 이상, 서술형 문단으로 작성하며, 미술관 전시 안내문처럼 진지하고 구체적인 문장으로 구성해주세요.**\n"
            "가능하다면 연도, 작가, 사조 정보도 문맥 속에 자연스럽게 통합해주세요.\n\n"
            f"{level_prompt}"
            "작품 이미지: (이미지는 아래의 base64로 제공됨)\n"
            "작품 이름:\n"
            "작가명:\n"
            "제작 년도:\n"
            "예술사조:\n"
            "작품 해설:"
        )

        # Gemini 요청
        response = model.generate_content([prompt, image], stream=False)
        result = response.text.strip()

        # 결과 추출 및 description 전처리
        raw_description = _extract_description(result)
        cleaned_description = _clean_description(raw_description)

        parsed = {
            "title": _extract_field(result, r"작품\s*이름\s*:\s*(.*)"),
            "artist": _extract_field(result, r"작가명\s*:\s*(.*)"),
            "year": _extract_field(result, r"제작\s*년도\s*:\s*(.*)"),
            "style": _extract_field(result, r"예술사조\s*:\s*(.*)"),
            "description": cleaned_description,
            "level": level
        }

        return parsed

    except Exception as e:
        return {"error": f"[Gemini 오류]: {e}"}


# ──────────────── 텍스트 추출 유틸 ────────────────
def _extract_field(text: str, pattern: str) -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else "정보 없음"


def _extract_description(text: str) -> str:
    match = re.search(r"작품\s*해설\s*:\s*(.*)", text, re.DOTALL)
    return match.group(1).strip() if match else "설명 없음"


def _clean_description(desc: str) -> str:
    # \n0 같은 이상한 줄바꿈 제거 → \n → 공백
    desc = desc.replace("\\n", "\n")
    desc = re.sub(r"\n+", " ", desc)          # 여러 줄바꿈 → 하나의 공백
    desc = re.sub(r"\s+", " ", desc).strip()  # 연속 공백 정리
    return desc


# ──────────────── Swagger 테스트용 API ────────────────
@app.post("/generate-artwork-description/")
async def generate_artwork_description(
    file: UploadFile = File(...),
    best_guess: str = Form(""),
    level: Literal["상", "중", "하"] = Form("중")
):
    image_bytes = await file.read()
    result = get_artwork_title_from_bytes(image_bytes, best_guess, level)
    return JSONResponse(content=result)
