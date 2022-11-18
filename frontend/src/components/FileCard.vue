<template>
    <n-card :title="file.name" :class="{error: file.state == 'error', selected: selected}">
        <template #cover>
            <div style="background-color: rgba(0, 0, 0, 0.3);">
                <img v-if="file.type == 'Image'" style="height: 180px; object-fit: contain;" :src="file.uri">
                <video v-else-if="file.type == 'Video'" style="display: block; width: 100%; height: 180px" preload="metadata"
                    controls>
                    <source :src="file.uri">
                </video>
                <div v-else-if="file.type == 'Manga'" class="cover-icon">
                    <n-icon :component="AutoStoriesRound" size="50" />
                </div>
                <div v-else-if="file.type == 'Story'" class="cover-icon">
                    <n-icon :component="AutoStoriesRound" size="50" />
                </div>
                <div v-else-if="file.type == 'Other'" class="cover-icon">
                    <n-icon :component="InsertDriveFileRound" size="50" />
                </div>
            </div>
            <div class="param">
                <n-checkbox :checked="selected" @update:checked="$emit('select', file.id)"/>
            </div>
        </template>
        {{ file.description }}
    </n-card>
</template>
<script setup>
import { NIcon } from "naive-ui";
import {
    AutoStoriesRound,
    InsertDriveFileRound,
    ErrorOutlineRound,
} from "@vicons/material";

const {file, selected} = defineProps({
    file: {},
    selected: {},
})
</script>
<style scoped>
.cover-icon {
    /* min-height: 140px; */
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

.test {
    background-color: #1c0000;
    border-color: #e88080;
}

.error {
    background-color: #1b0a0a;
    border-color: #e88080;
}

.selected {
    border-color: #63e2b7;
}
</style>