import { createApp } from 'vue'
import naive from 'naive-ui'
import { createPinia } from 'pinia'
import Root from './Root.vue'
import router from './router'
import './assets/vars.css'


const app = createApp(Root)

app.use(createPinia())
app.use(router)
app.use(naive)
app.mount('#app')
