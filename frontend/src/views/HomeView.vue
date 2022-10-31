<template>
    <n-table :bordered="true">
        <thead>
            <tr>
                <th>Last Updated</th>
                <th>Device</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            <tr v-if="data.length" v-for="session in data" :class="{highlight: session.sid == debugSid}">
                <td>
                    <n-time :time="Date.parse(session.last_updated)" />
                </td>
                <td>{{ session.user_agent }}</td>
                <td style="display: flex; justify-content: center;">
                    <n-button v-if="session.sid != debugSid" quaternary circle type="error" @click="terminateSession(session.sid)">
                        <template #icon>
                            <n-icon>
                                <DeleteForeverFilled />
                            </n-icon>
                        </template>
                    </n-button>
                    <span v-else>Your session!</span>
                </td>
            </tr>
            <tr v-else><td colspan="3"><n-empty description="No Data"/></td></tr>
        </tbody>
    </n-table>
</template>

<script setup>
import { NButton, NIcon, useMessage } from "naive-ui";
import { DeleteForeverFilled } from '@vicons/material'

const terminateSession = (sid) => {
    message.info(`Play ${sid}`);
}
const debugSid = "f653f4aa-5658-47d9-b8c1-c54002730535"
const data = [
    { sid: "2e30e1b9-4219-4abe-b66b-a92dc0d1c70a", last_updated: "2022-10-30 00:15:29.573054+03", user_agent: "PC / Windows 10 / Chrome 106.0.0" },
    { sid: "f653f4aa-5658-47d9-b8c1-c54002730535", last_updated: "2022-10-30 00:08:21.86411+03", user_agent: "PC / Windows 10 / Chrome 106.0.0" },
];

const message = useMessage();

</script>

<style scoped>
:deep(.highlight td) {
    background-color: rgba(90, 207, 168, 0.37) !important;
}
</style>

