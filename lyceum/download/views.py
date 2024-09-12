from django.conf import settings
from django.http.response import FileResponse

__all__ = []


def download_file(request, image_url):
    file_path = settings.MEDIA_ROOT / image_url
    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
    )
