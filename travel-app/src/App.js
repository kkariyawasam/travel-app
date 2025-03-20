import React, { useState } from "react";
import axios from "axios";
import './App.css';

const YouTubeSidebar = ({ videos }) => {
  return (
    <div className="sidebar">
      <h2>Recommended Videos</h2>
      <div className="video-list">
        {videos.length === 0 ? (
          <p className="text-center">No videos available</p>
        ) : (
          videos.map((video, index) => (
            <a
              key={index}
              href={video.link}
              target="_blank"
              rel="noopener noreferrer"
              className="video-item"
            >
              <img
                src={video.thumbnail}
                alt={video.title}
                className="video-thumbnail"
              />
              <p>{video.title}</p>
            </a>
          ))
        )}
      </div>
    </div>
  );
};

function App() {
  const [destination, setDestination] = useState("");
  const [numDates, setNumDates] = useState(1);
  const [itinerary, setItinerary] = useState("");
  const [loading, setLoading] = useState(false);
  const [videos, setVideos] = useState([]);

  const fetchItinerary = async () => {
    setLoading(true);
    setVideos([]);
    try {
      const response = await axios.get("http://localhost:5000/get_itinerary", {
        params: { destination, num_dates: numDates },
      });

      setItinerary(response.data.itinerary);
      setVideos(response.data.youtube_videos);
    } catch (error) {
      console.error("Error fetching itinerary:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {/* Left Sidebar - YouTube Videos */}
      <div className="left-column">
        <YouTubeSidebar videos={videos} />
      </div>

      {/* Right Column - Itinerary Display */}
      <div className="right-column">
        <h1>Travel Itinerary Generator</h1>

        <div className="input-container">
          {/* Destination Input */}
          <div className="input-group">
            <label>Enter Destination:</label>
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              placeholder="Enter destination"
            />
          </div>

          {/* Number of Days Input */}
          <div className="input-group">
            <label>Number of Days:</label>
            <input
              type="number"
              value={numDates}
              onChange={(e) => setNumDates(Number(e.target.value))}
              min="1"
            />
          </div>

          {/* Button to Fetch Itinerary */}
          <div className="button-container">
            <button
              onClick={fetchItinerary}
              disabled={loading}
            >
              {loading ? "Loading..." : "Get Itinerary"}
            </button>
          </div>
        </div>

        {/* Itinerary Display */}
        <div className="itinerary-container">
          <h2>Itinerary</h2>
          {itinerary.split("Day ").map((section, index) => {
            if (!section.trim()) return null;

            const parts = section.split(":");
            const title = parts[0] ? `Day ${parts[0]}` : "";
            const content = parts.slice(1).join(":").split(". ");

            return (
              <div key={index} className="itinerary-day">
                {title && <h3>{title}</h3>}
                <ul>
                  {content.map((sentence, idx) =>
                    sentence.trim() ? <li key={idx}>{sentence.trim()}.</li> : null
                  )}
                </ul>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default App;