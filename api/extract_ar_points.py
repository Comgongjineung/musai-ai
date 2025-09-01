# api/extract_ar_points.py
from __future__ import annotations
import base64, json, os
from typing import List, Dict
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if client.api_key is None:
    raise RuntimeError("OPENAI_API_KEY 환경 변수가 필요합니다.")

def _to_data_url(img: bytes) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(img).decode()

# ───────────────────────── 1단계: 숨은 이야기·상징 요약 ─────────────────────────
def _summarize(img_url: str) -> dict:
    prompt = (
        'Return ONLY JSON: {"story":"...", "symbols":["..."]} . '
        "• story: 그림의 숨은 이야기·풍자·금기 핵심 요약 (≤280자, KOR)\n"
        "• symbols: 이야기와 직결된 오브젝트·인물·조각상 등 최대 6개"
    )
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user",
             "content": [{"type": "image_url", "image_url": {"url": img_url}}]},
        ],
        timeout=60,
    )
    return json.loads(res.choices[0].message.content)

# ───────────────────────── 2단계: 좌표·설명 추출 ─────────────────────────
def _points(img_url: str, ctx: dict, max_pts=4) -> List[Dict]:
    story   = ctx.get("story", "")
    symbols = ", ".join(ctx.get("symbols", []))

    prompt = (
    '이 그림에서 예술사적으로 공인된 상징 요소들 중, story 및 symbols와 연결되는 핵심만 뽑아 최대 {max_pts}개의 JSON 포인트로 정리하라.\n'
    '각 description은 반드시 실제 해석/논문/예술사에서 언급된 의미 기반으로 2문장 요약하며, 과도한 해석은 제외.\n'
    '형식: {"points":[{"id":"pt1","x":0.00,"y":0.00,"description":"**대상명**: 내용 요약"}]}\n'
    f'<STORY>{story}</STORY>\n<SYMBOLS>{symbols}</SYMBOLS>'
)

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user",
             "content": [{"type": "image_url", "image_url": {"url": img_url}}]},
        ],
        timeout=60,
    )

    pts = json.loads(res.choices[0].message.content).get("points", [])[:max_pts]
    for i, p in enumerate(pts, 1):
        p.setdefault("id", f"pt{i}")
        p["x"] = max(0, min(1, float(p.get("x", 0))))
        p["y"] = max(0, min(1, float(p.get("y", 0))))
        p["description"] = str(p.get("description", ""))[:150]
    return pts

# ───────────────────────── 외부 호출 함수 ─────────────────────────
def extract_points(img_bytes: bytes, max_points: int = 4) -> List[Dict]:
    url   = _to_data_url(img_bytes)
    ctx   = _summarize(url)          # 숨은 이야기·상징 추출
    return _points(url, ctx, max_points)

# ───────────────────────── CLI 테스트 ─────────────────────────
if __name__ == "__main__":
    import sys, pathlib, pprint
    with pathlib.Path(sys.argv[1]).open("rb") as f:
        pprint.pp(extract_points(f.read()), width=120)