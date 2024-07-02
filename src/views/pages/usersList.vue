<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="page-content">
      <div class="flex">
        <div class="input_box">
          <el-input
            v-model="params.query"
            style="max-width: 600px"
            placeholder="请输入关键字"
            class="input-with-select"
          >
            <template #append>
              <el-button :icon="Search" @click="handleSearch"
                ><el-icon><Search /></el-icon
              ></el-button>
            </template>
          </el-input>
        </div>
        <el-button type="primary" @click="handleAddUser">新增用户</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="username" label="姓名" width="180" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="roles" label="角色" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <el-switch
                v-model="scope.row.status"
                @click="handleStatusChange(scope.row)"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" @click="handleEditUser(scope.row)"
              >编辑</el-button
            >
            <el-button type="danger" @click="handleDeleteUser(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        id="el-query-page"
        background
        layout="prev, pager, next, jumper, ->, total"
        :total="total"
        v-model:current-page="params.pageNum"
        :page-size="params.pageSize"
        @current-change="handleSearch"
      />
    </div>

    <el-dialog v-model="dialogVisible" title="新增用户">
      <el-form
        :model="formData"
        label-width="auto"
        style="max-width: 600px"
        :rules="rules"
        ref="userForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="formData.password"
            placeholder="请输入密码"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            type="email"
            v-model="formData.email"
            placeholder="请输入邮箱"
          />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入手机号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="flex">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAddUserSubmit(userForm)">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="dialogVisible2" title="编辑用户">
      <el-form
        :model="formData2"
        label-width="auto"
        style="max-width: 600px"
        :rules="rules"
        ref="userForm2"
      >
        <el-form-item label="邮箱" prop="email">
          <el-input
            type="email"
            v-model="formData2.email"
            placeholder="请输入邮箱"
          />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="formData2.phone" placeholder="请输入手机号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="flex">
          <el-button @click="dialogVisible2 = false">取消</el-button>
          <el-button type="primary" @click="handleEditUserSubmit(userForm2)">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { onMounted, reactive, toRefs, ref } from "vue";
import axios from "axios";
export default {
  name: "usersList",
  setup() {
    const state = reactive({
      keyword: "",
      params: {
        query: "",
        pageSize: 5,
        pageNum: 1,
      },
      tableData: [],
      // 控制对话框的显示和隐藏
      dialogVisible: false,
      dialogVisible2: false,
      formData: {
        username: "",
        password: "",
        email: "",
        phone: "",
      },
      formData2: {
        email: "",
        phone: "",
        username: "",
      },
      total: 0,
      rules: {
        username: [
          { required: true, message: "此项为必填项", trigger: "blur" },
        ],
        password: [
          {
            required: true,
            message: "此项为必填项",
            trigger: "blur",
          },
        ],
        email: [
          {
            required: false,
            message: "请输入正确的邮箱",
            trigger: "blur",
            pattern: /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
          },
        ],
        phone: [
          {
            required: false,
            message: "请输入正确的手机号",
            trigger: "blur",
            pattern: /^1[3-9]\d{9}$/,
          },
        ],
      },
    });

    const handleDeleteUser = (row) => {
      // console.log(row);
      const services = axios.create({
        timeout: 5000,
        baseURL: "http://localhost:8081/",
        headers: {
          "Content-type": "application/json;charset=UTF-8",
        },
      });

      services.post("/deleteUser", row).then((res) => {
        console.log(res);
        // 刷新用户列表
        handleSearch();
        // 刷新用户列表总数
        getTotal();
      });
    };

    const handleEditUserSubmit = (formElement) => {
      formElement.validate((valid) => {
        if (valid) {
          const services = axios.create({
            timeout: 5000,
            baseURL: "http://localhost:8081/",
            headers: {
              "Content-type": "application/json;charset=UTF-8",
            },
          });

          services.post("/editUser", state.formData2).then((res) => {
            console.log(res);
            // 隐藏对话框
            state.dialogVisible2 = false;
            // 刷新用户列表
            handleSearch();
          });
        } else {
          return;
        }
      });
    };

    const handleEditUser = (formData) => {
      // console.log(formData);

      state.formData2.username = formData.username;
      state.formData2.email = formData.email;
      state.formData2.phone = formData.phone;
      state.dialogVisible2 = true;
    };

    const handleStatusChange = (row) => {
      // console.log(row);
      // console.log(state.formData);
      const services = axios.create({
        timeout: 5000,
        baseURL: "http://localhost:8081/",
        headers: {
          "Content-type": "application/json;charset=UTF-8",
        },
      });

      services.post("/changeStatus", row).then((res) => {
        // 刷新用户列表
        handleSearch();
      });
    };

    const handleAddUserSubmit = (formElement) => {
      // 表单验证
      formElement.validate((valid) => {
        if (valid) {
          // 提交表单
          // alert("提交成功");
          const services = axios.create({
            timeout: 5000,
            baseURL: "http://localhost:8081/",
            headers: {
              "Content-type": "application/json;charset=UTF-8",
            },
          });

          services.post("/addUser", state.formData).then((res) => {
            console.log(res);
            // 隐藏对话框
            state.dialogVisible = false;
            // 清空表单数据
            state.formData = {
              username: "",
              password: "",
              email: "",
              phone: "",
            };
            // 刷新用户列表
            handleSearch();
            // 刷新用户列表总数
            getTotal();
          });
        } else {
          return;
        }
      });
    };

    const handleSearch = () => {
      const services = axios.create({
        timeout: 5000,
        baseURL: "http://localhost:8081/",
        headers: {
          "Content-type": "application/json;charset=UTF-8",
        },
      });

      services.post("/users", state.params).then((res) => {
        state.tableData = res.data.users.map((userArray) => ({
          username: userArray[0],
          email: userArray[1],
          phone: userArray[2],
          roles: userArray[3],
          status: userArray[4] === "true", // 将字符串'true'转换为布尔值
        }));
        console.log(state.tableData);
      });
    };

    const handleAddUser = () => {
      state.dialogVisible = true;
    };

    // 获取用户列表总数
    const getTotal = () => {
      const services = axios.create({
        timeout: 5000,
        baseURL: "http://localhost:8081/",
        headers: {
          "Content-type": "application/json;charset=UTF-8",
        },
      });

      services.post("/usersCount").then((res) => {
        console.log(res.data.count);
        state.total = res.data.count;
      });
    };

    onMounted(() => {
      // 初始化-获取用户列表
      handleSearch();
      // 获取用户列表总数
      getTotal();
    });

    const userForm = ref(null);
    const userForm2 = ref(null);

    return {
      ...toRefs(state),
      handleSearch,
      handleAddUser,
      handleAddUserSubmit,
      userForm,
      userForm2,
      getTotal,
      handleStatusChange,
      handleEditUser,
      handleEditUserSubmit,
      handleDeleteUser,
    };
  },
};
</script>

<style scoped>
.input_box {
  width: 200px;
  margin-right: 20px;
}

#el-query-page {
  margin-top: 20px;
}
</style>

