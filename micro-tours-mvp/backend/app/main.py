from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.scripts.spot_collector import SpotCollector
from backend.scripts.darija_script_generator import DarijaScriptGenerator
from backend.scripts.image_handler import ImageHandler
from backend.scripts.tts_video_generator import TTSVideoGenerator
from backend.scripts.landing_page_generator import LandingPageGenerator
import os
import logging

app = FastAPI(
    title="Micro-Tours Darija API",
    description="Automated Moroccan micro-tour video generator using Python, FastAPI, TTS, and AI.",
    version="1.0.0"
)

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("microtours")

API_KEY = os.getenv("SECRET_KEY", "changeme")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        logger.warning("Unauthorized API key attempt")
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

class SpotRequest(BaseModel):
    place_id: str = None
    json_path: str = None
    category: str = "cafe"
    city: str = "المغرب"

@app.get("/", tags=["Health"])
def read_root(x_api_key: str = Depends(verify_api_key)):
    """Health check endpoint."""
    logger.info("Health check endpoint called.")
    return {"message": "Welcome to Micro-Tours Darija API!"}

@app.post("/generate_microtour", tags=["Microtour"])
def generate_microtour(req: SpotRequest, x_api_key: str = Depends(verify_api_key)):
    """
    Generate a micro-tour: spot info, Darija script, images, video, and landing page.
    """
    try:
        logger.info(f"Microtour request: {req}")
        # 1. Collect spot info
        collector = SpotCollector()
        if req.place_id:
            spot = collector.fetch_spot(req.place_id)
        elif req.json_path:
            spots = collector.from_json(req.json_path)
            spot = spots[0] if spots else None
        else:
            logger.error("No place_id or json_path provided")
            return {"success": False, "error": "No place_id or json_path provided"}
        if not spot:
            logger.error("Spot not found")
            return {"success": False, "error": "Spot not found"}

        # 2. Generate Darija script
        script_gen = DarijaScriptGenerator()
        script = script_gen.generate_script(spot, category=req.category, city=req.city)
        if not script or len(script) < 10:
            logger.error("Script generation failed or too short")
            return {"success": False, "error": "Script generation failed"}

        # 3. Fetch images
        img_handler = ImageHandler()
        image_paths = img_handler.fetch_and_save_images(spot['name'])
        if not image_paths:
            logger.error("Image fetching failed")
            return {"success": False, "error": "Image fetching failed"}

        # 4. Generate TTS + video
        tts_video = TTSVideoGenerator()
        video_path = tts_video.generate(script, image_paths, spot['name'])
        if not video_path:
            logger.error("Video generation failed")
            return {"success": False, "error": "Video generation failed"}

        # 5. Generate landing page
        landing_gen = LandingPageGenerator()
        html_path = landing_gen.generate(spot, script, video_path)
        if not html_path:
            logger.error("Landing page generation failed")
            return {"success": False, "error": "Landing page generation failed"}

        logger.info(f"Microtour generated for {spot['name']}")
        return {
            "success": True,
            "spot": spot,
            "script": script,
            "images": image_paths,
            "video": video_path,
            "landing_page": html_path
        }
    except Exception as e:
        logger.exception("Error generating microtour")
        return {"success": False, "error": str(e)}
