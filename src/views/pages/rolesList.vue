<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>角色列表</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="page-content">
      <el-button type="primary" @click="handleAddRole">新增角色</el-button>

      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="rolename" label="角色" width="auto" />
        <el-table-column prop="roledescription" label="描述" width="auto" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" @click="handleEditRole(scope.row)"
              >编辑</el-button
            >
            <el-button type="danger" @click="handleDeleteRole(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="formData.id ? '编辑角色' : '新增角色'"
    >
      <el-form
        :model="formData"
        label-width="auto"
        style="max-width: 600px"
        :rules="rules"
        ref="roleForm"
      >
        <el-form-item label="角色名" prop="rolename">
          <el-input v-model="formData.rolename" placeholder="请输入角色名" />
        </el-form-item>
        <el-form-item label="描述" prop="roledescription">
          <el-input
            v-model="formData.roledescription"
            placeholder="请输入描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="flex">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            @click="handleRoleSubmit(roleForm, formData)"
          >
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { reactive, toRefs, ref, onMounted } from "vue";
import axios from "axios";
import { ElLoading } from "element-plus";
export default {
  name: "rolesList",
  setup() {
    const data = reactive({
      tableData: [],
      // roleForm: {
      //   rolename: "",
      //   roledescription: "",
      // },
      dialogVisible: false,
      rules: {
        rolename: [
          { required: true, message: "此项为必填项", trigger: "blur" },
        ],
      },
      formData: {
        rolename: "",
        roledescription: "",
      },
      loadingInstance: null,
    });

    const handleRoleSubmit = (roleForm, formData) => {
      console.log(formData.id);
      if (formData.id) {
        handleEditRoleSubmit(roleForm);
        // console.log("编辑角色");
      } else {
        handleAddRoleSubmit(roleForm);
        // console.log("新增角色");
      }
    };

    const handleDeleteRole = (row) => {
      console.log(row);
      const services = axios.create({
        timeout: 5000,
        baseURL: "http://localhost:8081/",
        headers: {
          "Content-type": "application/json;charset=UTF-8",
        },
      });

      services.post("/deleteRole", row).then((res) => {
        console.log(res);
        getRoles();
      });
    };

    const handleEditRoleSubmit = (formData) => {
      formData.validate((valid) => {
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

          services.post("/editRole", data.formData).then((res) => {
            console.log(res);
            // 隐藏对话框
            data.dialogVisible = false;

            getRoles();
          });
        } else {
          return;
        }
      });
    };

    const handleAddRoleSubmit = (form) => {
      form.validate((valid) => {
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

          services.post("/addRole", data.formData).then((res) => {
            console.log(res);
            // 隐藏对话框
            data.dialogVisible = false;
            // 清空表单数据
            data.formData = {
              rolename: "",
              roledescription: "",
            };

            getRoles();
          });
        } else {
          return;
        }
      });
    };

    const handleAddRole = () => {
      data.dialogVisible = true;
      data.formData = {
        rolename: "",
        roledescription: "",
      };
    };

    const getRoles = () => {
      const services = axios.create({
        timeout: 5000,
        baseURL: "http://localhost:8081/",
        headers: {
          "Content-type": "application/json;charset=UTF-8",
        },
      });

      // 拦截请求，加载loading和统一处理
      services.interceptors.request.use((config) => {
        data.loadingInstance = ElLoading.service({
          lock: true,
          text: "Loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        return config;
      });

      // 拦截响应，关闭loading
      services.interceptors.response.use((response) => {
        data.loadingInstance.close();
        return response;
      });

      services.post("/roles").then((res) => {
        // console.log(res);
        data.tableData = res.data.roles.map((role) => ({
          id: role[0],
          rolename: role[1],
          roledescription: role[2],
        }));
        console.log(data.tableData);
      });
    };

    const handleEditRole = (row) => {
      const { id, rolename, roledescription } = row;
      data.formData = { id, rolename, roledescription };
      console.log(data.formData);
      data.dialogVisible = true;
    };

    onMounted(() => {
      getRoles();
    });

    const roleForm = ref(null);

    return {
      ...toRefs(data),
      getRoles,
      handleAddRole,
      handleAddRoleSubmit,
      roleForm,
      handleEditRole,
      handleRoleSubmit,
      handleEditRoleSubmit,
      handleDeleteRole,
    };
  },
};
</script>