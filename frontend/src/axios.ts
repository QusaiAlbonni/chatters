import axios from 'axios';

const API_HOST = import.meta.env.VITE_API_HOST;

const axiosInstance = axios.create({
  baseURL: API_HOST + "/api/v1",
  headers: {
    'Content-Type': 'application/json',
  },
});


export default axiosInstance;
