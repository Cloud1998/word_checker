package com.example.demo.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.demo.entity.Province;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface ProvinceMapper extends BaseMapper<Province> {
    @Select("SELECT COUNT(*) FROM province WHERE name = #{name}")
    int isProvince(String name);
}