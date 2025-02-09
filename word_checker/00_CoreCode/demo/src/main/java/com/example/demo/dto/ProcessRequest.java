package com.example.demo.dto;

public class ProcessRequest {
    private String region;    // 格式：省/市/区
    private Integer capacity; // 装机容量（MW）

    public ProcessRequest(String region, Integer capacity) {
        this.region = region;
        this.capacity = capacity;
    }

    public ProcessRequest() {
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
}