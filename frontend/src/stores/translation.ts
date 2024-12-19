// src/stores/authStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Language } from '@/types/translation';
import { ChatApi } from '@/api/v1';
import { useApiStore } from './api';

export const useTransStore = defineStore('translation', () => {
  const langs: Ref<string[]> = ref([])

  const apiStore = useApiStore();

  const currentLang: string = localStorage.getItem('lang') as string

  const lang: Ref<string> = ref(currentLang || 'en');

  const switchLang = (language: string) => {
    lang.value = language;
    localStorage.setItem('lang', language);
    window.location.reload();
  };

  const loadLangs = async () => {
    const languages: Language[] = await apiStore.getLangs();
    const tempLangs: string[] = [];
    for (let language of languages){
      tempLangs.push(language.code);
    }
    langs.value = tempLangs;

  }

  return {
    lang,
    langs,
    switchLang,
    loadLangs
  }
}
)
