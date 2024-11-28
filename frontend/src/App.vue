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
import { useRoute } from 'vue-router';

const authStore = useAuthStore();

const router = useRouter();

const route = useRoute();

function redirectToLogin() {
  router.push('/login');
};

function isSignUp(){
  return window.location.pathname == "/signup"
}

function redirectIfNotLoggedIn() {
  if (!authStore.isAuthenticated() && !isSignUp()) {
    redirectToLogin();
  }
};

onMounted(
  () => redirectIfNotLoggedIn()
)
</script>
