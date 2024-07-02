import axios from 'axios'
// 引入loading插件
import { ElLoading } from 'element-plus'
// 引入element-plus的message插件
import { ElMessage } from 'element-plus'

let loadingInstance = null
const services = axios.create({
    timeout: 5000,
    baseURL: 'http://localhost:8081/',
    headers: {
        "Content-type": 'application/json;charset=UTF-8'
    }
})

// 拦截请求，加载loading和统一处理
services.interceptors.request.use(config => {
    loadingInstance = ElLoading.service({
        lock: true,
        text: 'Loading',
        background: 'rgba(0, 0, 0, 0.7)',
    })
    return config
})

// 响应请求，返回值统一处理
services.interceptors.response.use(response => {
    // 关闭loading
    loadingInstance.close()
    // 统一处理返回值
    const res = response.data
    console.log(res);

    return res

}, error => {
    // 关闭loading
    loadingInstance.close()
    // 使用element-plus统一处理错误
    // console.log("test");
    ElMessage({
        type: 'error',
        // 一般返回非200的错误都是服务器错误
        message: "用户名或密码错误",
        duration: 2 * 1000
    })

    return error.response.data.error
})

// 暴露get请求和post请求
export const get = (url, data) => {
    return services.get(url, data)
}


export const post = (url, data) => {
    return services.post(url, data);
}