<template>
  <div class="about">
    <h2>vue3的生命周期</h2>
    <div id="mount">{{ name }} --- {{ num }}</div>
  </div>
</template>

<script>
import {
  reactive,
  toRefs,
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
} from "vue";

export default {
  name: "AboutView",
  setup() {
    const data = reactive({
      name: "mounted",
      name2: "mounted2",
      num: 0,
    });

    // DOM渲染前
    onBeforeMount(() => {
      console.log("beforeMount：", document.getElementById("mount"));
    });

    // DOM渲染后
    onMounted(() => {
      console.log("mounted：", document.getElementById("mount"));

      setTimeout(() => {
        data.name = "updated";
        // 不会触发，因为页面没有这个数据，所以不会更新
        data.name2 = "updated2";
      }, 2000);
    });

    // 数据更新前
    onBeforeUpdate(() => {
      console.log("beforeUpdate-DOM：", document.getElementById("mount"));
      console.log(
        "beforeUpdate：",
        document.getElementById("mount").textContent
      );
    });

    // 数据更新后
    onUpdated(() => {
      console.log("updated-DOM：", document.getElementById("mount"));
      console.log("updated：", document.getElementById("mount").textContent);
      // 如果页面上有这个数据，则不能在更新区域更新，否则会造成死循环
      // data.num++;
    });

    return {
      ...toRefs(data),
    };
  },
};
</script>
