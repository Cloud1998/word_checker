package com.example.demo.config;

import com.example.demo.exception.StorageException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.Semaphore;

// 该注解表明这是一个配置类，Spring会自动扫描并加载该类中的配置信息
@Configuration
public class FileStorageConfig {
    // 使用 @Value 注解从配置文件中读取 "file.upload-dir" 属性的值，
    // 如果配置文件中未配置该属性，则使用默认值 "./uploads"
    // uploadDir 用于存储文件上传的目录路径
    @Value("${file.upload-dir:./uploads}")
    private String uploadDir;

    // 使用 @Value 注解从配置文件中读取 "file.max-concurrent-tasks" 属性的值，
    // 如果配置文件中未配置该属性，则使用默认值 10
    // maxConcurrentTasks 表示允许的最大并发文件上传任务数
    @Value("${file.max-concurrent-tasks:10}")
    private int maxConcurrentTasks;

    // @Bean 注解表示该方法会返回一个对象，并将其注册为 Spring 容器中的一个 bean
    // fileStorageLocation 方法用于创建文件存储的目录，并返回该目录的 Path 对象
    @Bean
    public Path fileStorageLocation() {
        // 将上传目录路径转换为绝对路径并进行规范化处理
        Path path = Paths.get(uploadDir).toAbsolutePath().normalize();
        try {
            // 创建上传目录，如果目录已经存在则不会重复创建
            Files.createDirectories(path);
            // 返回创建好的目录的 Path 对象
            return path;
        } catch (IOException ex) {
            // 如果创建目录时发生 I/O 异常，则抛出异常
            throw new StorageException("无法创建上传目录", ex);
        }
    }

    // @Bean 注解表示该方法会返回一个对象，并将其注册为 Spring 容器中的一个 bean
    // concurrencySemaphore 方法用于创建一个 Semaphore 对象，用于控制并发任务的数量
    @Bean
    public Semaphore concurrencySemaphore() {
        // 创建一个 Semaphore 对象，初始许可数量为 maxConcurrentTasks
        return new Semaphore(maxConcurrentTasks);
    }
}