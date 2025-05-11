# vision.py
from google.cloud import vision
from google.oauth2 import service_account

# 인증 정보로 Vision API 클라이언트 생성
credentials = service_account.Credentials.from_service_account_file("service_account.json")
client = vision.ImageAnnotatorClient(credentials=credentials)

def get_best_guess_label(image_bytes: bytes) -> str | None:
    image = vision.Image(content=image_bytes)
    response = client.web_detection(image=image)

    if response.error.message:
        raise Exception(f"이미지 인식 실패: {response.error.message}")

    best_guess_labels = response.web_detection.best_guess_labels
    if best_guess_labels:
        return best_guess_labels[0].label
    return None
