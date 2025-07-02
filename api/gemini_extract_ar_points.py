from __future__ import annotations
import json, os
from typing import List, Dict

import google.generativeai as genai

# ───────────────────────── API 초기화 ─────────────────────────
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ───────────────────────── 1단계: 작품 설명 생성 ─────────────────────────
def _describe_artwork(img_bytes: bytes) -> dict:
    prompt = (
        "이 이미지는 하나의 예술 작품이다.\n"
        "해당 그림에 대한 예술사적·상징적 분석을 최대한 깊이 있고 중립적인 시각에서 서술해줘.\n"
        "비평, 은유, 풍자, 시대적 맥락, 등장 인물, 색상과 구도에 기반한 상징 해석 등을 포함해서 800자 이내 한국어로 작성해.\n"
        'JSON ONLY: {"description":"..."}'
    )

    rsp = model.generate_content(
        [prompt, {"mime_type": "image/jpeg", "data": img_bytes}],
        generation_config={"response_mime_type": "application/json"},
    )
    return json.loads(rsp.text)

# ───────────────────────── 2단계: AR 포인트 추출 ─────────────────────────
def _points_from_description(img_bytes: bytes, description: str, max_pts: int) -> List[Dict]:
    prompt = (
        f'다음은 예술 작품에 대한 해설이다. 이 내용을 바탕으로, 이미지에서 AR 포인트로 시각화할 수 있는 핵심 상징 요소들을 최대 {max_pts}개 추출하라.\n'
        '각 포인트는 반드시 실제 이미지 속 시각적 요소와 연결되어야 하며, 좌표(x, y)는 (0~1) 정규화된 상대 좌표이다.\n'
        '각 설명(description)은 3문장 이내로 예술사적으로 정당화 가능한 해석만 포함하고, 과도한 추측은 배제한다.\n'
        '응답 형식: {"points":[{"id":"pt1","x":0.00,"y":0.00,"description":"**대상명**: 내용 요약"}]}\n'
        f"<DESCRIPTION>{description}</DESCRIPTION>"
    )

    rsp = model.generate_content(
        [prompt, {"mime_type": "image/jpeg", "data": img_bytes}],
        generation_config={"response_mime_type": "application/json"},
    )

    pts = json.loads(rsp.text)["points"][:max_pts]

    for i, p in enumerate(pts, 1):
        p.setdefault("id", f"pt{i}")
        p["x"] = max(0, min(1, float(p.get("x", 0))))
        p["y"] = max(0, min(1, float(p.get("y", 0))))
        p["description"] = str(p.get("description", ""))[:150]

    return pts

# ───────────────────────── 외부 호출 함수 ─────────────────────────
def extract_points(img_bytes: bytes, max_points: int = 4) -> List[Dict]:
    context = _describe_artwork(img_bytes)
    return _points_from_description(img_bytes, context.get("description", ""), max_points)

# ───────────────────────── CLI 테스트 ─────────────────────────
if __name__ == "__main__":
    import sys, pathlib, pprint

    if len(sys.argv) < 2:
        print("사용법: python script.py [이미지_경로]")
        sys.exit(1)

    image_path = pathlib.Path(sys.argv[1])
    with image_path.open("rb") as f:
        result = extract_points(f.read())
        pprint.pp(result, width=120)
