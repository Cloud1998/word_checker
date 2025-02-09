import request from './request';

// 创建任务
export const createTask = (data) => {
  return request.post('/create-task', data);
};

// 获取进度
export const getProgress = (taskId) => {
  return request.get(`/progress/${taskId}`);
};

// 上传文件
export const uploadFile = (taskId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return request.post(`/upload?taskId=${taskId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};