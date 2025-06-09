import pytest
from backend.scripts.darija_script_generator import DarijaScriptGenerator
from backend.scripts.spot_collector import SpotCollector
from backend.scripts.image_handler import ImageHandler
from backend.scripts.tts_video_generator import TTSVideoGenerator

# Sample spot for testing
def sample_spot():
    return {
        "name": "Café Hafa",
        "address": "Tangier, Morocco",
        "location": {"lat": 35.789, "lng": -5.813},
        "opening_hours": ["08:00–23:00"],
        "types": ["cafe"],
        "reviews": [],
        "user_ratings_total": 1000,
        "photos": []
    }

def test_script_generator():
    gen = DarijaScriptGenerator()
    script = gen.generate_script(sample_spot(), category="cafe", city="طنجة")
    assert isinstance(script, str) and len(script) > 10

def test_image_handler(monkeypatch):
    handler = ImageHandler()
    # Monkeypatch fetch_images to avoid real API call
    monkeypatch.setattr(handler, "fetch_images", lambda q, count: ["test.jpg"]*2)
    monkeypatch.setattr(handler, "download_and_process", lambda url, name, idx: f"/tmp/{name}_{idx}.jpg")
    paths = handler.fetch_and_save_images("Café Hafa")
    assert len(paths) == 2

def test_tts_video_generator(monkeypatch):
    tts = TTSVideoGenerator()
    # Monkeypatch script_to_audio and images_to_video
    monkeypatch.setattr(tts, "script_to_audio", lambda s, n: "/tmp/audio.mp3")
    monkeypatch.setattr(tts, "images_to_video", lambda imgs, a, n: "/tmp/video.mp4")
    video = tts.generate("test script", ["img1.jpg", "img2.jpg"], "Café Hafa")
    assert video.endswith(".mp4")
