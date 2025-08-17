import { useEffect, useState } from "react";
import { getConsumption } from "../api/consumption";
import type { ConsumptionResponse } from "../types/models";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer
} from "recharts";

export default function ConsumptionChart() {
  const [data, setData] = useState<ConsumptionResponse[]>([]);

  useEffect(() => {
    getConsumption().then(setData);
    console.log("Fetched consumption data:", data);
    
  }, []);

  return (
    <div className="p-4 bg-white shadow-md rounded-2xl">
      <h2 className="text-lg font-bold mb-2">Consumption Over Time</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3"/>
          <XAxis dataKey="reading_date"/>
          <YAxis/>
          <Tooltip/>
          <Line type="monotone" dataKey="meter_index" stroke="#8884d8"/>
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
