<template>
  <h1>Hello World</h1>
  <!-- 推荐使用第二种，简写的方式 -->

  <!-- 第一种，v-text -->
  <!-- <p v-text="data.name"></p> -->
  <p v-text="name"></p>

  <!-- <p>{{data.age}}</p> -->
  <p>{{ age }}</p>

  <p>{{ info }}</p>
  <p v-html="info"></p>

  <!-- v-bind:属性名="变量名":绑定动态的标签属性 -->
  <!-- v-bind的简写方式 :属性名="变量名" -->
  <p v-bind:data="dataVal">我有属性data</p>

  <!-- class类名绑定 -->
  <!-- 定义类名，如果isRed为true，则添加red类名 -->
  <p :class="{ red: isRed }">我是红色的</p>
  <p class="text" :class="{ red: !isRed }">我是红色的</p>
  <p class="text" :class="{ red: isRed }">我是红色的</p>

  <!-- 判断语句 v-if，值为true则标签存在 -->
  <!-- v-show，值为true，则标签显示 -->
  <p v-if="isTrue">我是if存在</p>
  <p v-show="isTrue">我是show展示</p>

  <p v-if="!isTrue">我是if存在</p>
  <p v-show="!isTrue">我是show展示</p>

  <!-- v-if与v-else要同级，中间不能有其他元素 -->
  <p v-if="isFalse">if</p>
  <p v-else>else</p>

  <!-- for循环，v-for=(每一个对象的变量，下标) in 数组 -->
  <ul>
    <!-- 添加key，是因为vue要求每一个数据都有一个唯一的标符，方便你后续更改数据它能自动匹配（比如更改第一个数据，它对应的会更改后并渲染到模板中） -->
    <li v-for="(item, index) in userList" :key="index">
      学生姓名：{{ item.username }} 学生年龄：{{ item.userage }}
    </li>
  </ul>
</template>

<script>
import { reactive, toRefs } from "vue";
export default {
  name: "home",
  // 生命周期函数，相当于beforeCreate、created
  setup() {
    // vue采用的是响应数据，而不是直接变量
    // 通过reactive声明一个对象数据
    const data = reactive({
      name: "小红",
      age: 20,
      info: "<i>这是一段斜体文字</i>",
      dataVal: 2,
      isRed: true,
      isTrue: true,
      isFalse: false,
      userList: [
        {
          username: "小明",
          userage: 10,
        },
        {
          username: "小w",
          userage: 20,
        },
        {
          username: "小c",
          userage: 30,
        },
        {
          username: "小d",
          userage: 40,
        },
      ],
    });

    // 声明的数据，需要return才能使用
    return {
      // data

      // 响应式数据无法直接使用扩展运算符，需要使用toRefs
      // 通过使用toRefs，使其简单，相当于扩展运算符...data
      ...toRefs(data),
    };
  },
};
</script>

<style>
.red {
  color: red;
}
</style>