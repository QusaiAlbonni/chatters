<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" class="text-center">
        <div class="text-h1 font-weight-bold mb-4">
          404
        </div>
        <div :class="mdAndDown? 'text-h6 mb-4' : 'text-h4 mb-4'">
          Oops! Page Not Found
        </div>
        <v-card-text class="text-body-1 mb-6 text-disabled">
          We couldn't find the page you're looking for
        </v-card-text>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts" setup>
import { useDisplay } from 'vuetify';

const { mdAndDown, mobile } = useDisplay();

definePage({
  meta: {
    layout: 'default'
  }
})
</script>
