<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>

import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore();

const router = useRouter();

function redirectToLogin() {
  router.push('/login');
};

function redirectToChat() {
  router.push('/chat');
}

function redirectIfNotLoggedIn() {
  if (!authStore.isAuthenticated()) {
    redirectToLogin();
  }
};

onMounted(
  () => redirectIfNotLoggedIn()
)
</script>
