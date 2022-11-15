<template>
    <n-card :title="file.name" :style="{backgroundColor: file.state == 'error' ? '#1c0000' : 'inherit', borderColor: file.state == 'error' ? '#e88080' : 'inherit'}">
        <template #cover>
            <div style="background-color: rgba(0, 0, 0, 0.3);">
                <div v-if="file.state == 'private'">
                    <img v-if="file.type == 'Image'" style="height: 180px; object-fit: contain;" :src="'/data/' + file.uri">
                    <video v-else-if="file.type == 'Video'" style="display: block; width: 100%; height: 180px" preload="metadata"
                        controls>
                        <source :src="'/data/' + file.uri">
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
                <div v-else-if="file.state == 'processing'" class="cover-icon">
                    <n-spin size="large" />
                </div>
                <div v-else-if="file.state == 'error'" class="cover-icon">
                    <n-icon :component="ErrorOutlineRound" color="#e88080" size="50" />
                </div>
            </div>
            <div class="param">
                <n-checkbox :checked="checked" @update:checked="$emit('check', file.id)"/>
                <!-- <n-dropdown v-if="file.state == 'private'" trigger="hover" :options="options" @select="handleSelect">
                    <n-button text>
                        <template #icon>
                            <n-icon>
                                <MoreVertRound />
                            </n-icon>
                        </template>
                    </n-button>
                </n-dropdown> -->
                <!-- <n-button text type="error">
                    <template #icon>
                        <n-icon>
                            <DeleteForeverRound />
                        </n-icon>
                    </template>
                </n-button> -->
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
    MoreVertRound,
    ErrorOutlineRound,
    DeleteForeverRound
} from "@vicons/material";
const props = defineProps({
    file: {},
    checked: {},
})

const options = [
    {
        label: "Publish",
        key: "publish",
    },
    {
        label: "Delete",
        key: "delete"
    },
]

const handleSelect = (key) => {
    alert(key);
}
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
</style>