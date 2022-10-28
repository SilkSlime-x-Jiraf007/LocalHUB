<script setup>
import Amogus from '@/components/icons/Amogus.vue'
import { stringToColor } from '@/utils/colors.js'
const props = defineProps(['username'])

</script>

<template>
    <div>
        <Amogus :color="stringToColor(props.username)" />
    </div>
</template>

<style scoped>
div {
    background-color: rgb(66, 66, 69);
    height: 28px;
    width: 28px;
    border-radius: 100%;
    overflow: hidden;
}
</style>
