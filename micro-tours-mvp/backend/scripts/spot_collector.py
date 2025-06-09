import requests
import json
import logging
from backend.config.settings import GOOGLE_PLACES_API_KEY

class SpotCollector:
    def __init__(self, api_key=None):
        self.api_key = api_key or GOOGLE_PLACES_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/place/details/json"
        self.search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        self.logger = logging.getLogger("microtours.spotcollector")

    def fetch_spot(self, place_id):
        try:
            params = {
                "place_id": place_id,
                "fields": "name,geometry,opening_hours,types,review,user_ratings_total,formatted_address,photos",
                "key": self.api_key
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OK":
                    return self.clean_data(data["result"])
                self.logger.error(f"Google Places error: {data.get('status')}")
            else:
                self.logger.error(f"HTTP error: {response.status_code}")
        except Exception as e:
            self.logger.exception("Exception fetching spot")
        return None

    def search_spots(self, location, radius=1000, type="tourist_attraction"):
        try:
            params = {
                "location": location,  # "lat,lng"
                "radius": radius,
                "type": type,
                "key": self.api_key
            }
            response = requests.get(self.search_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OK":
                    return [self.clean_data(spot) for spot in data["results"]]
                self.logger.error(f"Google Places error: {data.get('status')}")
            else:
                self.logger.error(f"HTTP error: {response.status_code}")
        except Exception as e:
            self.logger.exception("Exception searching spots")
        return []

    def clean_data(self, data):
        return {
            "name": data.get("name"),
            "address": data.get("formatted_address"),
            "location": data.get("geometry", {}).get("location"),
            "opening_hours": data.get("opening_hours", {}).get("weekday_text", []),
            "types": data.get("types", []),
            "reviews": data.get("reviews", []),
            "user_ratings_total": data.get("user_ratings_total"),
            "photos": data.get("photos", []),
        }

    def from_json(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [self.clean_data(spot) for spot in data]
        except Exception as e:
            self.logger.exception("Exception loading spots from JSON")
            return []
