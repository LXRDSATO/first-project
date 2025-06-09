# Micro-Tours Darija API Documentation

This document describes the available API endpoints for the Micro-Tours Darija project.

---

## Authentication

All endpoints require an `x-api-key` header with your API key.

```
x-api-key: your_secret_key
```

---

## Endpoints

### 1. Health Check

**GET /**

- **Description:** Check if the API is running.
- **Headers:**  
  `x-api-key: your_secret_key`
- **Response:**
  ```json
  {
    "message": "Welcome to Micro-Tours Darija API!"
  }
  ```

---

### 2. Generate Microtour

**POST /generate_microtour**

- **Description:** Generate a micro-tour video, script, images, and landing page for a given place.
- **Headers:**  
  `x-api-key: your_secret_key`
- **Request Body:**
  ```json
  {
    "place_id": "ChIJd8BlQ2BZwokRAFUEcm_qrcA", // required unless using json_path
    "category": "cafe",                        // optional, default: "cafe"
    "city": "طنجة"                             // optional, default: "المغرب"
  }
  ```
  Or:
  ```json
  {
    "json_path": "/path/to/spot.json",         // alternative to place_id
    "category": "monument",
    "city": "الرباط"
  }
  ```

- **Response (success):**
  ```json
  {
    "success": true,
    "spot": { ... },
    "script": "string",
    "images": ["image1.jpg", "image2.jpg"],
    "video": "video.mp4",
    "landing_page": "landing_page.html"
  }
  ```

- **Response (error):**
  ```json
  {
    "success": false,
    "error": "Error message"
  }
  ```

---

## Example Usage

```bash
curl -X POST http://localhost:8000/generate_microtour \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_secret_key" \
  -d '{"place_id": "ChIJd8BlQ2BZwokRAFUEcm_qrcA", "category": "cafe", "city": "طنجة"}'
```

---

## Notes

- All generated files (videos, images, landing pages) are saved in the frontend `pages/` directory.
- For production, restrict CORS and protect your API key.
- See the main README for deployment and environment setup.
