import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useKekerStore = defineStore('keker', () => {
  const tokenus = ref("sss")
  function setToken(token) {
    tokenus.value = token
  }

  
  return { setToken, tokenus }
})
