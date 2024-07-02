<template>
  <div>
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品列表</el-breadcrumb-item>
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
      </div>

      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="goods_name" label="商品名称" width="180" />
        <el-table-column prop="goods_price" label="价格（￥）" width="180" />
        <el-table-column prop="goods_weight" label="商品重量（kg）" />
        <el-table-column prop="goods_status" label="商品状态">
          <template #default="scope">
            <p>{{ scope.row.goods_status }}</p>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
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
  </div>
</template>

<script>
import { onMounted, reactive, toRefs, ref } from "vue";
import axios from "axios";
export default {
  name: "goodsList",
  setup() {
    const state = reactive({
      params: {
        query: "",
        pageSize: 5,
        pageNum: 1,
      },
      total: 0,
      tableData: [],
    });

    const handleSearch = () => {
      const services = axios.create({
        timeout: 5000,
        baseURL: "http://localhost:8081/",
        headers: {
          "Content-type": "application/json;charset=UTF-8",
        },
      });

      services.post("/goods", state.params).then((res) => {
        state.tableData = res.data.goods.map((userArray) => ({
          goods_name: userArray[1],
          goods_price: userArray[2],
          goods_weight: userArray[3],
          //   goods_status: userArray[5] === "true", // 将字符串'true'转换为布尔值
          goods_status:
            userArray[5] === 0
              ? "未通过"
              : userArray[5] === 1
              ? "审核中"
              : "已审核",
        }));
        console.log(state.tableData);
        // console.log(res);
      });
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

      services.post("/goodsCount").then((res) => {
        console.log(res.data.count);
        state.total = res.data.count;
        // console.log(res);
      });
    };

    onMounted(() => {
      getTotal();
      handleSearch();
    });

    return {
      ...toRefs(state),
      handleSearch,
      getTotal,
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