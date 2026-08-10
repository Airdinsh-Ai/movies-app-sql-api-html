import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")

OMDB_URL = "http://www.omdbapi.com/"


class MovieNotFoundError(Exception):
    """Raised when the OMDb API has no movie matching the given title."""


def fetch_movie(title):
    """Fetches details for a movie title from the OMDb API.

    Returns a dict with year, rating, poster_url, imdb_id and country.
    """
    try:
        response = requests.get(
            OMDB_URL, params={"apikey": API_KEY, "t": title}, timeout=10
        )
    except requests.exceptions.RequestException as error:
        raise ConnectionError("Could not connect to the OMDb API.") from error

    data = response.json()
    if data.get("Response") == "False":
        raise MovieNotFoundError(data.get("Error", f"Movie '{title}' not found."))

    year_text = "".join(char for char in data.get("Year", "") if char.isdigit())[:4]
    rating_text = data.get("imdbRating", "N/A")
    poster = data.get("Poster", "N/A")
    imdb_id = data.get("imdbID", "N/A")
    country = data.get("Country", "N/A")

    return {
        "year": int(year_text) if year_text else 0,
        "rating": float(rating_text) if rating_text != "N/A" else 0.0,
        "poster_url": poster if poster != "N/A" else None,
        "imdb_id": imdb_id if imdb_id != "N/A" else None,
        "country": country.split(",")[0].strip() if country != "N/A" else None,
    }
