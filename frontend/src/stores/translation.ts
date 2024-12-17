// src/stores/authStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Language } from '@/types/translation';
export const useTransStore = defineStore('translation', () => {
  const langs: Language[] = ['en', 'nl', 'de', 'ar', 'jp']

  const currentLang: Language = localStorage.getItem('lang') as Language

  const lang: Ref<Language> = ref(currentLang || 'en');

  const switchLang = (language: Language) => {
    lang.value = language;
    localStorage.setItem('lang', language);
    window.location.reload();
  };

  return {
    lang,
    langs,
    switchLang
  }
}
)
