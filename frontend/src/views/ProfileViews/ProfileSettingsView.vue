<template>
  <n-card>
    <n-tabs type="line" animated>
      <n-tab-pane name="sessions" :tab="renderTextBadge('Sessions', sessionData.length)">
        <!-- <n-button @click="getSessions">Refresh</n-button> -->
        <SessionsTable :sessionData="sessionData" @terminate="wTerminateUserSession" />
      </n-tab-pane>
      <n-tab-pane name="tags" tab="Tags">
        Тут будет глобальная настройка тэгов
      </n-tab-pane>
      <n-tab-pane name="security" tab="Security">
        Тут будет сброс пароля
      </n-tab-pane>
    </n-tabs>
  </n-card>
</template>

<script setup>
import { ref } from 'vue';
import { useMessage } from 'naive-ui'

import SessionsTable from '@/components/SessionsTable.vue'
import { getUserSessions, terminateUserSession } from '@/utils/api'
import { apiWrapper } from '@/utils/apiWrapper.js'
import { renderTextBadge } from '@/utils/textBadge'


const sessionData = ref([])
const apiw = apiWrapper()


function wGetSessions() {
  apiw.wrap(() => getUserSessions(), (content) => { sessionData.value = content })
}
function wTerminateUserSession(sid) {
  apiw.wrap(() => terminateUserSession(sid), (content) => { wGetSessions() })
}

wGetSessions()
</script>

<style scoped>
:deep(.highlight td) {
  background-color: rgba(90, 207, 168, 0.37) !important;
}
</style>