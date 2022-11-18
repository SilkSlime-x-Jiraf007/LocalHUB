<template>
    <n-card :title="file.name">
        <template #cover>
            <div style="background-color: rgba(0, 0, 0, 0.3);">
                <div class="cover-icon">
                    <n-spin size="large" />
                </div>
            </div>
        </template>
        {{ file.description }}
    </n-card>
</template>
<script setup>

const {file} = defineProps({
    file: {}
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
</style>