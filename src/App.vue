<template>
  <router-view />
</template>

<style>
body,
html {
  padding: 0;
  margin: 0;
}

/** flex布局类名 */
.flex-float {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.flex {
  display: flex;
  align-items: center;
}

.page-content {
  box-sizing: border-box;
  display: block;
  width: 100%;
  padding: 20px;
  background: #fff;
  margin-top: 30px;
}
</style>
