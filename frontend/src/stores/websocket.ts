import { defineStore } from "pinia";
import { useAuthStore } from "./auth";

export const useWebSocketStore = defineStore('websocket', () => {
  const authStore = useAuthStore();

  const createChatConnection = (roomName: string) : WebSocket => {
    return new WebSocket(`${import.meta.env.VITE_WS_HOST}/ws/chat/${roomName}/?token=${authStore.authToken}`)
  }

  return {
    createChatConnection
  }
})
