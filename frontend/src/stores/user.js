import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {

  function getPayload(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload)
  }

  const username = ref('')
  const sid = ref('')
  const accessToken = useStorage('access_token', "")
  const refreshToken = useStorage('refresh_token', "")
  const router = useRouter()

  function initUserFromTokens(at, rt) {
    accessToken.value = at
    refreshToken.value = rt
    let payload = getPayload(at)
    username.value = payload.sub;
    sid.value = payload.sid;
  }

  function clearUser() {
    accessToken.value = ""
    refreshToken.value = ""
    checkUser()
  }

  function checkUser() {
    if (accessToken.value != "" && refreshToken.value != "") {
      initUserFromTokens(accessToken.value, refreshToken.value)
    }
    else {
      router.push({ name: 'signin' })
      username.value = "";
      sid.value = "";
    }
  }

  function hasUser() {
    return username.value != '';
  }

  checkUser()
  return { username, sid, hasUser, initUserFromTokens, clearUser }
})
