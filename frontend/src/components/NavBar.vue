<template>
  <v-app-bar density="default" class="position-fixed">
    <v-avatar image="../assets/logo.svg" class="ml-4" />
    <v-app-bar-title>
      <v-btn href="/" class="font-weight-bold px-0" density="comfortable"> Chatters </v-btn>
      <v-btn icon="mdi-menu" v-if="inChat && mdAndDown" @click="appStore.toggleDrawer()"> </v-btn>
    </v-app-bar-title>
    <LangSelector v-if="authStore.isAuthenticated()"></LangSelector>
    <v-btn v-if="authStore.isAuthenticated()" varient="outlined" color="red" @click="logout()">logout</v-btn>
    <v-btn v-else-if="!isLoginPage" href="/login">login</v-btn>
  </v-app-bar>

  <v-snackbar :timeout="2000" color="deep-purple-accent-4" elevation="24" v-model="snackbar.visible">
    {{ snackbar.message }}
  </v-snackbar>

</template>
<script lang="ts" setup>

import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { useDisplay } from 'vuetify'

const { mobile, mdAndDown, smAndDown } = useDisplay()

const appStore = useAppStore()

const snackbar = appStore.errorSnackBar

const authStore = useAuthStore()
const route = useRoute()
const isLoginPage = route.name === '/login';


const inChat = ref(route.path.startsWith("/chat"))

const router = useRouter()

async function logout() {
  try {
    await authStore.logoutUser()
    router.push("/login")
  }
  catch (error) {
    snackbar.visible = true
    snackbar.message = "could not logout"
  }
}


</script>
