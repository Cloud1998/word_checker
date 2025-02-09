package com.example.demo.dto;

public class TaskProgress {
    // 任务id
    private String taskId;
    // 处理进度
    private int progress;     // 0-100
    // 地域信息
    private String region;
    // 装机容量
    private Integer capacity;
    // 错误提示
    private String errorMessage;

    public TaskProgress() {
    }

    public TaskProgress(String taskId, int progress) {
        this.taskId = taskId;
        this.progress = progress;
    }

    public TaskProgress(String taskId, int progress, String region, Integer capacity) {
        this.taskId = taskId;
        this.progress = progress;
        this.region = region;
        this.capacity = capacity;
    }

    public String getTaskId() {
        return taskId;
    }

    public void setTaskId(String taskId) {
        this.taskId = taskId;
    }

    public int getProgress() {
        return progress;
    }

    public void setProgress(int progress) {
        this.progress = progress;
    }

    public String getRegion() {
        return region;
    }

    public void setRegion(String region) {
        this.region = region;
    }

    public Integer getCapacity() {
        return capacity;
    }

    public void setCapacity(Integer capacity) {
        this.capacity = capacity;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}