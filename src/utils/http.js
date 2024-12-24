import axios from "axios";
import {useUserStore} from "@/stores/user";
import router from '@/router'
import { ElMessage } from 'element-plus'
const baseURL = import.meta.env.VITE_API_BASE_URL

const http = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    }
})

http.interceptors.request.use(config => {
    const userStore = useUserStore();
    if (userStore.userInfo.token) {
        config.headers.Authorization = `Bearer ${userStore.userInfo.token}`
    }
    return config
}, e => Promise.reject(e))

http.interceptors.response.use(res => res.data, e => {
    if (e.response) {
        switch (e.response.status) {
            case 401:
                ElMessage({
                    type: 'warning',
                    message: e.response.data.error || 'Please Login'
                })
                const userStore = useUserStore();
                userStore.userLogout()
                router.replace('/')
                break;
            case 403:
                ElMessage({
                    type: 'warning',
                    message: e.response.data.error || 'Permission Denied'
                })
                router.replace('/login')
                break;
            case 404:
                router.replace('/NotFound')
                break;
            default:
                ElMessage({
                    type: 'error',
                    message: e.response.data?.error || 'Server Error'
                })
        }
    } else if (e.request) {
        ElMessage({
            type: 'error',
            message: 'Network error, please check your network connection'
        })
    } else {
        ElMessage({
            type: 'error',
            message: 'Request configuration error'
        })
    }
    return Promise.reject(e)
})

export default http