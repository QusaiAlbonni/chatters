// src/stores/authStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import axiosInstance from '../axios';
import { AxiosError, type AxiosResponse } from 'axios';

export const useAuthStore = defineStore('auth', () => {
  const authToken = ref(localStorage.getItem('authToken') || null);
  if (authToken.value) {
    axiosInstance.defaults.headers.common['Authorization'] = `Token ${authToken.value}`;
  }

  const isTokenExists = () => authToken.value !== null;
  const isAuthenticated = () => isTokenExists();


  const storeToken = (token: string) => {
    authToken.value = token;
    localStorage.setItem('authToken', token);
  };

  const clearToken = () => {
    authToken.value = null;
    localStorage.removeItem('authToken')
  };

  const fetchAuthToken = async (username: string, password: string) => {
    const response = await axiosInstance.post('/token/login/', {
      username,
      password,
    });
    const data = response.data;

    if (data.auth_token) {
      storeToken(data.auth_token);
      axiosInstance.defaults.headers.common['Authorization'] = `Token ${data.auth_token}`;
    } else {
      throw new Error(data.message || 'Authentication failed');
    }
  };

  const logoutUser = async () => {
    let token: string | null = authToken.value
    let response = await axiosInstance.post('/token/logout/',
      {
        headers: {
          'Authorization': token
        }
      }
    )
    axiosInstance.defaults.headers.common['Authorization'] = null;
    clearToken()
  }

  const createUser = async (username: string, password: string, avatar: File | null, email: string): Promise<AxiosResponse> => {
    let form = new FormData();
    form.append('username', username)
    form.append('password', password)
    form.append('email', email)

    if (avatar){
      form.append('avatar', avatar)
    }
    const response = await axiosInstance.post('/users/', form,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response;
  }

  return {
    authToken,
    isTokenExists,
    storeToken,
    fetchAuthToken,
    isAuthenticated,
    logoutUser,
    clearToken,
    createUser
  };
});
