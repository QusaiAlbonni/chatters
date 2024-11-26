<template>
  <v-container class="fill-height px-1" fluid>
    <v-row justify="center" class="text-center">
      <v-col cols="12" md="6" class="text-center">
        <!-- Image -->
        <div class="d-flex justify-center">
          <v-img src="../../assets/logo.svg" alt="Placeholder Image" max-width="150" class="d-flex justify-center mb-4" />
        </div>
        <!-- Text -->
        <div :class="mdAndDown? 'text-h5' : 'text-h3'">
          <strong>Let's start Chatting!</strong>
        </div>
        <div class="text-disabled">
          Click on one of the rooms on the left and start Chatting!
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { useDisplay } from 'vuetify';

const { mdAndDown } = useDisplay();

definePage({
  meta: {
    layout: 'chat'
  }
})

</script>
