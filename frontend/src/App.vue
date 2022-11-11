<template>
    <n-layout style="height: 100vh;">
        <Header v-if="userStore.hasUser()" v-model:drawer="drawer"/>
        <n-layout position="absolute" has-sider class="container" :style="{top: userStore.hasUser() ? 'var(--header-height)' : '0'}">
            <Sider v-if="userStore.hasUser()" v-model:drawer="drawer" :width="siderWidth" />
            <n-layout content-style="padding: 24px;" :native-scrollbar="false">
                <router-view />
            </n-layout>
        </n-layout>
    </n-layout>
</template>

<script setup>
import Header from '@/Header.vue'
import Sider from '@/Sider.vue'
import { ref } from 'vue';
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
const drawer = ref(false)
const siderWidth = ref(300)
</script>

<style scoped>
</style>