import base64
import os
import io
import re
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Literal

# 환경설정
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

# 서양 미술 사조
KNOWN_STYLES = [
    "고대 미술", "중세 미술", "르네상스", "바로크", "로코코",
    "신고전주의", "낭만주의", "사실주의", "후기 인상주의", "후기인상주의",
    "신인상주의", "인상주의", "아르누보", "표현주의", "입체주의",
    "미래주의", "초현실주의", "추상표현주의", "팝아트", "현대미술"
]

def determine_style(end_date: int, gemini_style: str) -> str:
    if gemini_style and gemini_style.strip():
        gemini_style_clean = gemini_style.strip()
        if gemini_style_clean in KNOWN_STYLES:
            return gemini_style_clean

    if end_date is None:
        return "정보 없음"
    if end_date <= 400:
        return "고대 미술"
    elif end_date <= 1400:
        return "중세 미술"
    elif end_date <= 1600:
        return "르네상스"
    elif end_date <= 1750:
        return "바로크"
    elif 1720 <= end_date <= 1780:
        return "로코코"
    elif 1750 <= end_date <= 1830:
        return "신고전주의"
    elif 1800 <= end_date <= 1850:
        return "낭만주의"
    elif 1840 <= end_date <= 1880:
        return "사실주의"
    elif 1860 <= end_date <= 1890:
        return "인상주의"
    elif 1880 <= end_date <= 1905:
        return "후기 인상주의"
    elif 1890 <= end_date <= 1910:
        return "아르누보"
    elif 1905 <= end_date <= 1930:
        return "표현주의"
    elif 1907 <= end_date <= 1920:
        return "입체주의"
    elif 1910 <= end_date <= 1930:
        return "미래주의"
    elif 1915 <= end_date <= 1945:
        return "초현실주의"
    elif 1940 <= end_date <= 1960:
        return "추상표현주의"
    elif 1955 <= end_date <= 1970:
        return "팝아트"
    elif end_date >= 1960:
        return "현대미술"
    else:
        return "정보 없음"

# 동아시아/아시아 필터
def classify_asian_style(style_text: str) -> str:
    style_text = style_text.lower()

    #동아시아 - 한국
    if any(k in style_text for k in ["고조선", "삼국시대", "고구려", "백제", "신라", "통일신라", "고려", "조선", "korea"]):
        return "동아시아"
    #동아시아 - 일본
    elif any(k in style_text for k in ["에도", "에도막부", "에도시대", "메이지", "다이쇼", "쇼와", "heian", "kamakura", "muromachi"]):
        return "동아시아"
    #동아시아 - 중국
    elif any(k in style_text for k in ["하", "진", "한", "수", "당", "송", "원", "명", "청", "china"]):
        return "동아시아"
    #기타 동아시아
    elif any(k in style_text for k in ["몽골", "tibet", "taiwan"]):
        return "동아시아"
    #동남아시아
    elif any(k in style_text for k in [
        "thailand", "vietnam", "cambodia", "laos", "myanmar", "indonesia",
        "philippines", "malaysia", "singapore"
    ]):
        return "동남아시아"
    #남아시아
    elif any(k in style_text for k in [
        "india", "pakistan", "bangladesh", "sri lanka", "nepal", "bhutan", "maldives"
    ]):
        return "남아시아"
    #중앙아시아
    elif any(k in style_text for k in [
        "kazakhstan", "uzbekistan", "turkmenistan", "kyrgyzstan", "tajikistan"
    ]):
        return "중앙아시아"
    #서아시아/중동
    elif any(k in style_text for k in [
        "iran", "persia", "iraq", "syria", "turkey", "anatolia", "saudi arabia",
        "afghanistan", "armenia", "georgia"
    ]):
        return "서아시아/중동"

    return "정보 없음"

# Gemini 스트리밍
async def generate_artwork_stream(image_bytes: bytes, best_guess: str, level: str):
    try:
        #이미지 처리
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        w, h = image.size
        target_w = 342
        target_h = int(target_w / w * h)
        try:
            resample_mode = Image.Resampling.LANCZOS
        except AttributeError:
            resample_mode = Image.ANTIALIAS

        image = image.resize((target_w, target_h), resample_mode)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        #난이도 프롬프트
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
        else:
            #기본값 "중"
            level_prompt = (
                "일반인이 이해할 수 있도록, 친절하고 알기 쉬운 용어로 설명해주세요.\n"
                "작품의 배경과 작가의 의도 정도는 간단히 다루고, 너무 깊이 있는 분석은 피해주세요.\n"
            )

        #프롬프트 구성
        prompt = (
            "당신은 AI 기반 미술 도슨트입니다.\n"
            f"다음 이미지는 Vision API에서 '{best_guess}'로 추정된 작품입니다. 실제 작품 정보는 추정과 다를 수 있습니다.\n"
            "이 이미지에 대해 다음 형식을 기준으로 한국어로 정확한 정보를 제공해주세요.\n\n"
            "감정적인 말투가 아닌 객관적이고 정확한 정보만을 출력해야합니다.\n"
            "이야기체가 아닌 정보 전달체여야만 합니다.\n"
            "작품에 대한 해설은 대중적으로 받아들여지는 정확한 정보여야만 합니다.\n\n"
            "제작 년도가 정확한지 다시 검색 후 정확한 제작 년도를 반환받아야 합니다.\n\n"
            "작품 해설은 최소 10문장 이상, 서술형 문단으로 작성하며, 미술관 전시 안내문처럼 진지하고 구체적인 문장으로 구성해주세요.\n"
            "가능하다면 연도, 작가, 사조 정보도 문맥 속에 자연스럽게 통합해주세요.\n\n"
            "모든 대답은 korean(한국어)로 작성되어야 합니다.\n\n"
            "예술사조는 00주의 형태로 작성되어야 합니다.\n"
            f"작품이름이 없다면 '{best_guess}'를 반환해야합니다.\n\n"
            f"{level_prompt}"
            "작품 이미지: (이미지는 아래의 base64로 제공됨)\n"
            "작품 이름:\n"
            "작가명:\n"
            "제작 년도:\n"
            "예술사조:\n"
            "작품 해설:"
        )

        #Gemini 스트리밍 요청
        response = model.generate_content([prompt, image], stream=True)
        full_text = ""

        for chunk in response:
            yield chunk.text
            full_text += chunk.text

    except Exception as e:
        yield f"[Gemini 오류]: {e}"

#API
@app.post("/generate-artwork-description/")
async def generate_artwork_description(
    file: UploadFile = File(...),
    best_guess: str = Form(""),
    level: Literal["상", "중", "하"] = Form("중")
):
    image_bytes = await file.read()
    return StreamingResponse(
        generate_artwork_stream(image_bytes, best_guess, level),
        media_type="text/plain"
    )

#유틸
def _extract_field(text: str, pattern: str) -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else "정보 없음"

def _extract_description(text: str) -> str:
    match = re.search(r"작품\s*해설\s*:\s*(.*)", text, re.DOTALL)
    return match.group(1).strip() if match else "설명 없음"
