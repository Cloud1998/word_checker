package com.example.demo.service;

import com.example.demo.exception.StorageException;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

@Service
public class FileStorageService {
    // 定义文件存储的根路径，所有文件和目录将存储在该路径下
    private final Path rootLocation;
    // 定义最大存储容量，单位为 MB，这里设置为 1GB
    private final long maxStorageMB = 1024;
    /**
     * 构造函数，用于初始化文件存储的根路径
     * @param rootLocation 文件存储的根路径
     */
    public FileStorageService(Path rootLocation) {
        // 将传入的根路径赋值给类的成员变量
        this.rootLocation = rootLocation;
    }
    /**
     * 检查当前存储空间的使用情况，确保未超过最大存储容量
     * 如果超过最大存储容量，将抛出 StorageException 异常
     */
    public void checkStorage() {
        // 调用 getUsedSpaceMB 方法获取当前已使用的存储空间，单位为 MB
        long usedMB = getUsedSpaceMB();
        // 检查已使用的存储空间是否超过最大存储容量
        if (usedMB > maxStorageMB) {
            // 如果超过最大存储容量，抛出 StorageException 异常，并附带已使用的存储空间信息
            throw new StorageException("存储空间不足，已使用 " + usedMB + "MB");
        }
    }
    /**
     * 计算根路径下所有文件所占用的存储空间，单位为 MB
     * @return 已使用的存储空间，单位为 MB
     */
    private long getUsedSpaceMB() {
        try {
            // 使用 Files.walk 方法遍历根路径下的所有文件和目录
            return Files.walk(rootLocation)
                    // 将 Path 对象转换为 File 对象
                    .map(Path::toFile)
                    // 过滤出所有文件（排除目录）
                    .filter(File::isFile)
                    // 获取每个文件的长度（字节数）
                    .mapToLong(File::length)
                    // 对所有文件的长度求和
                    .sum()
                    // 将字节数转换为 MB
                    / (1024 * 1024);
        } catch (IOException e) {
            // 如果在遍历文件过程中发生 I/O 异常，抛出 StorageException 异常，并附带异常信息
            throw new StorageException("无法计算存储空间", e);
        }
    }
    /**
     * 定时任务，每小时执行一次，用于清理过期的文件和目录
     * 使用 @Scheduled 注解，fixedRate 属性指定任务执行的间隔时间，这里设置为 1 小时（3600000 毫秒）
     */
    @Scheduled(fixedRate = 3600000)
    public void cleanupExpiredFiles() {
        // 获取根路径下的所有子目录和文件
        File[] taskDirs = rootLocation.toFile().listFiles();
        // 如果根路径下没有子目录和文件，直接返回
        if (taskDirs == null) return;
        // 计算 1 小时前的时间戳，作为过期时间的截止点
        long cutoff = System.currentTimeMillis() - 3600000;
        // 遍历根路径下的所有子目录和文件
        for (File dir : taskDirs) {
            // 检查当前对象是否为目录，并且最后修改时间早于过期时间截止点
            if (dir.isDirectory() &&
                    dir.lastModified() < cutoff) {
                // 如果是过期的目录，调用 deleteDirectory 方法删除该目录及其所有子文件和子目录
                deleteDirectory(dir);
            }
        }
    }
    /**
     * 递归删除指定目录及其所有子文件和子目录
     * @param dir 要删除的目录
     */
    private void deleteDirectory(File dir) {
        // 获取指定目录下的所有子文件和子目录
        File[] files = dir.listFiles();
        // 如果目录下有子文件和子目录
        if (files != null) {
            // 遍历所有子文件和子目录
            for (File f : files) {
                // 删除每个子文件和子目录
                f.delete();
            }
        }
        // 删除指定目录
        dir.delete();
    }
}
