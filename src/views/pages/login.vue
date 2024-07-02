<template>
  <div class="login_wrap">
    <div class="form_wrap">
      <!-- ref：获取dom元素 -->
      <el-form
        ref="formRef"
        style="max-width: 600px"
        :model="dynamicValidateForm"
        label-width="auto"
        class="demo-dynamic"
      >
        <!-- :rules：正则表达式验证 -->
        <!-- prop：表单域的名称，对应表单的data中的属性名。与下面的v-model对应 -->
        <el-form-item
          prop="username"
          label="账号"
          :rules="[
            {
              required: true,
              message: '此项为必填项',
              // 触发条件: 输入框失去焦点时
              trigger: 'blur',
            },
          ]"
        >
          <el-input v-model="dynamicValidateForm.username" />
        </el-form-item>

        <el-form-item
          prop="password"
          label="密码"
          :rules="[
            {
              required: true,
              message: '此项为必填项',
              // 触发条件: 输入框失去焦点时
              trigger: 'blur',
            },
          ]"
        >
          <el-input type="password" v-model="dynamicValidateForm.password" />
        </el-form-item>

        <!-- 忘记密码和手机号登录的跳转 -->

        <div class="other_login">
          <el-button type="text" size="small" @click="handleForgetPwd">
            忘记密码
          </el-button>
          <el-button type="text" size="small" @click="handlePhoneLogin">
            手机号登录
          </el-button>
        </div>

        <el-button type="primary" class="login_btn" @click="handleLogin"
          >登录</el-button
        >

        {{ count }}
      </el-form>
    </div>
  </div>
</template>

<script>
import { toRefs, reactive } from "vue";
// 导入useStore
import { useStore } from "vuex";
// 路由跳转
import { useRouter } from "vue-router";
import { loginAPI } from "@/utils/request";

export default {
  name: "login",
  setup() {

    

    // 路由跳转
    const router = useRouter();

    // 使用useStore
    const store = useStore();
    // 监听count
    // const count = store.state.count.count;

    const data = reactive({
      dynamicValidateForm: {
        username: "",
        password: "",
      },

      // count: count,
    });

    const handleLogin = () => {
      // 调用登录接口
      loginAPI(data.dynamicValidateForm)
        .then((res) => {
          // 登录成功
          // console.log(res);
          if (res == "用户名或密码错误") {
            return;
          }
          store.commit("userLogin/setUInfo", data.dynamicValidateForm);
          localStorage.setItem(
            "userLogin",
            JSON.stringify(data.dynamicValidateForm)
          );

          // 路由跳转
          router.push("/");
        })
        .catch((err) => {
          // console.log(err);
        });

      // store.commit("userLogin/setUInfo", data.dynamicValidateForm);
      // localStorage.setItem(
      //   "userLogin",
      //   JSON.stringify(data.dynamicValidateForm)
      // );

      // // 路由跳转
      // router.push("/user");
    };

    // console.log("count修改前：", store.getters["count/getCount"]);
    // const handleLogin = () => {
    //   // store.commit("setCount",5);

    //   // 使用store.dispatch提交action
    //   store
    //     .dispatch("count/setCountPromise", 50)
    //     .then((res) => {
    //       console.log(store.state.count.count);
    //       alert("修改成功");
    //       console.log("count修改后：", store.getters["count/getCount"]);
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //     });
    // };

    return {
      ...toRefs(data),
      handleLogin,
    };
  },
};
</script>

<style scoped>
.login_wrap {
  width: 100%;
  height: 100vh;
  background: rgb(56, 86, 139);
  position: relative;
}

.form_wrap {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  padding: 30px 50px;
  border-radius: 5px;
}

.login_btn {
  display: block;
  margin: 10px auto;
}

.other_login {
  display: flex;
  justify-content: space-between;
}
</style>