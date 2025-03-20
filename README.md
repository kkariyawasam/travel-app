# Travel Assistant

## Overview

This project is a Travel Itinerary Generator that helps users plan their trips by generating a detailed itinerary for a given destination and number of days. It also provides recommended YouTube videos related to the destination for additional travel inspiration.

## UI preview

<img width="943" alt="image" src="https://github.com/user-attachments/assets/f953ce5b-306c-4d87-b4cd-bb6a380ab85b" />


## Features

Itinerary Generation: Generates a detailed travel plan for a specified destination and number of days using OpenAI's GPT-4.
YouTube Integration: Fetches relevant YouTube videos for the destination using the YouTube Data API.
User-Friendly UI: A React-based frontend for easy interaction and display of the itinerary and videos.

## Technologies Used

Backend: Flask (Python)
Frontend: React (JavaScript)

APIs:
OpenAI API (GPT-4 for itinerary generation)
YouTube Data API (for fetching videos)

Other Libraries:
dotenv for environment variable management
flask_cors for enabling CORS in the backend
axios for making API calls from the frontend
