<template>
  <div>
    <el-card class="box-card">
      <h2>手机号找回密码</h2>
      <el-form
        :model="ruleForm"
        status-icon
        :rules="rules"
        ref="ruleForm"
        label-position="left"
        label-width="80px"
        class="demo-ruleForm"
      >
        <!-- 手机号 -->
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="ruleForm.phone"></el-input>
        </el-form-item>
        <!-- 验证码 -->
        <el-form-item label="验证码" prop="checkPass">
          <el-input v-model="ruleForm.checkPass" maxlength="4"></el-input>
        </el-form-item>
        <el-button
          style="margin: 5px; margin-left: 80px"
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
      </div>
    </el-card>
  </div>
</template>