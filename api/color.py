from colorthief import ColorThief
from fastapi import UploadFile
from io import BytesIO

def extract_color_info(image_file: UploadFile) -> dict:
    try:
        img_bytes = BytesIO(image_file.file.read())
        color_thief = ColorThief(img_bytes)

        dominant = color_thief.get_color(quality=1)
        palette = color_thief.get_palette(color_count=5)

        return {
            "dominant_rgb": dominant,
            "palette": palette
        }

    except Exception as e:
        raise RuntimeError(f"Color extraction failed: {str(e)}")
