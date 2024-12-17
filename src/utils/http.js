import axios from "axios";
import {useUserStore} from "@/stores/user";
import router from '@/router'
import { ElMessage } from 'element-plus'

const http = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    }
})

// axios请求拦截器
http.interceptors.request.use(config => {
    const userStore = useUserStore();
    if (userStore.userInfo.token) {
        config.headers.Authorization = `Bearer ${userStore.userInfo.token}`
    }
    return config
}, e => Promise.reject(e))

// axios响应式拦截器
http.interceptors.response.use(res => res.data, e => {
    // 确保 e.response 存在
    if (e.response) {
        switch (e.response.status) {
            case 401:
                ElMessage({
                    type: 'warning',
                    message: e.response.data.error || '未授权访问'
                })
                const userStore = useUserStore();
                userStore.userLogout()
                router.replace('/')
                break;
            case 403:
                ElMessage({
                    type: 'warning',
                    message: e.response.data.error || '禁止访问'
                })
                router.replace('/login')
                break;
            case 404:
                router.replace('/NotFound')
                break;
            default:
                ElMessage({
                    type: 'error',
                    message: e.response.data?.error || '服务器错误'
                })
        }
    } else if (e.request) {
        // 请求已经发出，但没有收到响应
        ElMessage({
            type: 'error',
            message: '网络错误，请检查您的网络连接'
        })
    } else {
        // 请求配置有误
        ElMessage({
            type: 'error',
            message: '请求配置错误'
        })
    }
    return Promise.reject(e)
})

export default http