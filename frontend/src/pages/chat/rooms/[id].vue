<template>
  <LoadingSpinner v-if="loading" />
  <v-container v-else style="margin-bottom: 100px;">
    <v-row>
      <v-col class="d-flex justify-center py-6 text-disabled text-body-1 text-weigt-thin">The begining </v-col>
    </v-row>
    <v-row>
      <v-col style="padding: 0">
        <v-list :class="['bg-transparent', mdAndUp ? 'px-12' : '']">
          <v-list-item v-for="[index, message] of messages?.entries()" :key="message.pk" class="px-2">
            <v-col cols="12" :class="('d-flex px-0 ' + (message.isOwned(user?.id) ? 'justify-end' : 'justify-start'))"
              style="padding: 0px;">
              <v-avatar :image="showMessage(message, index) ? message.user?.avatar : ''"
                :class="['mx-2', message.isOwned(user?.id) ? 'order-2' : 'order-1',]"></v-avatar>

              <v-card :color="message.isOwned(user?.id) ? 'light-blue-darken-3' : 'dark'"
                :class="['text-color-white', mdAndDown ? 'mobile-card' : 'desktop-card', message.isOwned(user?.id) ? 'order-1' : 'order-2']">
                <v-card-text style="padding: 10px; padding-bottom: 0; padding-top: 5px;">
                  <div :class="{ 'truncate': !message.expanded }">
                    {{ message.translatedContent }}
                  </div>
                  <v-btn v-if="isMessageLong(message)" variant="plain" size="x-small" density="compact"
                    class="text-caption mt-1 pa-0 pb-3" @click="toggleMessage(message)">
                    {{ message.expanded ? 'show less' : 'show more' }}
                  </v-btn>
                </v-card-text>
                <div class="px-2 pb-2 text-caption" style="opacity: 0.6;">{{ new Date(message.created_at ||
                  Date.now()).toLocaleTimeString() }}</div>
              </v-card>
            </v-col>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>

    <v-row :class="['message-field', 'position-fixed', 'bg-grey-darken-4', mdAndDown ? 'w-100' : 'w-75']">
      <v-form class="w-100 d-flex justify-between" @submit.prevent="sendMessage()">
        <v-text-field v-model="messageContent" label="Type a message" hint="Press Enter to send" varient="flat"
          class="p-12" />
        <v-btn icon="mdi-send" class="mx-1" type="submit"></v-btn>
      </v-form>
    </v-row>
  </v-container>
</template>

<style scoped>
.truncate {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.mobile-card {
  max-width: 70%;
  border-radius: 13px;
}

.desktop-card {
  max-width: 40%;
  border-radius: 13px;
}

.message-field {
  position: fixed;
  left: 444;
  bottom: 0;
  right: auto;
  top: auto;
  z-index: 1000;
  padding: 12px;
}
</style>

<script lang="ts" setup>
import type { Message, Room, User } from '@/api/v1';
import { useApiStore } from '@/stores/api';
import { useRoute } from 'vue-router';
import { useWebSocketStore } from '@/stores/websocket';
import { useAppStore } from '@/stores/app';
import { ExpandableMessage } from '@/types/message';
import { useDisplay } from 'vuetify';

const route = useRoute();
const apiStore = useApiStore();
const webSocketStore = useWebSocketStore();
const appStore = useAppStore();

const { mobile, mdAndDown, mdAndUp } = useDisplay();

let roomId: string;

if ('id' in route.params) {
  roomId = route.params.id;
}

definePage({
  meta: {
    layout: 'chat'
  }
})

const loading = ref(true);
const user: Ref<User | null> = ref(null);
const room: Ref<Room | null> = ref(null);
const messages: Ref<ExpandableMessage[]> = ref([]);
const errorMessage: Ref<string> = ref("An error have occured")
const error: Ref<boolean> = ref(false)
const messageContent: Ref<string> = ref("");

let socket: Ref<WebSocket>;


function toggleMessage(message: any) {
  message.expanded = !message.expanded;
}

function isMessageLong(message: ExpandableMessage): boolean {
  return message.translatedContent.length > 100;
}

function transformMessage(message: any): ExpandableMessage {
  return new ExpandableMessage(
    message.content,
    message.pk,
    message.user,
    message.room,
    message.created_at,
    message.modified_at,
    false,
    message.language,
    message.translations
  );
}

function transformMessages(messages: Message[]): ExpandableMessage[] {
  let newMessages: ExpandableMessage[] = [];
  messages.forEach((element) => {
    let newMessage: ExpandableMessage = transformMessage(element);
    newMessages.push(newMessage);
  })
  return newMessages;
}

function showMessage(message: ExpandableMessage, index: number): boolean {
  return ((index === 0) || (messages.value[index - 1].user?.id !== message.user?.id));
}

async function scrollDown() {
  await nextTick();
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

function initSocket() {
  socket = ref(webSocketStore.createChatConnection((room.value?.pk || 1).toString()));
}

async function onConnectionSuccess() {
  loading.value = false;
  console.log('WS connection successful');
  await scrollDown();
}

function onConnectionClose() {
  error.value = true;
  console.log('closed');

}

function closeConnection() {
  if (socket)
    socket.value.close();
}

function onMessageReceived(event: any) {
  const data = JSON.parse(event.data);
  messages.value?.push(transformMessage(data.message))
  scrollDown();
}

function sendMessage() {
  socket.value.send(JSON.stringify({ message: messageContent.value }));
  messageContent.value = "";
}

async function deleteMessage(){

}

async function initChat() {
  loading.value = true;
  error.value = false;
  try {
    if ('id' in route.params)
      roomId = route.params.id;

    user.value = await apiStore.getUser();
    messages.value = transformMessages(await apiStore.fetchMessages(roomId));
    room.value = await apiStore.getRoom(parseInt(roomId));

    // WS CONNECTION
    initSocket();

    socket.value.onopen = onConnectionSuccess;
    socket.value.onclose = onConnectionClose;
    socket.value.onmessage = onMessageReceived;


  }
  catch (e: any) {
    errorMessage.value = e.message
    error.value = true
  }
}

onMounted(initChat)

watch(() => {
  if ('id' in route.params)
    return route.params.id
},
  async () => {
    await closeConnection();
    await initChat();
  })
</script>
