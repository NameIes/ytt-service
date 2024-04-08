import requests


def copy_post_to_websites(business, images, videos, text):
    files = []

    for image in images:
        files.append(
            ('file', open(image.file.path, 'rb'))
        )

    for website in business.websites.all():
        requests.post(website.url, data={
            'videos': videos,
            'text': text,
            'code': website.code
        }, files=files)
