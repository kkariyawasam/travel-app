# Travel Assistant

## Overview

Travel Assistant is a full-stack application that helps users discover top tourist attractions, view related YouTube videos, and find the cheapest hotels for a given location. The backend is built using Flask, OpenAI API, and YouTube Data API, while the frontend is developed with React and Framer Motion for animations.

## UI preview

## Features

- Retrieve the top 5 tourist attractions for a specified location.
- Fetch the most-watched YouTube video related to each attraction.
- Find the cheapest available hotel in the location.
- User-friendly React-based frontend with animations.
- API-powered responses for reliable travel recommendations.

## Technologies Used

### Backend (Flask)

- Python
- Flask
- OpenAI API
- YouTube Data API
- Flask-CORS

### Frontend (React)

- React
- Framer Motion (animations)
- Axios (HTTP requests)
- Tailwind CSS (styling)

## Usage

1. Open the frontend in your browser (usually at `http://localhost:3000`).
2. Enter a location in the search bar and click "Search".
3. View the top 5 attractions along with their descriptions.
4. Watch related YouTube videos by clicking on the thumbnails.
5. Check the cheapest available hotel in the selected location.

## API Endpoints

### `POST /destination`

**Request:**

```json
{
  "userInput": "Paris"
}
```

**Response:**

```json
[
  {
    "name": "Eiffel Tower",
    "description": "A world-famous iron lattice tower in Paris.",
    "youtube_video": {
      "title": "Eiffel Tower Travel Guide",
      "link": "https://www.youtube.com/watch?v=example",
      "thumbnail": "https://img.youtube.com/example.jpg"
    },
    "cheapest_hotel": {
      "name": "Hotel Paris",
      "price": "$100 per night"
    }
  }
]
```

## Future Improvements

- Integrate Google Places API for more accurate hotel pricing.
- Add user authentication to save favorite destinations.
- Improve UI with interactive maps.
