<template>
    <n-drawer v-if="mobile" :show="drawer" @update:show="toggle" :width="siderWidth" placement="left"
        style="top: var(--header-height); background-color: var(--dark-gray);" :z-index="8">
        <n-drawer-content :body-content-style="{ padding: '16px 0px' }" :native-scrollbar="false">
            <n-menu :options="makeMenuOptions(routerOptions)" :value="route.name" @update:value="toggle" />
        </n-drawer-content>
    </n-drawer>
    <n-layout-sider v-else :native-scrollbar="false" content-style="padding: 16px 0px;" bordered :width="menuWidth">
        <n-menu :options="makeMenuOptions(routerOptions)" :value="route.name" />
    </n-layout-sider>
</template>
<script setup>
import { h } from 'vue'
import { RouterLink, useRoute } from "vue-router";
import { NIcon } from "naive-ui";
import {
    RssFeedRound,
    PhotoLibraryRound,
    VideoLibraryRound,
    LibraryBooksRound,
    TranslateRound,
    FileUploadRound,
    SellRound,
    LockRound
} from "@vicons/material";

import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'

const emit = defineEmits(['update:drawer'])

const { siderWidth, drawer } = defineProps({
    siderWidth: {},
    drawer: Boolean
})


const breakpoints = useBreakpoints(breakpointsTailwind)
const mobile = breakpoints.smallerOrEqual('2xl')
const route = useRoute()

const toggle = (e) => {
    emit('update:drawer', drawer)
}


const routerOptions = [
    {
        display: "Feed",
        name: "Feed",
        icon: RssFeedRound
    },
    null,
    {
        display: "Images",
        name: "Images",
        icon: PhotoLibraryRound
    },
    {
        display: "Videos",
        name: "Videos",
        icon: VideoLibraryRound
    },
    {
        display: "Stories",
        name: "Stories",
        icon: LibraryBooksRound
    },
    {
        display: "Mangas",
        name: "Mangas",
        icon: TranslateRound
    },
    null,
    {
        display: "Tags",
        name: "Tags",
        icon: SellRound
    },
    null,
    {
        display: "Upload",
        name: "Upload",
        icon: FileUploadRound
    },
    {
        display: "Private",
        name: "Private",
        icon: LockRound
    },
]

const makeMenuOptions = (routerOptions) => {
    let menuOptions = [];
    for (let routerOption of routerOptions) {
        if (routerOption)
            menuOptions.push({
                label: () => h(RouterLink, { to: { name: routerOption.name } }, { default: () => routerOption.display }),
                key: routerOption.name,
                icon: () => h(NIcon, null, { default: () => h(routerOption.icon) })
            })
        else
            menuOptions.push({
                key: 'divider',
                type: 'divider',
            })
    }
    return menuOptions
}

</script>