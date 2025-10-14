from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from google.cloud import vision
from api.jemini import get_artwork_title_from_bytes

router = APIRouter()

def is_probably_title(text: str) -> bool:
    if not text:
        return False
    if text.lower().startswith("by "):
        return False
    if any(word in text.lower() for word in ["artist", "painting", "artwork", "gallery"]):
        return False
    if len(text) > 50:
        return False
    return True

def get_image_analysis(image_data: bytes):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_data)
    response = client.web_detection(image=image)
    web_detection = response.web_detection

    # 원본 이미지 URL
    image_url = None
    if web_detection.full_matching_images:
        image_url = web_detection.full_matching_images[0].url
    elif web_detection.partial_matching_images:
        image_url = web_detection.partial_matching_images[0].url

    # Best Guess Label
    best_guess = ""
    if web_detection.best_guess_labels:
        best_guess = web_detection.best_guess_labels[0].label.lower()

    # title 후보 추출
    entities = web_detection.web_entities if web_detection.web_entities else []
    title_candidates = []
    for entity in entities:
        desc = entity.description.strip()
        if desc and is_probably_title(desc):
            title_candidates.append((desc, entity.score))
    title_candidates.sort(key=lambda x: x[1], reverse=True)

    page_titles = []
    if web_detection.pages_with_matching_images:
        for page in web_detection.pages_with_matching_images:
            if page.page_title:
                page_titles.append(page.page_title.strip())

    # title 결정
    title = None
    if title_candidates:
        title = title_candidates[0][0]
    else:
        for t in page_titles:
            if is_probably_title(t):
                title = t
                break

    if not title and is_probably_title(best_guess):
        title = best_guess

    return image_url, best_guess, title