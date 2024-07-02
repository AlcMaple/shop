export default {
    namespaced: true, // 命名空间,防止命名冲突

    // 初始化全局状态,刷新页面会再次进行初始化
    state: {
        count: 0,
    },
    // 计算state,无需在各个页面进行判断,通过getters获取true/false值
    getters: {
        getCount(state) {
            return state.count > 10
        }
    },
    // 更新state,唯一方法:commit mutations,使用时需要传递参数
    mutations: {
        // 第一个参数为state,第二个参数是传递的变量
        setCount(state, count) {
            state.count = count
        }
    },
    // 允许异步操作,可以返回promise,修改state值仍然需要使用commit mutations
    actions: {
        // 第一个参数为state上下文context,第二个参数是传递的变量
        setCountPromise(context, count) {
            return new Promise((resolve, reject) => {
                if (count > 100) {
                    return reject('count不能大于100')
                } else {
                    // 第一个参数是mutations的方法名
                    context.commit('setCount', count)
                    resolve()
                }
            })
        }
    },
}
