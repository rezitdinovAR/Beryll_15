import {createApp} from 'vue'
import App from './App.vue'
import {createPinia} from 'pinia';
import router from "@/router/router.js";

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import './style.scss'

const pinia = createPinia();
let app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')