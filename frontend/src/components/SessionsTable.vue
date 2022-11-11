<template>
  <n-table>
    <thead>
      <tr>
        <th>Last Updated</th>
        <th>Device</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="sessionData.length" v-for="session in sessionData" :class="{ highlight: session.sid == userStore.sid }">
        <td>
          {{moment(session.last_updated).fromNow()}}
        </td>
        <td>{{ session.user_agent }}</td>
        <td>
          <div style="display: flex; justify-content: center; text-align: center;">
            <n-button v-if="session.sid != userStore.sid" quaternary circle type="error"
              @click="$emit('terminate', session.sid)">
              <template #icon>
                <n-icon>
                  <DeleteForeverFilled />
                </n-icon>
              </template>
            </n-button>
            <span v-else>Current session</span>
          </div>
        </td>
      </tr>
      <tr v-else>
        <td colspan="3">
          <n-empty description="No Session Data" />
        </td>
      </tr>
    </tbody>
  </n-table>
</template>

<script setup>
import { NButton, NIcon } from "naive-ui";
import { DeleteForeverFilled } from '@vicons/material'
import moment from 'moment';

import { useUserStore } from '@/stores/user'


const { sessionData } = defineProps(['sessionData'])

const userStore = useUserStore()
</script>