<template>
  <div class="common-layout">
    <el-container>
      <el-header class="nav-bar">
        <div class="container">
          <a href="/" class="bar-title" rel="noopener">
            <img src="../assets/logo.svg" class="logo" viewBox="0 0 128 128" width="24" height="24"></img>
            <span class="text">WordChecker</span>
          </a>
          <div class="content">
            <nav class="menu">
              <a href="/upload" class="nav-bar-menu-link" rel="noopener noreferrer">上传</a>
            </nav>
          </div>
        </div>
      </el-header>
      <el-main>
        <div class="step-content">
          <!-- 步骤 1：填写项目信息 -->
          <div v-if="active === 0">
            <h2>请选择项目所在的省市区</h2>
            <el-cascader v-model="selectedRegion" :options="regionOptions" :props="cascaderProps" placeholder="请选择省、市、区"
              expand-trigger="hover" filterable clearable />
          </div>
          <!-- 步骤 2：上传可研报告 -->
          <div v-if="active === 1">
            <h2>上传可研报告</h2>

          </div>
          <!-- 步骤 3：后台文件处理 -->
          <div v-if="active === 2">
            <h2>后台文件处理</h2>

          </div>
          <!-- 步骤 4：处理结果下载 -->
          <div v-if="active === 3">
            <h2>处理结果下载</h2>

          </div>
        </div>
      </el-main>
      <el-footer>
        <!-- 步骤显示区域 -->
        <el-steps class="steps" style="max-width: 800px" :active="active" finish-status="success" align-center>
          <el-step v-for="(step, index) in steps" :key="index" :title="step.title" :description="step.description"
            @click="toggleHandler(index)" style="cursor: pointer;">
          </el-step>
        </el-steps>
      </el-footer>
    </el-container>
  </div>
  <div>
  </div>
</template>
  
<script setup>
import { ref } from 'vue'

const active = ref(0)
const steps = [
  { title: 'Step 1', description: '填写项目信息' },
  { title: 'Step 2', description: '上传可研报告' },
  { title: 'Step 3', description: '后台文件处理' },
  { title: 'Step 4', description: '处理结果下载' },
];

// 步骤切换
const toggleHandler = (index) => {
  switch (index) {
    case 0:
      active.value = 0;
      break;
    case 1:
      active.value = 1;
      break;
    case 2:
      active.value = 2;
      break;
    case 3:
      active.value = 3;
      break;
    default:
      console.log('未知步骤');
  }
}


const test = () => alert("test")
</script>
  
<style scoped lang="scss">
$font-family-base: Quotes, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;

.nav-bar {
  font-family: $font-family-base;
  letter-spacing: .2px;
  line-height: 24px;
  font-size: 16px;
  font-weight: 400;
  color: #213547;
  direction: ltr;
  overflow-wrap: break-word;
  text-rendering: unset !important;
  font-synthesis: unset !important;
  box-sizing: border-box;
  position: relative;
  border-bottom: 1px solid rgba(60, 60, 60, 0.12);
  height: 55px;
  background-color: #ffffff;
  white-space: nowrap;
  transition: border-color .5s, background-color .5s;
  padding: 0 32px;

  a {
    color: inherit;
    text-decoration: inherit;
    touch-action: manipulation;
    background-color: transparent;
  }

  img {
    display: block;
    vertical-align: middle;
  }
}

.container {
  display: flex;
  justify-content: space-between;
  margin: 0 auto;
  max-width: 1376px;
}

.bar-title {
  display: flex;
  align-items: center;
  padding-top: 1px;
  height: 55px;
  transition: opacity .25s;
}

.logo {
  position: relative;
}

.text {
  font-size: 16px;
  font-weight: 500;
}

.logo+.text {
  padding-left: 8px;
}

.content {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex-grow: 1;

  .menu {
    display: flex;
    align-items: center;
    padding-left: 16px;
    flex-grow: 1;
  }
}

.nav-bar-menu-link {
  display: block;
  padding: 0 12px;
  line-height: 54px;
  font-size: 13px;
  font-weight: 500;
  color: #213547;
  transition: color .25s;
  white-space: nowrap;

  &:hover {
    color: #42b883;
  }
}

.active {
  border-bottom: 1px solid #42b883;
}
</style>
  