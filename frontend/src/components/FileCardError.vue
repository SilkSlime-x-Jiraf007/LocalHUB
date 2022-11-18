<template>
    <n-card :title="file.name" class="error">
        <template #cover>
            <div style="background-color: rgba(0, 0, 0, 0.3);">
                <div class="cover-icon">
                    <n-icon :component="ErrorOutlineRound" color="#e88080" size="50" />
                </div>
            </div>
            <div class="param">
                <n-button @click="$emit('delete', file.id)" quaternary circle type="error">
                    <template #icon>
                        <n-icon>
                            <DeleteForeverRound />
                        </n-icon>
                    </template>
                </n-button>
            </div>
        </template>
        {{ file.description }}
    </n-card>
</template>
<script setup>
import { NIcon } from "naive-ui";
import {
    ErrorOutlineRound,
    DeleteForeverRound
} from "@vicons/material";

const { file, selected } = defineProps({
    file: {},
})
</script>
<style scoped>
.cover-icon {
    height: 180px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.param {
    position: absolute;
    right: 6px;
    top: 6px;
}

.error {
    background-color: #1b0a0a;
    border-color: #e88080;
}
</style>