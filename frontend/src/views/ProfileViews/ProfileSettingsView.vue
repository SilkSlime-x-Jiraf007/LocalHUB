<template>
  <n-card>
    <n-tabs type="line" animated>
      <n-tab-pane name="sessions" :tab="`Sessions (${sessionData.length})`">
        <!-- <n-button @click="getSessions">Refresh</n-button> -->
        <SessionsTable :sessionData="sessionData" @terminate="terminateSession" />
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


const sessionData = ref([])
const messager = useMessage()
const apiw = apiWrapper()


async function getSessions() {
  const content = await apiw.wrap(() => getUserSessions())
  sessionData.value = content
}
async function terminateSession(sid) {
  await apiw.wrap(() => terminateUserSession(sid))
  await getSessions()
}

getSessions()
</script>

<style scoped>
:deep(.highlight td) {
  background-color: rgba(90, 207, 168, 0.37) !important;
}
</style>