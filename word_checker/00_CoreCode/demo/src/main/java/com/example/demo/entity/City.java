package com.example.demo.entity;

import com.baomidou.mybatisplus.annotation.TableName;

@TableName("city")
public class City {
    private String code;
    private String name;
    private String provincecode;

    public City(String code, String name, String provincecode) {
        this.code = code;
        this.name = name;
        this.provincecode = provincecode;
    }

    public City() {
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

    public String getProvincecode() {
        return provincecode;
    }

    public void setProvincecode(String provincecode) {
        this.provincecode = provincecode;
    }
}
