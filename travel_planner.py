from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import logging
import requests
from openai import OpenAI
from dotenv import load_dotenv
from googleapiclient.discovery import build
import requests
import logging


# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

if not openai_api_key or not youtube_api_key:
    raise ValueError("Missing API Keys. Please set them in the .env file.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # ✅ Fixes CORS errors

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# System prompt for OpenAI
system_prompt = (
    "You are a travel assistant that provides users with the five most attractive places near their entered location. "
    "Additionally, you fetch the most-watched YouTube videos related to those attractions and display the cheapest available hotel near that location. "
    "Ensure that the responses are concise, informative, and visually engaging where applicable."
)

def clean_text(text):
    """Remove unwanted characters and extra spaces"""
    return re.sub(r"[\*\n]", "", text).strip()

def get_openai_response(prompt):
    """Fetch response from OpenAI API"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return None

def extract_attractions(response_text):
    """Extract valid tourist attractions while removing introductory text."""
    lines = response_text.split("\n")
    attractions = []
    
    for line in lines:
        if not line.strip() or line.lower().startswith(("certainly", "here are", "the top")):
            continue
        match = re.match(r"^\d*\.*\s*(.*?):\s*(.*)", line.strip())
        if match:
            attractions.append({
                "name": clean_text(match.group(1)),
                "description": clean_text(match.group(2))
            })
    return attractions

def get_location_coordinates(location):
    """Fetch latitude and longitude from OpenStreetMap API"""
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}"
        headers = {
            "User-Agent": "MyApp/1.0 (christinajayakody28@gmail.com)"  # ✅ Replace with your email
        }
        response = requests.get(url, headers=headers, timeout=5)  # ✅ Add headers
        response.raise_for_status()  # ✅ Raise error for bad responses

        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            return {
                "latitude": float(data[0].get("lat", 0)),
                "longitude": float(data[0].get("lon", 0))
            }
        else:
            logging.error(f"Location not found: {location}")
            return {"latitude": None, "longitude": None}
    except requests.RequestException as e:
        logging.error(f"Error fetching coordinates: {e}")
        return {"latitude": None, "longitude": None}


def get_tourist_attractions(location):
    """Get top 5 tourist attractions for a given location."""
    prompt = f"List only the top 5 tourist attractions near {location}. Provide each in 'Name: Description' format."
    response = get_openai_response(prompt)
    return extract_attractions(response) if response else []

def get_youtube_videos(query, location):
    """Fetch the most-watched YouTube video for a given query with location-based filtering"""
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
    search_query = f"{query} travel guide {location}"  # ✅ Improved search relevance
    request = youtube.search().list(
        q=search_query,
        part="snippet",
        type="video",
        order="viewCount",
        maxResults=1
    )
    response = request.execute()
    
    if response["items"]:
        video = response["items"][0]
        return {
            "title": video["snippet"]["title"],
            "link": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
            "thumbnail": video["snippet"]["thumbnails"]["high"]["url"]
        }
    return {"title": "No video found", "link": "", "thumbnail": ""}

def get_cheapest_hotel(location):
    """Get the cheapest hotel for a given location."""
    prompt = f"Provide only the name and price of the cheapest hotel in {location}. Format: 'Hotel Name - $Price per night'"
    response = get_openai_response(prompt)
    match = re.match(r'^(.*) - (\$\d+ per night)', response.strip()) if response else None
    return {"name": clean_text(match.group(1)), "price": clean_text(match.group(2))} if match else {"name": "N/A", "price": "N/A"}

@app.route("/destination", methods=["POST"])
def handle_input():
    """Handle user input and return attractions, YouTube videos, and hotels."""
    data = request.get_json(silent=True) or request.form
    user_input = data.get("userInput")
    
    if not user_input:
        return jsonify({"error": "No location provided"}), 400
    
    logging.info(f"Fetching top attractions for {user_input}...")
    places = get_tourist_attractions(user_input)
    if not places:
        return jsonify({"error": "Could not find attractions for the location"}), 404
    
    attractions_list = []
    for place in places:
        logging.info(f"Fetching coordinates for {place['name']} in {user_input}...")
        coords = get_location_coordinates(place["name"])

        logging.info(f"Fetching most-watched YouTube video for {place['name']} in {user_input}...")
        video_details = get_youtube_videos(place["name"], user_input)
        
        logging.info(f"Fetching cheapest hotel for {place['name']} in {user_input}...")
        hotel_details = get_cheapest_hotel(user_input)  # ✅ Using main location instead of attraction name
        
        attractions_list.append({
            "name": place["name"],
            "description": place["description"],
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "youtube_video": video_details,
            "cheapest_hotel": hotel_details
        })
    
    return jsonify(attractions_list)

if __name__ == "__main__":
    app.run(debug=True)
