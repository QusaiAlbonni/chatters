<template>
  <LoginForm></LoginForm>
</template>
<script lang="ts" setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  if (authStore.isAuthenticated()){
    if (window.history.length > 1)
      router.back()
    else {
      router.push("/")
    }
  }
})
</script>
