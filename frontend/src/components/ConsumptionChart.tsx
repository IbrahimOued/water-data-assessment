import { useEffect, useState } from "react";
import { getConsumption } from "../api/consumption";
import type { ConsumptionResponse, WaterPoint } from "../types/models";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer
} from "recharts";
import { getWaterPoints } from "../api/waterPoints";

interface ConsumptionExtended extends ConsumptionResponse {
  point_id?: number;
  point_name?: string;
}

export default function ConsumptionChart() {
  const [data, setData] = useState<ConsumptionExtended[]>([]);
  const [points, setPoints] = useState<WaterPoint[]>([]);
  const [selectedPoint, setSelectedPoint] = useState<number | null>(null);

  useEffect(() => {
    getConsumption().then((res) => {
      setData(res as ConsumptionExtended[]);
    });
    getWaterPoints().then(setPoints);
  }, []);

  // --- filter by selected water point ---
  const filteredData = data
    .filter(d => selectedPoint ? d.point_id === selectedPoint : true)
    .map(d => ({
      ...d,
      reading_date: new Date(d.reading_date).toLocaleDateString(),
    }));

  // --- KPIs ---
  const totalConsumption = filteredData.reduce((sum, d) => sum + (d.meter_index || 0), 0);
  const avgConsumption = filteredData.length > 0 ? (totalConsumption / filteredData.length).toFixed(2) : 0;
  const lastReading = filteredData.length > 0 ? filteredData[filteredData.length - 1].meter_index : "-";

  return (
    <div className="p-6 bg-white shadow-md rounded-2xl space-y-6">
      <h2 className="text-lg font-bold">Consumption Dashboard</h2>

      {/* ---- KPIs ---- */}
      <div className="grid grid-cols-3 gap-4">
        <div className="rounded-2xl shadow p-4 text-center bg-gray-50">
          <h3 className="text-sm text-gray-500">Total Consumption</h3>
          <p className="text-xl font-bold">{totalConsumption}</p>
        </div>
        <div className="rounded-2xl shadow p-4 text-center bg-gray-50">
          <h3 className="text-sm text-gray-500">Average Consumption</h3>
          <p className="text-xl font-bold">{avgConsumption}</p>
        </div>
        <div className="rounded-2xl shadow p-4 text-center bg-gray-50">
          <h3 className="text-sm text-gray-500">Last Reading</h3>
          <p className="text-xl font-bold">{lastReading}</p>
        </div>
      </div>

      {/* ---- Dropdown ---- */}
      <div>
        <select
          className="border rounded-lg p-2 mb-4"
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            setSelectedPoint(Number(e.target.value) || null)
          }
        >
          <option value="">All Water Points</option>
          {points.map((p) => (
            <option key={p.point_id} value={p.point_id}>
              {p.point_name} ({p.village})
            </option>
          ))}
        </select>
      </div>

      {/* ---- Chart ---- */}
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={filteredData}>
          <CartesianGrid strokeDasharray="3 3"/>
          <XAxis dataKey="reading_date"/>
          <YAxis/>
          <Tooltip/>
          <Line type="monotone" dataKey="meter_index" stroke="#2563eb" strokeWidth={2}/>
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
