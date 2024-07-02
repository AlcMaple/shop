<template>
  <div>
    <el-card class="box-card">
      <h2>注册</h2>
      <el-form
        :model="ruleForm"
        status-icon
        :rules="rules"
        ref="ruleForm"
        label-position="left"
        label-width="80px"
        class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="ruleForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
          <el-input
            type="password"
            v-model="ruleForm.pass"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="password">
          <el-input
            type="password"
            v-model="ruleForm.password"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <!-- 手机号 -->
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="ruleForm.phone"></el-input>
        </el-form-item>
        <!-- 验证码 -->
        <el-form-item label="验证码" prop="checkPass">
          <el-input v-model="ruleForm.checkPass" maxlength="4"></el-input>
        </el-form-item>
        <el-button
          style="margin:5px;margin-left:80px;"
          type="primary"
          @click="getCheckCode"
          :disabled="isButtonDisabled"
          >{{ ruleForm.time }}</el-button
        >
      </el-form>
      <div class="btnGroup">
        <el-button type="primary" @click="submitForm('ruleForm')"
          >提交</el-button
        >
        <el-button @click="resetForm('ruleForm')">重置</el-button>
        <el-button @click="goBack">返回</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    var validatePhone = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入手机号"));
      } else if (!/^1[34578]\d{9}$/.test(value)) {
        callback(new Error("手机号格式不正确!"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        username: "",
        pass: "",
        password: "",
        phone: "",
        time: "获取验证码",
        // 验证码
        checkPass: "",
      },
      isButtonDisabled: false,
      rules: {
        username: [
          { required: true, message: "用户名不能为空！", trigger: "blur" },
        ],
        pass: [{ required: true, validator: validatePass, trigger: "blur" }],
        password: [
          { required: true, validator: validatePass2, trigger: "blur" },
        ],
        phone: [{ required: true, validator: validatePhone, trigger: "blur" }],
        checkPass: [
          { required: true, message: "验证码不能为空！", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    submitForm(formName) {
      // console.log(formName);
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const requestData = {
            username: this.ruleForm.username,
            password: this.ruleForm.password,
            phone: this.ruleForm.phone,
            checkPass: this.ruleForm.checkPass,
          };

          console.log(requestData);

          // 向正确的端点发送POST请求
          this.axios
            .post("http://127.0.0.1:8081/sign", requestData, {
              headers: {
                "Content-Type": "application/json",
              },
            })
            .then((res) => {
              if (res.data.code === "200") {
                this.$message.success(res.data.msg);
              } else {
                this.$message.warning(res.data.msg);
              }
            })
            .catch((error) => {
              console.error("提交表单出错:", error);
            });
        } else {
          console.log("提交出错!!");
          return false;
        }
      });
    },

    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    goBack() {
      this.$router.go(-1);
    },

    getCheckCode() {
      // 获取验证码
      // 向正确的端点发送POST请求
      this.axios
        .post("http://127.0.0.1:8081/sendSms", {
          phone: this.ruleForm.phone,
        })
        .then((res) => {
          if (res.data.code === "200") {
            this.$message.success(res.data.msg);
          } else {
            this.$message.warning(res.data.msg);
          }
        })
        .catch((error) => {
          console.error("获取验证码出错:", error);
        });

      // 验证码倒计时
      this.ruleForm.time = "60秒后重试";

      // 禁用按钮，防止用户多次点击获取验证码
      this.isButtonDisabled = true; // 禁用按钮

      // 验证码倒计时
      var timer = setInterval(() => {
        this.ruleForm.time = parseInt(this.ruleForm.time) - 1 + "秒后重试";
        if (this.ruleForm.time === "0秒后重试") {
          clearInterval(timer);
          this.ruleForm.time = "获取验证码";
          this.isButtonDisabled = false; // 启用按钮
        }
      }, 1000);
    },
  },
};
</script>

<style scoped>
.box-card {
  margin: auto auto;
  width: 400px;
}
.login-from {
  margin: auto auto;
}
</style>