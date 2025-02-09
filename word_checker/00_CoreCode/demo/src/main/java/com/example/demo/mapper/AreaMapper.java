package com.example.demo.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.demo.entity.Area;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface AreaMapper extends BaseMapper<Area> {
    @Select("SELECT COUNT(*) FROM area WHERE name = #{name}")
    int isArea(String name);
}