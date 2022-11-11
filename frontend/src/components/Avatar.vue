<script setup>
import Amogus from '@/components/icons/Amogus.vue'
import { stringToColor } from '@/utils/colors.js'
const props = defineProps({
    username: {},
    size: {
        default: '28px'
    }
})
</script>

<template>
    <div :style="{height: props.size, width: props.size}">
        <Amogus :color="stringToColor(props.username)"/>
    </div>
</template>

<style scoped>
div {
    background-color: rgb(66, 66, 69);
    border-radius: 100%;
    overflow: hidden;
}
</style>
