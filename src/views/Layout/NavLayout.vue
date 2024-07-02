<template>
  <div class="common-layout">
    <el-container>
      <el-header class="common-header flex-float">
        <div class="flex">
          <img class="logo" src="../../assets/logo.png" alt="" />
          <h1 class="title">商铺后台管理系统</h1>
        </div>

        <!-- 使用element-plus的按钮组件 -->
        <el-button type="danger" @click="logout">退出</el-button>
      </el-header>
      <el-container>
        <el-aside width="200px" class="common-aside">
          <!-- 使用element-plus的菜单组件 -->
          <!-- :router="true"，开启路由功能，使得下面的index属性可以直接跳转到对应的页面（相当于vue-router的<router-link>） -->
          <el-menu background-color="none" text-color="#fff" :router="true">
            <!-- 一级导航，默认不跳转（不具备导航功能），index="1"作为id标识 -->
            <el-sub-menu index="1">
              <!-- #title是一个插槽，可以自定义标题内容（这里是标题内容为账号管理） -->
              <template #title>
                <el-icon><User /></el-icon>
                <span>账号管理</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/user">账号列表</el-menu-item>
              </el-menu-item-group>
            </el-sub-menu>

            <el-sub-menu index="2">
              <template #title>
                <el-icon><Box /></el-icon>
                <span>角色管理</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/roles">角色列表</el-menu-item>
              </el-menu-item-group>
            </el-sub-menu>

            <el-sub-menu index="3">
              <template #title>
                <el-icon><Box /></el-icon>
                <span>商品管理</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/goods">商品列表</el-menu-item>
              </el-menu-item-group>
            </el-sub-menu>
          </el-menu>
        </el-aside>
        <!-- 内容 -->
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import { useStore } from "vuex";
export default {
  name: "NavLayout",
  setup() {
    const router = useRouter();
    const store = useStore();

    const logout = () => {
      // 退出登录
      localStorage.removeItem("userLogin");
      store.commit("user/logout", {});

      router.push("/login");
    };

    return {
      logout,
    };
  },
};
</script>

<style scoped>
.el-container {
  height: 100vh;
  overflow: hidden;
}

.common-header {
  background: rgb(39, 45, 53);
}

.common-aside {
  background: rgb(48, 55, 65);
}

.logo {
  width: 80px;
}

.title {
  color: #fff;
}

.el-main {
  background: #efefef;
}
</style>