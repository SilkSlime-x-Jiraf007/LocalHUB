<template>
  <n-space vertical>
    <n-upload v-model:file-list="fileList" @update:file-list="handleFileListChange" multiple directory-dnd
      :custom-request="wUploadFile">
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
    <n-grid :x-gap="12" :y-gap="8" cols="1 700:2 1050:3 1400:4 2100:6">
      <n-grid-item v-for="file in privateFilesList">
        <FileCard :file="file" :checked="checkedFiles.includes(file.id)" @check="handleCheck" />
      </n-grid-item>
    </n-grid>
  </n-space>
</template>
  
<script setup>
import { ref } from 'vue';
import {
  FileUploadRound
} from "@vicons/material";
import { uploadFile, getPrivateFiles } from '@/utils/api'
import { apiWrapper } from '@/utils/apiWrapper'
import FileCard from '@/components/FileCard.vue'


const apiw = apiWrapper()

const privateFilesList = ref([
  {
    "id": 1,
    "uri": "user/SilkSlime/image.jpg",
    "owner": "SilkSlime",
    "description": "This is image",
    "upload_time": "2022-11-13T21:47:52.976108+03:00",
    "size": "228.0 B",
    "name": "image",
    "type": "Image",
    "group": null,
    "state": "private",
    "message": ""
  },
  {
    "id": 2,
    "uri": "user/SilkSlime/other.json",
    "owner": "SilkSlime",
    "description": "This is other file",
    "upload_time": "2022-11-13T21:47:52.976108+03:00",
    "size": "2282.0 B",
    "name": "other",
    "type": "Other",
    "group": null,
    "state": "private",
    "message": ""
  },
  {
    "id": 3,
    "uri": "user/SilkSlime/video.mp4",
    "owner": "SilkSlime",
    "description": "This is some video",
    "upload_time": "2022-11-13T21:47:52.976108+03:00",
    "size": "22.0 MB",
    "name": "video",
    "type": "Video",
    "group": null,
    "state": "private",
    "message": ""
  },
  {
    "id": 4,
    "uri": "user/SilkSlime/story.txt",
    "owner": "SilkSlime",
    "description": "This is text story",
    "upload_time": "2022-11-13T21:47:52.976108+03:00",
    "size": "22.0 B",
    "name": "story",
    "type": "Story",
    "group": null,
    "state": "private",
    "message": ""
  },
  
  {
    "id": 5,
    "uri": "user/SilkSlime/wrong.jpg",
    "owner": "SilkSlime",
    "description": "This is processing file",
    "upload_time": "2022-11-13T21:47:52.976108+03:00",
    "size": "0 B",
    "name": "wrong",
    "type": "Other",
    "group": null,
    "state": "processing",
    "message": ""
  },
  {
    "id": 6,
    "uri": "user/SilkSlime/wrong.jpg",
    "owner": "SilkSlime",
    "description": "This is ERROR file!",
    "upload_time": "2022-11-13T21:47:52.976108+03:00",
    "size": "0 B",
    "name": "wrong",
    "type": "Other",
    "group": null,
    "state": "error",
    "message": "Any message with error"
  },
])

const checkedFiles = ref([])
const handleCheck = (id) => {
  if (checkedFiles.value.includes(id)) {
    checkedFiles.value = checkedFiles.value.filter(x => x != id)
  } else {
    checkedFiles.value.push(id)
  }
}




const wGetPrivateFiles = () => {
  apiw.wrap(() => getPrivateFiles(), (content) => { privateFilesList.value = content })
}
// wGetPrivateFiles()
// setInterval(wGetPrivateFiles, 1000);

const fileList = ref([]);
const handleFileListChange = (fl) => {
  fileList.value = fl.filter(x => x.status != "finished")
}
const wUploadFile = ({
  file,
  onFinish,
  onError,
  onProgress
}) => {
  apiw.wrap(() => uploadFile(file.file, onProgress), onFinish, onError)
};
</script>
<style scoped>
:deep(.n-upload-file--success-status span) {
  color: #63e2b7 !important;
}

/* .n-upload-file--success-status>div>div>span {
  color: #63e2b7 !important;
} */
</style>