from google.cloud import vision
import io

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

def get_best_guess_label(image_data: bytes):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_data)

    response = client.web_detection(image=image)
    web_detection = response.web_detection

    if web_detection.best_guess_labels:
        best_guess = web_detection.best_guess_labels[0].label.lower()
    else:
        best_guess = ""

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

    if title_candidates:
        return title_candidates[0][0]

    for title in page_titles:
        if is_probably_title(title):
            return title

    return best_guess if is_probably_title(best_guess) else None

