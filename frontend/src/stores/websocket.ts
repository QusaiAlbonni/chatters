import { defineStore } from "pinia";
import { useAuthStore } from "./auth";
import { useTransStore } from "./translation";

export const useWebSocketStore = defineStore('websocket', () => {
  const authStore = useAuthStore();
  const transStore = useTransStore();

  const createChatConnection = (roomId: string, language: string = transStore.lang) : WebSocket => {
    return new WebSocket(`${import.meta.env.VITE_WS_HOST}/ws/chat/${roomId}/?token=${authStore.authToken}&lang=${language}`)
  }

  return {
    createChatConnection
  }
})
