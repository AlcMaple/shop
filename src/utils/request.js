import { get, post } from '@/utils/services'

export const loginAPI = (data) => {
    return post('/login', data);
}

export const getUserInfoAPI = (data) => {
    return get('/users', data);
}