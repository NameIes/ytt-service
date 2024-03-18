import requests
from db_models.models import DownloadedFile
from django.core import files
from io import BytesIO


def save_files_from_telegram(urls: list) -> list:
    downloaded_files = []

    for url in urls:
        response = requests.get(url)
        fstream = BytesIO()
        fstream.write(response.content)
        filename = url.split('/')[-1]

        file_obj = DownloadedFile()
        file_obj.file.save(filename, files.File(fstream))
        file_obj.save()

        downloaded_files.append(file_obj)

    return downloaded_files
