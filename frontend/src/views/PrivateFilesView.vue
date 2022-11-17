<template>
  <n-space vertical>
    <n-space>
      <n-button @click="checkAll">Check All</n-button>
      <n-button @click="clearAll">Clear All</n-button>
      <div>
        <n-select v-model:value="filesTags" multiple filterable tag :options="options" max-tag-count="responsive" />
      </div>
    </n-space>


    <n-grid :x-gap="12" :y-gap="8" cols="1 700:2 1050:3 1400:4 2100:6">
      <n-grid-item v-for="file in privateFilesList">
        <FileCard :file="file" :checked="checkedFiles.includes(file.id)" @check="handleCheck" />
      </n-grid-item>
    </n-grid>


    <div style="display: flex; justify-content: center;">
      <n-pagination v-model:page="page" v-model:page-size="pageSize" :page-count="100" show-size-picker
        :page-sizes="[10, 20, 30, 40]" />
    </div>


  </n-space>
</template>
  
<script setup>
import { ref } from 'vue';
import {
  FileUploadRound,
  ConstructionRound
} from "@vicons/material";
import { uploadFile, getPrivateFiles } from '@/utils/api'
import { apiWrapper } from '@/utils/apiWrapper'
import FileCard from '@/components/FileCard.vue'

const page = ref(2)
const pageSize = ref(20)

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


const checkedFiles = ref([])
const handleCheck = (id) => {
  if (checkedFiles.value.includes(id)) {
    checkedFiles.value = checkedFiles.value.filter(x => x != id)
  } else {
    checkedFiles.value.push(id)
  }
}

const checkAll = () => {
  checkedFiles.value = privateFilesList.value.map(({ id }) => id)
}
const clearAll = () => {
  checkedFiles.value = []
}

const wGetPrivateFiles = () => {
  apiw.wrap(() => getPrivateFiles(), (content) => { privateFilesList.value = content })
}
// wGetPrivateFiles()
// setInterval(wGetPrivateFiles, 1000);

</script>
<style scoped>

</style>