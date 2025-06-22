from __future__ import annotations

import base64
import io
import os
import re
from typing import Dict

from dotenv import load_dotenv
from PIL import Image
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"


def get_artwork_title_from_bytes(
    image_bytes: bytes,
    best_guess: str = "",
    *,
    target_width: int = 342,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> Dict[str, str]:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        ow, oh = image.size
        th = int(oh * target_width / ow)
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.ANTIALIAS
        image = image.resize((target_width, th), resample)
        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=92)
        data_uri = f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}"

        prompt = (
            "당신은 AI 기반 도슨트 앱입니다.\n"
            f"Vision API는 이 작품을 '{best_guess}'(이)라고 추정했습니다.\n"
            "아래 양식에 맞춰 한국어로 답변하세요. "
            "특히 '작품 해설'은 10문장 이상, 구체적 서술형으로 작성해야 합니다.\n\n"
            "작품 이미지:\n"
            "작품 이름:\n"
            "작가명:\n"
            "제작 년도:\n"
            "예술사조:\n"
            "작품 해설:"
        )

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }
        ]

        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        text = response.choices[0].message.content.strip()

        return {
            "image_url": data_uri,
            "title": _extract_field(text, r"작품\s*이름\s*:\s*(.*)"),
            "artist": _extract_field(text, r"작가명\s*:\s*(.*)"),
            "year": _extract_field(text, r"제작\s*년도\s*:\s*(.*)"),
            "style": _extract_field(text, r"예술사조\s*:\s*(.*)"),
            "description": _extract_description(text),
        }

    except Exception as exc:
        return {"error": f"[GPT-4o mini 오류] {exc}"}


def _extract_field(text: str, pattern: str) -> str:
    m = re.search(pattern, text)
    value = m.group(1).strip() if m else ""
    return value if value else "정보 없음"


def _extract_description(text: str) -> str:
    m = re.search(r"작품\s*해설\s*:\s*(.*)", text, flags=re.DOTALL)
    value = m.group(1).strip() if m else ""
    return value if value else "설명 없음"


if __name__ == "__main__":
    import argparse
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("image_path")
    ap.add_argument("--guess", default="")
    args = ap.parse_args()

    try:
        with open(args.image_path, "rb") as f:
            info = get_artwork_title_from_bytes(f.read(), best_guess=args.guess)
            for k, v in info.items():
                print(f"{k}: {v}")
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)
