import { createStore } from 'vuex'
import count from './state/count.js'
import userLogin from './state/userLogin.js'

export default createStore({
  // 将state数据分模块管理,通过文件对state进行分割,应用到各个页面
  modules: {
    // => count:count
    count,
    userLogin
  }


})
