<template>
    <n-layout-header bordered class="nav" style="box-shadow: var(--shadow);">
        <n-button v-if="mobile" @click="$emit('update:drawer', !drawer)" quaternary circle>
            <template #icon>
                <n-icon>
                    <MenuRound />
                </n-icon>
            </template>
        </n-button>
        <n-text tag="div" class="ui-logo" :depth="1">
            <img height="32px" src="@/assets/logo.svg">
            <span>LocalHUB{{ route.name ? ` | ${route.name}` : "" }}</span>
        </n-text>
        <div style="flex-grow: 10;" />
        <n-divider vertical />
        <n-dropdown v-if="userStore.username != ''" :options="userOptions" placement="bottom-end" trigger="click"
            @select="handleSelect">
            <n-button :quaternary="!mobileMini" size="large" :text="mobileMini">
                <n-space justify="space-between" align="center">
                    <Avatar :username='userStore.username' />
                    <span v-if="!mobileMini">{{ userStore.username }}</span>
                </n-space>
            </n-button>
        </n-dropdown>
        <n-button v-else size="large">
            Sign In
        </n-button>
    </n-layout-header>
</template>
<script setup>
import { h } from 'vue';
import { useRouter, useRoute } from 'vue-router'
import { NIcon } from "naive-ui";
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'
import { PersonOutlineOutlined, SettingsRound, LogOutOutlined, MenuRound } from "@vicons/material";

import { useUserStore } from '@/stores/user'
import { getUserSessions, terminateUserSession } from '@/utils/api'
import Avatar from '@/components/Avatar.vue'

const { drawer } = defineProps(['drawer'])

const breakpoints = useBreakpoints(breakpointsTailwind)
const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const mobileMini = breakpoints.smallerOrEqual('md')
const mobile = breakpoints.smallerOrEqual('2xl')


const renderIcon = (icon) => {
    return () => {
        return h(NIcon, null, {
            default: () => h(icon)
        });
    };
};

const userOptions = [
    {
        label: "Profile",
        key: "profile",
        icon: renderIcon(PersonOutlineOutlined)
    },
    {
        label: "Profile Settings",
        key: "editProfile",
        icon: renderIcon(SettingsRound)
    },
    {
        label: "Logout",
        key: "logout",
        icon: renderIcon(LogOutOutlined)
    }
]
const handleSelect = (key) => {
    switch (key) {
        case "profile":
            router.push({ name: "Profile" })
            break;
        case "editProfile":
            router.push({ name: "Settings" })
            break;
        case "logout":
            terminateUserSession(userStore.sid);
            userStore.clearUser()
            router.push({ name: "Sign In" })
            break;
    }
}
</script>
<style scoped>
.nav {
    display: flex;
    align-items: center;
    padding: 8px;
    height: var(--header-height);
    position: absolute;
    z-index: 10;
}

.ui-logo {
    display: flex;
    align-items: center;
    font-size: 18px;
}

.ui-logo>img {
    margin: 0 12px 0 8px;
    height: 32px;
    width: 32px;
}
</style>