// Utilities
import { defineStore } from 'pinia'
import { reactive, ref } from 'vue'

export const useAppStore = defineStore('app', (helpers) => {
  const errorSnackBar = reactive({
    visible: false,
    message: "An Error Have occured"
  })

  const drawer = ref(false)

  function toggleDrawer(){
    drawer.value = !drawer.value
  }

  return {
    errorSnackBar,
    drawer,
    toggleDrawer
  }
})
