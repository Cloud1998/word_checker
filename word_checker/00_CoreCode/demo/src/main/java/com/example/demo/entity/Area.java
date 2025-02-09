package com.example.demo.entity;

import com.baomidou.mybatisplus.annotation.TableName;

@TableName("area")
public class Area {
    private String code;
    private String name;
    private String citycode;
    private String provincecode;

    public Area(String code, String name, String citycode, String provincecode) {
        this.code = code;
        this.name = name;
        this.citycode = citycode;
        this.provincecode = provincecode;
    }

    public Area() {
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCitycode() {
        return citycode;
    }

    public void setCitycode(String citycode) {
        this.citycode = citycode;
    }

    public String getProvincecode() {
        return provincecode;
    }

    public void setProvincecode(String provincecode) {
        this.provincecode = provincecode;
    }
}
