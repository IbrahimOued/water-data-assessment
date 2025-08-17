import ConsumptionChart from "../components/ConsumptionChart";
import WaterPointsMap from "../components/WaterPointsMap";

export default function Dashboard() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
      <ConsumptionChart />
      <WaterPointsMap />
    </div>
  );
}
