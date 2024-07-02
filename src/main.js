import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// 注册 store
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 导入所有图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 导入 axios
import axios from 'axios'
import VueAxios from 'vue-axios'

// 全局注册图标
const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(store).use(router).use(ElementPlus).use(VueAxios, axios).mount('#app')
