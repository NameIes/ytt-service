import json
import requests


def copy_post_to_websites(business, images, videos, text):
    files = {}

    for i, image in enumerate(images):
        files['file' + str(i)] = open(image.file.path, 'rb')

    for website in business.websites.all():
        for i in files.keys():
            files[i].seek(0)
        requests.post(website.url, data={
            'videos': json.dumps(videos),
            'text': text,
            'code': website.code
        }, files=files)
