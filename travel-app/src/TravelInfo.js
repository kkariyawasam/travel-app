import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Input from "./components/ui/input";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "./TravelInfo.css";


const TravelInfo = () => {
    const [location, setLocation] = useState("");
    const [data, setData] = useState([]);
    const [coordinates, setCoordinates] = useState({ lat: 0, lng: 0 });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Custom Leaflet Marker Icon
    const customIcon = L.icon({
        iconUrl: "https://leafletjs.com/examples/custom-icons/leaf-red.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41]
    });

    const fetchData = async () => {
        if (!location) return;
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post("http://localhost:5000/destination", {
                userInput: location,
            });

            setData(response.data);

            // Assuming API returns lat/lng in response
            if (response.data.length > 0 && response.data[0].latitude && response.data[0].longitude) {
                setCoordinates({ lat: response.data[0].latitude, lng: response.data[0].longitude });
            } else {
                setError("Location data not found!");
            }
        } catch (err) {
            setError("Failed to fetch data. Try again!");
        }

        setLoading(false);
    };

    return (
        <motion.div
            className="flex flex-col items-center justify-center h-screen w-full text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
        >
            <h1 className="text-3xl font-bold mb-4 flex items-center gap-2">🌍 Travel Assistant</h1>
            <motion.div className="flex gap-2" whileHover={{ scale: 1.05 }}>
                <Input
                    type="text"
                    placeholder="Where do you want to go?..."
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="shadow-lg"
                />
                <motion.button
                    onClick={fetchData}
                    className="bg-blue-500 text-white px-4 py-2 rounded-md"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Search
                </motion.button>
            </motion.div>

            {loading && <motion.div className="animate-spin mx-auto">⏳</motion.div>}
            {error && <p className="text-red-500">{error}</p>}

            <motion.div
                className="grid gap-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.8 }}
            >
                {data.map((place, index) => (
                    <motion.div
                        key={index}
                        className="p-4 shadow-lg rounded-lg bg-white"
                        whileHover={{ scale: 1.05 }}
                    >
                        <h2 className="text-xl font-bold">{place.name}</h2>
                        <p className="text-gray-601">{place.description}</p>
                        {place.youtube_video && (
                            <div className="mt-2">
                                <a href={place.youtube_video.link} target="_blank" rel="noreferrer">
                                    <motion.img
                                        src={place.youtube_video.thumbnail}
                                        alt={place.youtube_video.title}
                                        className="rounded-lg shadow-md"
                                        whileHover={{ scale: 1.1 }}
                                    />
                                </a>
                            </div>
                        )}
                        {place.cheapest_hotel && (
                            <p className="mt-2 text-sm text-gray-700">
                                Cheapest Hotel: <strong>{place.cheapest_hotel.name}</strong> - {place.cheapest_hotel.price}
                            </p>
                        )}
                    </motion.div>
                ))}
            </motion.div>

            {/* Render Map Only If Coordinates Are Set */}
            {coordinates.lat !== 0 && coordinates.lng !== 0 && (
                <MapContainer center={[coordinates.lat, coordinates.lng]} zoom={10} className="h-96 w-full mt-6">
                    <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                    <Marker position={[coordinates.lat, coordinates.lng]} icon={customIcon}>
                        <Popup>{location}</Popup>
                    </Marker>
                </MapContainer>
            )}
        </motion.div>
    );
};

export default TravelInfo;

