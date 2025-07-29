import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def convert_difficulty_prompt(original_text: str, level: str) -> str:
    if level == "EASY":
        level_prompt = (
            "어린이가 이해하기 힘든 단어 사용을 지양하고 쉬운 단어와 짧은 문장을 사용해주세요.\n"
            "전문 용어나 외래어는 풀어서 설명하고, 핵심 내용만 간단하게 요약해주세요.\n"
            # "어려운 단어나 역사적 맥락은 설명하지 마세요.\n"
            "구어체를 피하고 문어체로 작성해주세요.\n"
            "어린이에게 말하는 듯한 말투를 사용하지 말아 주세요.\n"
        )
    elif level == "HARD":
        level_prompt = (
            "예술사적 맥락, 작가의 철학, 시대적 배경, 작품 기법을 포함한 깊이 있는 설명을 해주세요.\n"
            "예술사 용어나 표현주의/추상주의와 같은 사조 용어를 적극적으로 사용해도 좋습니다.\n"
            "전공자나 큐레이터도 납득할 수 있는 해설이 되어야 합니다.\n"
            "구어체를 피하고 문어체로 작성해주세요.\n"
        )
    else:
        level_prompt = (
            "일반인이 이해할 수 있도록, 친절하고 알기 쉬운 용어로 설명해주세요.\n"
            "작품의 배경과 작가의 의도 정도는 간단히 다루고, 너무 깊이 있는 분석은 피해주세요.\n"
            "구어체를 피하고 문어체로 작성해주세요.\n"
        )

    prompt = (
        "다음은 작품 해설입니다. 이 해설을 다음 난이도에 맞게 다시 작성해주세요.\n\n"
        f"--- 원본 해설 ---\n{original_text}\n\n"
        f"--- 난이도 기준 ---\n{level_prompt}"
        "\n\n--- 변환된 해설 ---"
    )

    response = model.generate_content(prompt, stream=False)
    return response.text.strip()
