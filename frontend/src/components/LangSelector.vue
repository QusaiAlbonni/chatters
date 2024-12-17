<template>
  <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn
          color="primary"
          v-bind="props"
        >
          {{ transStore.lang }}
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          :value="item"
          @click="selectLang(item)"
        >
          <v-list-item-title>{{ item }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
</template>

<script lang="ts" setup>
import { useTransStore } from '@/stores/translation';
import type { Language } from '@/types/translation';

const transStore = useTransStore();

const items = transStore.langs;

function selectLang(lang: Language){
  transStore.switchLang(lang)
}
</script>
