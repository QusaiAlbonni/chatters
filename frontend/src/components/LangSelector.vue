<template>
  <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn
          color="primary"
          v-bind="props"
          @click="loadLangsIfEmpty()"
        >
          {{ transStore.lang }}
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in transStore.langs"
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

const transStore = useTransStore();

function selectLang(lang: string){
  transStore.switchLang(lang)
}
async function loadLangsIfEmpty(){
  if (transStore.langs.length == 0){
    await transStore.loadLangs();
  }
}
</script>
