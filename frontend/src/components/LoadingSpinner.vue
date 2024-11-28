<template>
  <div class="loading-overlay">
    <v-card class="loading-card" elevation="8">
      <!-- Spinner circles -->
      <div class="spinner-container">
        <div class="spinner-outer"></div>
        <div class="spinner-inner"></div>
      </div>
      <!-- Pulse bars -->
      <div class="pulse-container">
        <div class="pulse-bar-long"></div>
        <div class="pulse-bar-short"></div>
      </div>
    </v-card>
  </div>
</template>

<script setup>
// No logic needed for this component
</script>

<style scoped>
.loading-overlay {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-card {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background: black;
  border-radius: 8px;
}

.spinner-container {
  position: relative;
  width: 64px;
  height: 64px;
}

.spinner-outer {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 4px solid rgb(229, 241, 255);
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
}

.spinner-inner {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 4px solid rgb(59, 130, 246);
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
}

.pulse-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.pulse-bar-long {
  width: 96px;
  height: 8px;
  background: rgb(229, 241, 255);
  border-radius: 4px;
  animation: pulse 1.5s ease-in-out infinite;
}

.pulse-bar-short {
  width: 64px;
  height: 8px;
  background: rgb(229, 241, 255);
  border-radius: 4px;
  animation: pulse 1.5s ease-in-out infinite;
  animation-delay: 0.2s;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>


