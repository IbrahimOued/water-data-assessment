import axios from "axios";

const axiosClient = axios.create({
  // baseURL: import.meta.env.VITE_API_BASE_URL, // FastAPI backend
  baseURL: "http://localhost:8000",
});

export default axiosClient;
