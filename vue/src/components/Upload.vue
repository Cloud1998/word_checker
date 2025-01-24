<template>
  <div>
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
        <div class="content-container">
          <!-- 步骤 1：上传项目信息 -->
          <div v-if="active === 0">
            <!-- 表单 -->
            <h2 class="step-title">{{steps[active].description}}</h2>
            <el-form 
              ref="formRef"
              :model="form"
              :rules="formRules"
              size="large"
              style="max-width: 600px"
              label-width="auto"
              label-position="right"
            >
              <el-form-item label="地域信息" prop="region">
                <el-cascader v-model="form.region" :options="regionOptions"
                  placeholder="请选择省、市、区" expand-trigger="hover" filterable clearable />
              </el-form-item>
              <el-form-item label="装机容量" prop="capacity">
                <el-input-number v-model.number="form.capacity" :min="0" :step="50" >
                  <template #suffix>
                    <span>MW</span>
                  </template>
                </el-input-number>
              </el-form-item>
              <!-- 文件 -->
              <div class="upload-container">
                <label>上传报告</label>
                <el-upload
                class="upload"
                drag
                action="http://localhost:8080/api/upload"
                v-model:file-list="fileList"
                >
                  <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                  <div class="el-upload__text">
                    拖拽上传或 <em>单击上传</em>
                  </div>
                  <template #tip>
                    <div class="el-upload__tip">
                      每次只能上传1个不超过10MB的docx文件。
                    </div>
                  </template>
                </el-upload>
              </div>
            </el-form>
            <div class="submit-container">
              <el-button @click="submitForm">提交</el-button>
            </div>
          </div>
          <!-- 步骤 2：后台文件处理 -->
          <div v-if="active === 1">
            <h2 class="step-title">{{steps[active].description}}</h2>
            <div class="step-content">
              <div class="demo-progress">
              <el-progress type="dashboard" :percentage="percentage" :color="colors" />
            </div>
            </div>
          </div>
          <!-- 步骤 3：文件下载 -->
          <div v-if="active === 2">
            <h2 class="step-title">{{steps[active].description}}</h2>
            <div class="step-content">
              <p>点击下载</p>
            </div>
          </div>
        </div>
      </el-main>
      <el-footer>
        <!-- 步骤显示区域 -->
        <el-steps class="steps" :active="active" finish-status="success" align-center>
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
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus';
// 地域信息
import regionOptions from '@/assets/PCA.json'
// 表单引用
const formRef = ref();
// 表单数据
const form = reactive({
  region: [],
  capacity: 0
});
// 表单验证规则
const formRules = ref({
  region: [
    { required: true, message: '请选择地域信息', trigger: 'change' }
  ],
});
// 提交表单方法
const submitForm = async () => {
  const valid = await formRef.value.validate();
  if (valid) {
    ElMessage.success('表单验证通过');
    console.log('表单数据：', form.value);
  } else {
    ElMessage.error('表单验证失败，请检查输入');
  }
};

// 文件列表
const fileList = ref([
  {
    name: 'food.docx',
    url: ''
  }
])

// 进度条
const percentage = ref(0)
const colors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
]
onMounted(() => {
  setInterval(() => {
    percentage.value = (percentage.value % 100) + 10
  }, 500)
})

// 步骤
const active = ref(0)
// 步骤信息
const steps = [
  { title: 'Step 1', description: '上传项目信息' },
  { title: 'Step 2', description: '后台文件处理' },
  { title: 'Step 3', description: '处理结果下载' },
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
</script>
  
<style scoped lang="scss">
$font-family-base: Quotes, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
.el-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

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

.el-main {
  flex: 1;
  display: flex;
  justify-content: center;

  .content-container {
    margin-top: 0;
    // border: 1px solid;
    width: 100%;
    padding-left: 24px;
    .step-title {
      margin-top: 0;
      // display: flex;
      // justify-content: center;
    }
    .upload-container{
      width: 100%;

      label{
        font-size: 14px;
        font: Microsoft YaHei;
        color: rgb(96, 98, 102);
      }
    }
    .submit-container {
      display: flex;
      justify-content: center;
    }
  }
}

.el-footer {
  margin-top: auto;
  display: flex;
  justify-content: center;
  margin-bottom: 80px;

  .el-steps {
    flex: 1;
    max-width: 800px;
    min-width: 800px;
  }
}
</style>
  