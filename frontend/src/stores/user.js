import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

function getPayload(token) {
  try {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload)
  } catch (err) {
  }
  return null
}

export const useUserStore = defineStore('user', () => {

  const accessToken = useStorage('access_token', "")
  const refreshToken = useStorage('refresh_token', "")

  const username = computed(() => {
    let payload = getPayload(refreshToken.value)
    if (payload) return payload.sub
    else return ""
  })
  const sid = computed(() => {
    let payload = getPayload(refreshToken.value)
    if (payload) return payload.sid
    else return ""
  })

  function hasUser() {
    return username.value != '';
  }

  function clearUser() {
    accessToken.value = ""
    refreshToken.value = ""
  }

  function setTokens(at, rt) {
    accessToken.value = at
    refreshToken.value = rt
  }

  return { setTokens, username, sid, hasUser, clearUser }
})
