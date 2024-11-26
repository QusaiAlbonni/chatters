<template>
  <v-navigation-drawer :temporary="mdAndDown" :permanent="mdAndUp" :floating="mdAndDown" v-model="appStore.drawer" class="position-fixed">
    <v-skeleton-loader v-if="loading" v-for="i in 9" type="list-item-two-line"></v-skeleton-loader>
    <v-alert v-else-if="errorOccured" type="error" icon="mdi-wifi-off" closable color="">
      {{ error }}
    </v-alert>
    <v-list v-else nav>
      <v-list-item v-for="room in rooms" prepend-icon="mdi-pound" :title="room.name" :value="room.pk"
        :to="{ name: '/chat/rooms/[id]', params: { id: room.pk || 0 }, }" link></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import type { Room } from '@/api/v1';
import { useApiStore } from '@/stores/api';
import { useAppStore } from '@/stores/app';
import { useDisplay } from 'vuetify'

const { mobile, mdAndDown, smAndDown, mdAndUp } = useDisplay();

const appStore = useAppStore();
const apiStore = useApiStore();

const loading = ref<boolean>(true);
const rooms = ref<Room[]>([]);
const error = ref<Error | null>(null);
const errorOccured = ref<boolean>(false);

if (mdAndUp.value) {
  appStore.toggleDrawer();
}

onMounted(async () => {
  try {
    rooms.value = await apiStore.fetchRooms();
    loading.value = false;
  }
  catch (e : any) {
    loading.value = false;
    errorOccured.value = true;
    error.value = e.message;
  }
})
</script>
