<template>
  <n-tabs type="bar" animated>
    <n-tab-pane display-directive="show:lazy" name="Upload" :tab="renderTextBadge('Upload', uploadingFileList.length)">
      <n-upload multiple :custom-request="wUploadFile" :file-list="uploadingFileList" @change="handleUploadChange">
        <n-upload-dragger>
          <div style="margin-bottom: 12px">
            <n-icon size="48" :depth="3">
              <FileUploadRound />
            </n-icon>
          </div>
          <n-text style="font-size: 16px">
            Click or drag a file to this area to upload
          </n-text>
          <n-p depth="3" style="margin: 8px 0 0 0">
            Upload an image, video, story in txt format or manga in tar archive format
          </n-p>
        </n-upload-dragger>
      </n-upload>
    </n-tab-pane>


    <n-tab-pane display-directive="show:lazy" name="Processing"
      :tab="renderTextBadge('Processing', processingFilesList.length)">
      <n-grid v-if="processingFilesList.length" :x-gap="12" :y-gap="8" cols="1 700:2 1050:3 1400:4 2100:6">
        <n-grid-item v-for="file in processingFilesList" :key="file.id">
          <FileCardProcessing :file="file" :selected="selectedFiles.includes(file.id)" @select="handleSelect" />
        </n-grid-item>
      </n-grid>
      <div v-else>
        <n-empty description="No Processing Files" />
      </div>
    </n-tab-pane>


    <n-tab-pane display-directive="show:lazy" name="Error" :tab="renderTextBadge('Error', errorFilesList.length)">
      <n-space v-if="errorFilesList.length" vertical>
        <n-button @click="deleteFiles(errorFilesList.map(x => x.id))" type="error">Delete All</n-button>
        <n-grid :x-gap="12" :y-gap="8" cols="1 700:2 1050:3 1400:4 2100:6">
          <n-grid-item v-for="file in errorFilesList" :key="file.id">
            <FileCardError :file="file" @delete="wDeleteFile(file.id)" />
          </n-grid-item>
        </n-grid>
      </n-space>
      <div v-else>
        <n-empty description="No Error Files" />
      </div>
    </n-tab-pane>


    <n-tab-pane display-directive="show:lazy" name="Ready" :tab="renderTextBadge('Ready', readyFilesList.length)">
      <n-space v-if="readyFilesList.length" vertical>
        <div class="flex-wrap">
          <div class="flex" style="flex-grow: 1">
            <n-button @click="selectAll" style="flex-grow: 1">Select All</n-button>
            <n-button :disabled="selectedFiles.length == 0" @click="clearAll" style="flex-grow: 1">Clear All</n-button>
          </div>
          <div style="flex-grow: 999; min-width: 200px;">
            <n-select :disabled="selectedFiles.length == 0" v-model:value="filesTags" multiple filterable tag
              :options="options" max-tag-count="responsive" placeholder="Intersecting Tags" />
          </div>
          <div class="flex" style="flex-grow: 1">
            <n-button :disabled="selectedFiles.length == 0" @click="deleteFiles(selectedFiles)" type="error"
              style="flex-grow: 1">Delete</n-button>
            <n-button :disabled="selectedFiles.length == 0" type="primary" style="flex-grow: 1">Publish</n-button>
          </div>
        </div>
        <n-grid :x-gap="12" :y-gap="8" cols="1 700:2 1050:3 1400:4 2100:6">
          <n-grid-item v-for="file in readyFilesList.slice((page - 1) * pageSize, page * pageSize)" :key="file.id">
            <FileCard @tagsupdate="updateTags" @like="handleLike" :file="file" :selected="selectedFiles.includes(file.id)" @select="handleSelect" />
          </n-grid-item>
        </n-grid>
        <div v-if="readyFilesList.length > pageSize" style="display: flex; justify-content: center;">
          <n-pagination v-model:page="page" :page-slot="7" :item-count="readyFilesList.length" :page-size="pageSize" />
        </div>
      </n-space>
      <div v-else>
        <n-empty description="No Ready Files" />
      </div>
    </n-tab-pane>


  </n-tabs>

</template>
  
<script setup>
import {
  FileUploadRound,
} from "@vicons/material";
import { ref, watch, computed } from 'vue';
import { uploadFile } from '@/utils/api'
import { getPrivateFiles, deleteFile } from '@/utils/api'
import { apiWrapper } from '@/utils/apiWrapper'
import FileCard from '@/components/FileCard.vue'
import FileCardError from '@/components/FileCardError.vue'
import FileCardProcessing from '@/components/FileCardProcessing.vue'
import { renderTextBadge } from '@/utils/textBadge'


const apiw = apiWrapper()


// Uploading
const uploadingFileList = ref([]);
const handleUploadChange = (data) => {
  uploadingFileList.value = data.fileList;
}

const wUploadFile = ({
  file,
  onFinish,
  onError,
  onProgress
}) => {
  apiw.wrap(() => uploadFile(file.file, onProgress), () => { onFinish() }, () => { onError() })
};


// Pages
const page = ref(1)
const pageSize = 12


// FileList
const filesList = ref([
  {
    "id": 495,
    "uri": "data/user/SilkSlime/IMG_7268.JPG",
    "owner": "SilkSlime",
    "description": "",
    "upload_time": "2022-11-18T23:45:35.712634+03:00",
    "size": "677.13 KB",
    "name": "IMG_7268",
    "type": "Image",
    "state": "private",
    "tags": ["Настя", "Балда", "Настя", "Балда", "Настя", "Балда", "Настя", "Балда", "Настя", "Балда"]
  },
]
)
const processingFilesList = computed(() => {
  return filesList.value.filter(x => x.state == 'processing')
})
const errorFilesList = computed(() => {
  return filesList.value.filter(x => x.state == 'error')
})
const readyFilesList = computed(() => {
  return filesList.value.filter(x => x.state == 'private')
})
watch(readyFilesList, async (n, o) => {
  let maxPage = Math.ceil(n.length / pageSize)
  if (page.value > maxPage)
    page.value = maxPage
})
const wGetPrivateFiles = () => {
  apiw.wrap(() => getPrivateFiles(), (content) => { filesList.value = content })
}
// wGetPrivateFiles()
// setInterval(wGetPrivateFiles, 2000);


// Selecting
const selectedFiles = ref([])
const handleSelect = (id) => {
  if (selectedFiles.value.includes(id)) {
    selectedFiles.value = selectedFiles.value.filter(x => x != id)
  } else {
    selectedFiles.value.push(id)
  }
}
const selectAll = () => {
  selectedFiles.value = readyFilesList.value.map(({ id }) => id)
}
const clearAll = () => {
  selectedFiles.value = []
}


// Deleting
const wDeleteFile = (id) => {
  apiw.wrap(() => deleteFile(id))
}

const deleteFiles = (ids) => {
  for (let id of ids) {
    handleSelect(id)
    wDeleteFile(id)
  }
}

// Like
const handleLike = (id) => {
  alert(`Liked ${id}`)
}
</script>
<style scoped>
:deep(.n-upload-file--success-status span) {
  color: #63e2b7 !important;
}

.flex-wrap {
  display: flex;
  gap: 8px 12px;
  flex-wrap: wrap;
}

.flex {
  display: flex;
  gap: 8px 12px;
}
</style>