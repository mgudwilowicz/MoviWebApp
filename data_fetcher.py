import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="
HEADERS = {"Content-Type": "application/json"}


def fetch_movie(title):
    """Fetch movie info from OMDb API by title. Returns dict or None."""
    response = requests.get(BASE_URL + title, headers=HEADERS)
    data = response.json()
    if data.get("Response") == "False":
        return None
    return {
        "name": data.get("Title"),
        "director": data.get("Director"),
        "year": data.get("Released"),
        "poster_url": data.get("Poster"),
    }
