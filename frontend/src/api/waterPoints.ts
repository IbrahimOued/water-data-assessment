import axiosClient from "./axiosClient";
import { type WaterPoint } from "../types/models";

export const getWaterPoints = async (): Promise<WaterPoint[]> => {
  const res = await axiosClient.get<WaterPoint[]>("/water_points");
  return res.data;
};
