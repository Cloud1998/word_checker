package com.example.demo.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.demo.entity.City;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface CityMapper extends BaseMapper<City> {
    @Select("SELECT COUNT(*) FROM city WHERE name = #{name}")
    int isCity(String name);
}
