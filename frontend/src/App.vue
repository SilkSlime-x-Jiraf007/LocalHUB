<template>
    <n-layout style="height: 100vh;">
        <Header v-if="userStore.hasUser()" v-model:drawer="drawer" titleSuffix="Test" />
        <n-layout position="absolute" has-sider class="container">
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
.container {
    top: var(--header-height);
}
</style>