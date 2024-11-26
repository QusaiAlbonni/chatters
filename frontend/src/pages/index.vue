<template>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() => {
  router.push('/chat')
})
</script>
