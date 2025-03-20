from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from openai import OpenAI
from googleapiclient.discovery import build
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load API keys from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

openai_client = OpenAI(api_key=openai_api_key)

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=youtube_api_key)


def get_youtube_videos(destination, max_results=3):
    try:
        search_query = f"Top interesting travel places located in {destination}."
              #  search_query = f"Top tourist attractions in {destination} travel guide Suggest a list of interesting travel places located within a 100 km of {destination}."

        request = youtube.search().list(
            q=search_query,
            part="snippet",
            maxResults=max_results,
            order="viewCount",
            type="video"
        )
        response = request.execute()

        videos = [
            {
                "title": item["snippet"]["title"],
                "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }
            for item in response.get("items", [])
        ]

        return videos if videos else [{"title": "No video found", "link": "", "thumbnail": ""}]

    except Exception as e:
        return [{"error": f"Failed to fetch videos: {str(e)}"}]

# Function to generate itinerary
def get_itinerary(destination, num_days):
    system_prompt = f"""
    You are a travel assistant helping users plan their itinerary.
    When a user provides a destination and the number of days, generate a detailed travel plan with activities per day.
    Ensure the plan includes:
    - Must-visit landmarks
    - Local food suggestions
    - Cultural experiences
    - Travel tips
    
    Insted of words show some emoji in the itenary description
    """

    prompt = f"Provide a {num_days}-day itinerary for {destination}."
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

# API route to get travel itinerary and YouTube videos
@app.route('/get_itinerary', methods=['GET'])
def get_travel_itinerary():
    destination = request.args.get('destination')
    num_days = int(request.args.get('num_dates'))

    itinerary = get_itinerary(destination, num_days)
    videos = get_youtube_videos(destination)

    return jsonify({
        "itinerary": itinerary,
        "youtube_videos": videos
    })

if __name__ == '__main__':
    app.run(debug=True)
