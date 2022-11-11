<template>
  <n-dropdown trigger="click" placement="bottom-center" :options="uploadOptions" @select="uploadSelect">
    <n-button>Upload</n-button>
  </n-dropdown>
  <n-upload multiple directory-dnd :custom-request="customRequest" :default-upload="false" ref="uploadSubmit">
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
</template>
  
<script setup>
import { ref } from 'vue';
import {
  FileUploadRound
} from "@vicons/material";
import { instance } from '@/utils/api'

const uploadSubmit = ref(null);

const uploadOptions = [
  {
    label: "Upload",
    key: "upload"
  },
  {
    label: "Upload & Group",
    key: "group"
  },
]

const uploadSelect = (key) => {
  switch (key) {
    case "upload":
      uploadSubmit.value?.submit()
      break;
    case "group":
      // TODO
      alert("Nope ;-)")
      break;
  }
}
// TODO
// TODO
// TODO
// TODO
// TODO
// TODO
// TODO
// TODO
// TODO
// TODO
// TODO
// TODO
// TODO

// GATEWAY TIMEOUT выкидывает если файл больщой => настроить nginx!!!
const customRequest = ({
  file,
  onFinish,
  onError,
  onProgress
}) => {
  const formData = new FormData();
  formData.append("uploaded_file", file.file);

  instance.post('/files/', formData, {
    onUploadProgress: function (progressEvent) {
      onProgress({ percent: Math.ceil(progressEvent.loaded / progressEvent.total * 100) });
    }
  }).then(res => {
    console.log(res)
    onFinish();
  }).catch(err => {
    console.log(err)
    onError();
  })
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