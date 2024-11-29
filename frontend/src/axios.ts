import axios from 'axios';
import { useAppStore } from './stores/app';

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
    if (error.status === 401){
      localStorage.removeItem("authToken");
      const appStore = useAppStore();
      appStore.errorSnackBar.message = "Something went wrong please login";
      appStore.errorSnackBar.visible = true;
      window.location.href = '/login';
    }
    throw error;
  }
)

export default axiosInstance;
