import requests
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from backend.config.settings import UNSPLASH_ACCESS_KEY, IMAGE_OUTPUT_PATH
import logging

class ImageHandler:
    def __init__(self, access_key=None, output_path=None):
        self.access_key = access_key or UNSPLASH_ACCESS_KEY
        self.output_path = output_path or IMAGE_OUTPUT_PATH
        os.makedirs(self.output_path, exist_ok=True)
        self.logger = logging.getLogger("microtours.imagehandler")

    def fetch_images(self, query, count=3):
        try:
            url = f"https://api.unsplash.com/search/photos"
            params = {
                "query": query,
                "per_page": count,
                "client_id": self.access_key
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return [img['urls']['regular'] for img in data['results']]
            self.logger.error(f"Unsplash API error: {response.status_code} {response.text}")
        except Exception as e:
            self.logger.exception("Exception fetching images")
        return []

    def download_and_process(self, img_url, spot_name, idx=0):
        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert("RGB")
                img = img.resize((1280, 720))
                # Add watermark
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()
                text = f"{spot_name} - MicroTours"
                draw.text((10, 680), text, (255,255,255), font=font)
                # Save
                filename = f"{spot_name.replace(' ', '_')}_{idx}.jpg"
                path = os.path.join(self.output_path, filename)
                img.save(path, "JPEG")
                return path
            self.logger.error(f"Image download failed: {img_url}")
        except Exception as e:
            self.logger.exception("Exception processing image")
        return None

    def fetch_and_save_images(self, spot_name, query=None, count=3):
        query = query or spot_name
        urls = self.fetch_images(query, count)
        paths = []
        for idx, url in enumerate(urls):
            path = self.download_and_process(url, spot_name, idx)
            if path:
                paths.append(path)
        return paths
