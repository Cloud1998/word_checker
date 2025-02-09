package com.example.demo.utils;

import com.example.demo.mapper.AreaMapper;
import com.example.demo.mapper.CityMapper;
import com.example.demo.mapper.ProvinceMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class StringUtils {

    @Autowired
    private ProvinceMapper provinceMapper;
    @Autowired
    private CityMapper cityMapper;
    @Autowired
    private AreaMapper areaMapper;

    /**
     * 检查字符串是否为 null 或空字符串
     * @param str 要检查的字符串
     * @return 如果字符串为 null 或空字符串，返回 true；否则返回 false
     */
    public boolean isNullOrEmpty(String str) {
        return str == null || str.isEmpty();
    }

    /**
     * 检查字符串是否为空白字符串（包含 null、空字符串和仅包含空格的字符串）
     * @param str 要检查的字符串
     * @return 如果字符串为空白字符串，返回 true；否则返回 false
     */
    public boolean isBlank(String str) {
        return isNullOrEmpty(str) || str.trim().isEmpty();
    }

    /**
     * 检查字符串是否为城市名
     * @param region 要检查的邮箱地址
     * @return 如果是有效的邮箱地址，返回 true；否则返回 false
     */
    public boolean isRegion(String region) {
        if (isBlank(region)) {
            return false;
        }
        return (provinceMapper.isProvince(region) == 1) || (cityMapper.isCity(region) == 1) || (areaMapper.isArea(region) == 1);
    }
}