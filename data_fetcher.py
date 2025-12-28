import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

url = f"http://www.omdbapi.com/?apikey={api_key}&t="

headers = {
    "Content-Type": "application/json"
}



def fetch_movie(movie):
    response = requests.get(url + movie, headers=headers)
    data = response.json()

    return {'name': data['Title'], 'director': data['Director'], 'year': data['Released'], 'poster_url': data['Poster']}

