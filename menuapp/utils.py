import os
import requests
from slugify import slugify
from django.conf import settings

def download_image(url: str, hotel_name: str) -> str:
    """
    Download image from URL and store it under media/menu_images/<hotel>/
    Returns relative path, or None if failed.
    """
    if not url:
        return None

    try:
        # Send headers to avoid 403/blocked requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, stream=True, timeout=15, allow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        print(f"[Image Download Error] URL: {url} | Error: {e}")
        return None

    # Check content type
    content_type = response.headers.get("Content-Type", "").lower()
    if "image" not in content_type:
        print(f"[Invalid Image Content] URL: {url} | Content-Type: {content_type}")
        return None

    # Determine file extension
    if "jpeg" in content_type or "jpg" in content_type:
        ext = "jpg"
    elif "png" in content_type:
        ext = "png"
    elif "gif" in content_type:
        ext = "gif"
    else:
        ext = "jpg"  # default fallback

    # Prepare folder
    hotel_slug = slugify(hotel_name)
    dest_dir = os.path.join(settings.MEDIA_ROOT, "menu_images", hotel_slug)
    os.makedirs(dest_dir, exist_ok=True)

    # Create safe filename
    base_name = slugify(url.split("/")[-1]) or slugify(hotel_name)
    file_name = f"{base_name}.{ext}"
    file_path = os.path.join(dest_dir, file_name)

    try:
        with open(file_path, "wb") as img_file:
            for chunk in response.iter_content(chunk_size=1024):
                img_file.write(chunk)
    except Exception as e:
        print(f"[Save Image Error] URL: {url} | Error: {e}")
        return None

    # Return relative path for MEDIA_URL serving
    rel_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
    return rel_path.replace("\\", "/")