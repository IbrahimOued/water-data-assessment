import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { type LatLngExpression } from "leaflet";  
import { getWaterPoints } from "../api/waterPoints";
import { type WaterPoint } from "../types/models";
import "leaflet/dist/leaflet.css";

// 👇 Fix for missing marker icons in Vite/React builds
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

// Override the default icon
L.Marker.prototype.options.icon = L.icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41],
});

export default function WaterPointsMap() {
  const [points, setPoints] = useState<WaterPoint[]>([]);

  useEffect(() => {
    getWaterPoints().then(setPoints);
  }, []);

  const center: LatLngExpression = [12.0, -1.5];

  return (
    <div className="p-4 bg-white shadow-md rounded-2xl">
      <h2 className="text-lg font-bold mb-2">Water Points</h2>
      <MapContainer center={center} zoom={7} style={{ height: "400px", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
        {points.map((p) => (
          <Marker key={p.point_id} position={[p.latitude, p.longitude] as LatLngExpression}>
            <Popup>
              <b>{p.point_name}</b><br/>
              {p.village}, {p.commune}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
