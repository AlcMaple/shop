const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // 关闭非必要的错误提示
  lintOnSave: false,

  // 解决跨域问题:前端使用代理服务器
  // 开启代理服务器
  devServer: {
    // 代理服务器可以将路由中的指定前缀转发到指定的后端服务器中
    proxy: {
      '/api': {
        // 假设项目的后端地址：http://localhost:8081
        target: 'http://localhost:8081',
        ws: true, // 是否启用websockets
        changeOrigin: true,  // 代理时是否更改host
        // 用于辅助重写请求后端的路径
        pathRewrite: {
          // 代理服务器请求后端时，将地址中的/api转换成空
          '^/api': '' //这里理解成用'/api'代替target里面的地址
        }
      }
    }
  }
})