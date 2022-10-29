<template>
    <n-data-table :columns="columns" :data="data" :row-class-name="rowClassName" />
</template>

<script setup>
import { h } from "vue";
import { NButton, NIcon, useMessage } from "naive-ui";
import { DeleteForeverFilled } from '@vicons/material'

const rowClassName = (row) => {
    if (row.sid != "f653f4aa-5658-47d9-b8c1-c54002730535") {
        return 'highlight'
    }
    return ''
}
const play = (row) => {
    message.info(`Play ${row.sid}`);
}
const createColumns = () => {
    return [
        {
            title: "Last Updated",
            key: "last_updated"
        },
        {
            title: "Device",
            key: "user_agent"
        },
        {
            title: "",
            key: "actions",
            render(row) {
                return h(
                    NButton,
                    {
                        quaternary: true,
                        circle: true,
                        type: "error",
                        onClick: () => play(row),
                    },
                    {
                        icon: () => h(
                            NIcon,
                            null,
                            {
                                default: () => h(DeleteForeverFilled),
                            }
                        )
                    }
                );
            }
        }
    ];
};
{/* <n-button quaternary circle type="error">
      <template #icon>
        <n-icon><DeleteForeverFilled /></n-icon>
      </template>
    </n-button> */}


const data = [
    { sid: "2e30e1b9-4219-4abe-b66b-a92dc0d1c70a", last_updated: "2022-10-30 00:15:29.573054+03", user_agent: "PC / Windows 10 / Chrome 106.0.0" },
    { sid: "f653f4aa-5658-47d9-b8c1-c54002730535", last_updated: "2022-10-30 00:08:21.86411+03", user_agent: "PC / Windows 10 / Chrome 106.0.0" },
];

const message = useMessage();
const columns = createColumns()
</script>

<style scoped>
:deep(.highlight td) {
    background-color: rgba(90, 207, 168, 0.37) !important;
}
</style>

