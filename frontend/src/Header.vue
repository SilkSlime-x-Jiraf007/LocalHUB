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
            <span>LocalHUB{{ titleSuffix ? ` | ${titleSuffix}` : "" }}</span>
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
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'
import { MenuRound } from '@vicons/material'
import { NIcon } from "naive-ui";
import Avatar from '@/components/Avatar.vue'
import {
    PersonOutlineOutlined as UserIcon,
    EditFilled as EditIcon,
    LogOutOutlined as LogoutIcon
} from "@vicons/material";
const { titleSuffix } = defineProps({
    titleSuffix: {
        default: null
    },
    drawer: {}
})

const breakpoints = useBreakpoints(breakpointsTailwind)
const mobileMini = breakpoints.smallerOrEqual('md')
const mobile = breakpoints.smallerOrEqual('2xl')

const router = useRouter()
const userStore = useUserStore()

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
        icon: renderIcon(UserIcon)
    },
    {
        label: "Edit Profile",
        key: "editProfile",
        icon: renderIcon(EditIcon)
    },
    {
        label: "Logout",
        key: "logout",
        icon: renderIcon(LogoutIcon)
    }
]
const handleSelect = (key) => {
    switch (key) {
        case "profile":
            alert('Неа');
            break;
        case "editProfile":
            alert('Тоже нет!');
            break;
        case "logout":
            // TODO clear session
            userStore.clearUser()
            router.push({name: "SignIn"})
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