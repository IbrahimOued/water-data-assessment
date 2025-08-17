import axiosClient from "./axiosClient";
import { type ConsumptionResponse } from "../types/models";

export const getConsumption = async (): Promise<ConsumptionResponse[]> => {
  const res = await axiosClient.get<ConsumptionResponse[]>("/consumption");
  return res.data;
};
