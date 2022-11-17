<template>
  <n-space vertical>
    <n-upload v-model:file-list="fileList" multiple
      :custom-request="wUploadFile"
    >
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
  </n-space>
</template>
  
<script setup>
import {
  FileUploadRound,
} from "@vicons/material";
import { uploadFile } from '@/utils/api'
import { apiWrapper } from '@/utils/apiWrapper'

const apiw = apiWrapper()

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
</style>