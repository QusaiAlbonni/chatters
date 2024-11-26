import { defineStore } from "pinia";
import { ChatApi, UsersApi, type Message, type Room, type User } from '@/api/v1/Api'
import axiosInstance from '@/axios'

export const useApiStore =  defineStore('api', () => {
  const chatApi = new ChatApi(undefined, undefined, axiosInstance);
  const userApi = new UsersApi(undefined, undefined, axiosInstance);

  const fetchRooms = async () : Promise<Room[]> => {
    let rooms: Room[] = (await chatApi.chatRoomsList()).data;
    return rooms;
  };

  const fetchMessages = async (roomId: string) : Promise<Message[]> => {
    let messages = (await chatApi.chatRoomsMessagesList(roomId)).data
    return messages;
  };

  const getUser = async () : Promise<User> => {
    return (await userApi.usersMeRead()).data;
  };

  const getRoom = async (id: number) : Promise<Room> => {
    return (await chatApi.chatRoomsRead(id)).data
  };

  return {
    fetchRooms,
    fetchMessages,
    getUser,
    getRoom
  };
});
