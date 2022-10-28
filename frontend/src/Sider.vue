<template>
    <n-drawer v-if="mobile" :show="drawer" @update:show="toggle" :width="siderWidth" placement="left"
        style="top: var(--header-height); background-color: var(--dark-gray);" :z-index="8">
        <n-drawer-content>
            <router-link @click="toggle" to="/">Fome</router-link>
            <router-link @click="toggle" to="/about">About</router-link>
        </n-drawer-content>
    </n-drawer>
    <n-layout-sider v-else :native-scrollbar="false" content-style="padding: 24px;" bordered :width="menuWidth">
        <router-link to="/">Fome</router-link>
        <router-link to="/about">About</router-link>
    </n-layout-sider>
</template>
<script setup>
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'
const emit = defineEmits(['update:drawer'])
const {siderWidth, drawer} = defineProps({
    siderWidth: {},
    drawer: Boolean
})

const toggle = (e) => {
    emit('update:drawer', drawer)
} 

const breakpoints = useBreakpoints(breakpointsTailwind)
const mobile = breakpoints.smallerOrEqual('2xl')
</script>