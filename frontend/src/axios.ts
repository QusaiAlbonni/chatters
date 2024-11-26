import axios from 'axios';

const API_HOST = import.meta.env.VITE_API_HOST;

const axiosInstance = axios.create({
  baseURL: API_HOST + "/api/v1",
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosInstance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    console.error("an Error occured");
    localStorage.removeItem("authToken");
    window.location.href = '/login'
  }
)

export default axiosInstance;
