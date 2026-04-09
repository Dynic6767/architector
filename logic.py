import json
import requests
import time
from config import *

class Leonardobot:
    def __init__(self, api_key):
        self.api_key = "45561f30-65ea-409a-ac38-add7eefdca65"
        self.authorization = "Bearer %s" % api_key
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.authorization
        }
        self.url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    def gen_image(self, promt, filename="result.jpg"):
        payload = {
            "height": 512,
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Setting model ID to Leonardo Creative
            "prompt": promt,
            "width": 512
        }

        response = requests.post(self.url, json=payload, headers=self.headers)
        print(response.status_code)
        generation_id = response.json()['sdGenerationJob']['generationId']
        time.sleep(20)

        url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id
        response = requests.get(url, headers=self.headers)
        data = response.json()

        gen_img = data["generations_by_pk"]["generated_images"][0]["url"]
        gen_data = requests.get(gen_img).content

        with open(filename, "wb") as f:
            f.write(gen_data)

        return gen_img

api = Leonardobot("45561f30-65ea-409a-ac38-add7eefdca65")

if __name__ == "__main__":
    api.gen_image("white cat", "cat.jpg")