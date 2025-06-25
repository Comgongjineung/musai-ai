from __future__ import annotations
import json, os
from typing import List, Dict

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ───────────────────────── 1단계: 숨은 이야기·상징 요약 ─────────────────────────
def _summarize(img_bytes: bytes) -> dict:
    prompt = (
        'JSON ONLY: {"story":"...", "symbols":["..."]}\n'
        "• story: 280자 이하 한국어로 그림의 배경이 되는 다층적이고 은유적인 서사, 사회적 풍자, 혹은 숨겨진 의미를 요약\n"
        "• symbols: 이야기와 직접 연결되는 핵심 상징 오브젝트·인물 최대 6개"
    )
    rsp = model.generate_content(
        [prompt, {"mime_type": "image/jpeg", "data": img_bytes}],
        generation_config={"response_mime_type": "application/json"},
    )
    return json.loads(rsp.text)

# ───────────────────────── 2단계: 좌표·설명 추출 ─────────────────────────
def _points(img_bytes: bytes, ctx: dict, max_pts: int) -> List[Dict]:
    story   = ctx.get("story", "")
    symbols = ", ".join(ctx.get("symbols", []))

    prompt = (
    '이 그림에서 **예술사적으로 가장 널리 공인된 해석에 기반하여**, story 및 symbols와 연결되는 핵심 상징 요소들을 뽑아 최대 {max_pts}개의 JSON 포인트로 정리하라.\n'
    '각 description은 반드시 실제 예술사 논문이나 비평에서 언급된 의미를 바탕으로 3문장 이내로 요약하며, **과도한 현대적 비판이나 추측성 해석은 절대 포함하지 않는다.**\n' # 이 부분 수정 및 강조
    '형식: {"points":[{"id":"pt1","x":0.00,"y":0.00,"description":"**대상명**: 내용 요약"}]}\n'
    f'<STORY>{story}</STORY>\n<SYMBOLS>{symbols}</SYMBOLS>'
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
    context = _summarize(img_bytes)
    return _points(img_bytes, context, max_points)

# ───────────────────────── CLI 테스트 ─────────────────────────
if __name__ == "__main__":
    import sys, pathlib, pprint
    with pathlib.Path(sys.argv[1]).open("rb") as f:
        pprint.pp(extract_points(f.read()), width=120)