export default {
    namespaced: true,

    state: {
        userLogin: (localStorage.getItem('userLogin') && JSON.parse(localStorage.getItem('userLogin'))) || {},
    },
    // 计算state,无需在各个页面进行判断,通过getters获取true/false值
    getters: {

    },
    // 更新state,唯一方法:commit mutations,使用时需要传递参数
    mutations: {
        // 第一个参数为state,第二个参数是传递的变量
        setUInfo(state, uInfo) {
            state.userLogin = uInfo;
        }
    },
}