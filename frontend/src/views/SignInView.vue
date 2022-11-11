<template>
    <div class="card-wrapper">
        <n-card title="Sign In">
            <n-space vertical>
                <n-input required v-model:value="username" type="text" placeholder="Username" />
                <n-input required v-model:value="password" type="password" show-password-on="click"
                    placeholder="Password" />
                <n-button @click="signin" type="primary" block>Sign In</n-button>
            </n-space>
            <template #footer v-if="errorMessages.length != 0">
                <div v-for="errorMessage in errorMessages" class="error-message">{{ errorMessage }}</div>
            </template>
        </n-card>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { userSignIn } from '@/utils/api'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
const router = useRouter()
const userStore = useUserStore()

const username = ref("")
const password = ref("")
const errorMessages = ref([])


const signin = async () => {
    try {
        const {content, message} = await userSignIn(username.value, password.value);
        userStore.setTokens(content.access_token, content.refresh_token)
        router.push('/')
    } catch ({content, message}) {
        console.log(content)
        console.log(message)
    }
}
</script>
<style scoped>
.card-wrapper {
    display: flex;
    justify-content: center;
}

.n-card {
    max-width: 600px;
}

.error-message {
    color: #e88080
}
</style>