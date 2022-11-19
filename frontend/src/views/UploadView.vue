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


    <n-tab-pane display-directive="show:lazy" name="Processing" :tab="renderTextBadge('Processing', totalProcessing)">
      <n-space v-if="processingFilesList.length">
        <n-grid :x-gap="12" :y-gap="8" cols="1 700:2 1050:3 1400:4 2100:6">
          <n-grid-item v-for="file in processingFilesList" :key="file.id">
            <FileCardProcessing :file="file" :selected="selectedFiles.includes(file.id)" @select="handleSelect" />
          </n-grid-item>
        </n-grid>
        <div v-if="totalError > pageSize" style="display: flex; justify-content: center;">
          <n-pagination v-model:page="pageError" :page-slot="7" :item-count="totalError" :page-size="pageSize" />
        </div>
      </n-space>
      <div v-else>
        <n-empty description="No Processing Files" />
      </div>
    </n-tab-pane>


    <n-tab-pane display-directive="show:lazy" name="Error" :tab="renderTextBadge('Error', totalError)">
      <n-space v-if="errorFilesList.length" vertical>
        <n-button @click="deleteFileList(errorFilesList.map(x => x.id), wGetErrorFiles)" type="error">Delete Visible</n-button>
        <n-grid :x-gap="12" :y-gap="8" cols="1 700:2 1050:3 1400:4 2100:6">
          <n-grid-item v-for="file in errorFilesList" :key="file.id">
            <FileCardError :file="file" @delete="wDeleteFile(file.id, wGetErrorFiles)" />
          </n-grid-item>
        </n-grid>
        <div v-if="totalError > pageSize" style="display: flex; justify-content: center;">
          <n-pagination v-model:page="pageError" :page-slot="7" :item-count="totalError" :page-size="pageSize" />
        </div>
      </n-space>
      <div v-else>
        <n-empty description="No Error Files" />
      </div>
    </n-tab-pane>


    <n-tab-pane display-directive="show:lazy" name="Ready" :tab="renderTextBadge('Ready', totalPrivate)">
      <n-space v-if="privateFilesList.length" vertical>
        <div class="flex-wrap">
          <div class="flex" style="flex-grow: 1">
            <n-button @click="selectAll" style="flex-grow: 1">Select Visible</n-button>
            <n-button :disabled="selectedFiles.length == 0" @click="clearAll" style="flex-grow: 1">Clear All</n-button>
          </div>
          <div style="flex-grow: 999; min-width: 200px;">
            <n-select :disabled="selectedFiles.length == 0" v-model:value="filesTags" multiple filterable tag
              :options="options" max-tag-count="responsive" placeholder="Intersecting Tags" />
          </div>
          <div class="flex" style="flex-grow: 1">
            <n-button :disabled="selectedFiles.length == 0" @click="deleteFileList(selectedFiles, wGetPrivateFiles)" type="error"
              style="flex-grow: 1">Delete</n-button>
            <n-button :disabled="selectedFiles.length == 0" type="primary" style="flex-grow: 1">Publish</n-button>
          </div>
        </div>
        <n-grid :x-gap="12" :y-gap="8" cols="1 700:2 1050:3 1400:4 2100:6">
          <n-grid-item v-for="file in privateFilesList" :key="file.id">
            <FileCard @tagsupdate="(a) => { }" @like="handleLike" :file="file"
              :selected="selectedFiles.includes(file.id)" @select="handleSelect" />
          </n-grid-item>
        </n-grid>
        <div v-if="totalPrivate > pageSize" style="display: flex; justify-content: center;">
          <n-pagination v-model:page="pagePrivate" :page-slot="7" :item-count="totalPrivate" :page-size="pageSize" />
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
import { getProcessingFiles, getErrorFiles, getPrivateFiles, deleteFile } from '@/utils/api'
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



const pageSize = ref(6)

// Processing
const pageProcessing = ref(1)
const totalProcessing = ref(0)
const processingFilesList = ref([])
watch(totalProcessing, async (n, o) => {
  let maxPage = Math.max(Math.ceil(n / pageSize.value), 1)
  if (pageProcessing.value > maxPage) {
    pageProcessing.value = maxPage
  }
})
const wGetProcessingFiles = () => {
  apiw.wrap(() => getProcessingFiles(pageProcessing.value, pageSize.value), ({ items, total }) => {
    processingFilesList.value = items;
    totalProcessing.value = total;
  })
}
watch(pageProcessing, async (n, o) => {
  wGetProcessingFiles()
})
wGetProcessingFiles()
setInterval(wGetProcessingFiles, 2000);
// Error
const pageError = ref(1)
const totalError = ref(0)
const errorFilesList = ref([])
watch(totalError, async (n, o) => {
  let maxPage = Math.max(Math.ceil(n / pageSize.value), 1)
  if (pageError.value > maxPage) {
    pageError.value = maxPage
  }
})
const wGetErrorFiles = () => {
  apiw.wrap(() => getErrorFiles(pageError.value, pageSize.value), ({ items, total }) => {
    errorFilesList.value = items;
    totalError.value = total;
  })
}
watch(pageError, async (n, o) => {
  wGetErrorFiles()
})
wGetErrorFiles()
setInterval(wGetErrorFiles, 2000);
// Private
const pagePrivate = ref(1)
const totalPrivate = ref(0)
const privateFilesList = ref([])
watch(totalPrivate, async (n, o) => {
  let maxPage = Math.max(Math.ceil(n / pageSize.value), 1)
  if (pagePrivate.value > maxPage) {
    pagePrivate.value = maxPage
  }
})
const wGetPrivateFiles = () => {
  apiw.wrap(() => getPrivateFiles(pagePrivate.value, pageSize.value), ({ items, total }) => {
    privateFilesList.value = items;
    totalPrivate.value = total;
  })
}
watch(pagePrivate, async (n, o) => {
  wGetPrivateFiles()
})
const selectedFiles = ref([])
const handleSelect = (id) => {
  if (selectedFiles.value.includes(id)) {
    selectedFiles.value = selectedFiles.value.filter(x => x != id)
  } else {
    selectedFiles.value.push(id)
  }
}
const selectAll = () => {
  selectedFiles.value.push(...privateFilesList.value.map(({ id }) => id))
}
const clearAll = () => {
  selectedFiles.value.length = 0
}
wGetPrivateFiles()
setInterval(wGetPrivateFiles, 2000);



// Deleting
const wDeleteFile = (id, callback=null) => {
  apiw.wrap(() => deleteFile(id), (content) => {
    selectedFiles.value = selectedFiles.value.filter(x => x != id)
    if (callback) callback()
  })
}
const deleteFileList = (ids, callback=null) => {
  for (let id of ids) {
    wDeleteFile(id, callback)
  }
}

// Like
const handleLike = (id) => {
  alert(`Liked ${id}`)
}

// tags
const filesTags = ref([])
const options = [
  {
    type: "group",
    label: "Common",
    key: "Common",
    children: [
      {
        label: "Soft",
        value: "Soft",
      },
      {
        label: "Test",
        value: "Test"
      }
    ]
  },
  {
    type: "group",
    label: "Artist",
    key: "Artist",
    children: [
      {
        label: "JLullaby (39)",
        value: "JLullaby"
      },
      {
        label: "ikemeru19",
        value: "ikemeru19"
      },
      {
        label: "Aroma Sensei",
        value: "Aroma Sensei"
      },
    ]
  }
];
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