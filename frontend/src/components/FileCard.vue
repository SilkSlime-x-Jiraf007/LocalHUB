<template>
    <n-card :class="{ error: file.state == 'error', selected: selected }" content-style="padding: 6px 8px">
        <template #cover>
            <div style="background-color: rgba(0, 0, 0, 0.3);">
                <img v-if="file.type == 'Image'" style="height: 180px; object-fit: contain;" :src="file.uri">
                <video v-else-if="file.type == 'Video'" style="display: block; width: 100%; height: 180px"
                    preload="metadata" controls>
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
                <n-checkbox :checked="selected" @update:checked="$emit('select', file.id)" />
            </div>
        </template>
        <n-thing>
            <template #header>
                {{ file.name }}
            </template>
            <template #header-extra>
                <!-- <n-rate color="#4fb233">
                    <n-icon size="20">
                        <cash-icon />
                    </n-icon>
                </n-rate> -->
                <n-button @click="handleLike" text size="small" type="error">
                    <template #icon>
                        <FavoriteRound v-if="file.like"/>
                        <FavoriteBorderRound v-else />
                    </template>
                </n-button>
            </template>
            <template v-if="file.description" #description>
                {{ file.description }}
            </template>
            <div v-if="!editMode" style="display: flex; align-items: flex-start; gap: 6px;">
                <div style="flex-grow: 100; display: flex; gap: 3px; flex-wrap: wrap;">
                    <n-tag v-if="fileTags?.length" v-for="tag in fileTags" :key="tag" size="small">{{ tag }}</n-tag>
                    <span v-else>No Tags</span>
                </div>
                <n-button @click="handleEditMode" text size="small">
                    <template #icon>
                        <SettingsRound />
                    </template>
                </n-button>
            </div>
            <div v-if="editMode" style="display: flex; align-items: flex-start; gap: 6px;">
                <div  style="flex-grow: 100; display: flex; gap: 3px; flex-wrap: wrap;">
                    <n-select v-if="editMode" v-model:value="fileTags" size="small" multiple filterable tag
              :options="options"/>
                </div>
                <n-button @click="handleEditMode" size="tiny">
                    <template #icon>
                        <CheckRound />
                    </template>
                </n-button>
            </div>
            
            <template #footer>
                <n-p depth="3">
                    by {{ file.owner }}
                </n-p>
            </template>
        </n-thing>
    </n-card>
</template>
<script setup>
import { ref } from "vue";
import { NIcon } from "naive-ui";
import {
    AutoStoriesRound,
    InsertDriveFileRound,
    FavoriteBorderRound,
    FavoriteRound,
    SettingsRound,
    CheckRound
} from "@vicons/material";

const { file, selected } = defineProps({
    file: {},
    selected: {},
})
const emit = defineEmits(['like', 'tagsupdate'])


const editMode = ref(false)
const fileTags = ref(file.tags)

const handleEditMode = () => {
    if (editMode.value == false) editMode.value = true;
    else {
        emit('tagsupdate', {id: file.id, tagList: fileTags.value})
        editMode.value = false;
    }
}

const handleLike = () => {
    emit('like', file.id)
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
    right: 8px;
    top: 6px;
}

.selected {
    border-color: #63e2b7;
}
</style>