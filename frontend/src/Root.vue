<template>
    <n-config-provider :theme="darkTheme">
        <n-message-provider>
            <n-dialog-provider>
                <App />
            </n-dialog-provider>
        </n-message-provider>
    </n-config-provider>
  </template>
  
  <script setup>
  import { darkTheme } from 'naive-ui'
  import App from '@/App.vue'
  </script>