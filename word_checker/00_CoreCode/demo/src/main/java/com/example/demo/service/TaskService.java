package com.example.demo.service;

import com.example.demo.dto.ProcessRequest;
import com.example.demo.dto.TaskProgress;
import com.example.demo.exception.StorageException;
import com.example.demo.utils.Highlighter;
import com.example.demo.utils.StringUtils;
import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.common.Term;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.Semaphore;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

// 该注解表明这是一个 Spring 服务类，用于处理业务逻辑
@Service
public class TaskService {
    @Autowired
    private StringUtils stringUtils;

    // 存储文件上传的根目录路径
    private final Path rootLocation;
    // 用于控制并发任务数量的信号量
    private final Semaphore semaphore;
    // 用于存储任务 ID 与任务进度信息的映射关系，使用 ConcurrentHashMap 保证线程安全
    private final Map<String, TaskProgress> taskMap = new ConcurrentHashMap<>();

    // 构造函数，通过依赖注入的方式传入根目录路径和信号量
    public TaskService(Path rootLocation, Semaphore semaphore) {
        this.rootLocation = rootLocation;
        this.semaphore = semaphore;
    }

    /**
     * 创建一个新的任务
     * @param request 包含任务相关信息的请求对象
     * @return 生成的任务 ID
     */
    public String createTask(ProcessRequest request) {
        // 生成一个唯一的任务 ID
        String taskId = UUID.randomUUID().toString();
        // 根据根目录和任务 ID 构建任务目录路径
        Path taskDir = rootLocation.resolve(taskId);
        // 创建任务目录，如果目录已存在则不会重复创建
        taskDir.toFile().mkdirs();

        // 在任务映射中添加新的任务进度信息
        taskMap.put(taskId, new TaskProgress(
                taskId, 0,
                request.getRegion(),
                request.getCapacity()
        ));

        // 返回生成的任务 ID
        return taskId;
    }

    /**
     * 异步处理文件
     * @param taskId 任务 ID
     * @param file 要处理的文件
     */
    @Async
    public void processFile(String taskId, MultipartFile file) {
        try {
            // 获取信号量许可，若没有可用许可则阻塞
            semaphore.acquire();
            // 更新任务进度为 10%
            updateProgress(taskId, 10);

            // 1. 存储原始文件
            // 获取任务目录路径
            Path taskDir = getTaskDir(taskId);
            // 构建原始文件的存储路径
            Path inputFile = taskDir.resolve("original.docx");
            // 将上传的文件保存到指定路径
            file.transferTo(inputFile);

            System.out.println("已收到上传的文件");

            // 更新任务进度为 30%
            updateProgress(taskId, 30);

            // 2. 调用处理算法
            processDocument(taskDir, taskMap.get(taskId));

            // 更新任务进度为 100%
            updateProgress(taskId, 100);
        } catch (Exception e) {
            // 若处理过程中出现异常，记录异常信息到任务进度中
            // taskMap.get(taskId).setError(e.getMessage());
            System.out.println(e.getMessage());
        } finally {
            // 释放信号量许可
            semaphore.release();
        }
    }

    /**
     * 处理文档的方法，这里是示例处理流程，需替换为实际业务逻辑
     * @param taskDir 任务目录路径
     * @param progress 任务进度信息
     */
    private void processDocument(Path taskDir, TaskProgress progress) {
        try {
            System.out.println("创建输入流");
            // 创建文件输入流
            File file = new File(taskDir.toFile(), "original.docx");
            FileInputStream fis = new FileInputStream(file);
            // 创建 XWPFDocument 对象，用于表示 DOCX 文档
            XWPFDocument document = new XWPFDocument(fis);
            System.out.println("打开文件成功");
            // 合并所有段落文本
            StringBuilder fullText = new StringBuilder();
            // 遍历文档中的每个段落
            for (XWPFParagraph paragraph : document.getParagraphs()) {
                String text = paragraph.getText();
                if (text != null) {
                    fullText.append(text);
                }
            }
            String text = fullText.toString();
            HashSet<String> matches = new HashSet<>();

            System.out.println("开始分词");
            // 分词
            List<Term> words = HanLP.segment(text);

            String[] regions = progress.getRegion().split("/");
            // 遍历词元列表并输出每个词及其词性
            for (Term word : words) {
                if(word.nature.toString().equals("ns") && stringUtils.isRegion(word.word)){
                    if (!word.word.equals(regions[0]) && !word.word.equals(regions[1]) && !word.word.equals(regions[2])) {
                        matches.add(word.word);
                    }
                }
            }
            System.out.println("开始标记");
            // 高亮
            for (String match : matches) {
                Highlighter.highlightText(document, match);
            }
            // 生成输出文件
            FileOutputStream fos = new FileOutputStream("output.docx");
            document.write(fos);
            // 构建输出文件的路径
            Path outputFile = taskDir.resolve("output.docx");
            // 将模板文件复制到输出文件路径
            Files.copy(this.getClass().getResourceAsStream("/template.docx"), outputFile);
            // 关闭文档和输入流
            document.close();
            fis.close();
            fos.close();
        } catch (Exception e) {
            // 若处理过程中出现异常，抛出自定义的存储异常
            throw new StorageException("文件处理失败", e);
        }
    }

    /**
     * 获取任务的进度信息
     * @param taskId 任务 ID
     * @return 任务进度信息对象，如果任务不存在则返回一个初始进度为 0 的对象
     */
    public TaskProgress getProgress(String taskId) {
        return taskMap.getOrDefault(taskId, new TaskProgress(taskId, 0));
    }

    /**
     * 更新任务的进度信息
     * @param taskId 任务 ID
     * @param progress 要更新的进度值
     */
    private void updateProgress(String taskId, int progress) {
        // 根据任务 ID 从任务映射中获取任务进度对象
        TaskProgress task = taskMap.get(taskId);
        if (task != null) {
            // 若任务存在，则更新其进度值
            task.setProgress(progress);
        }
    }

    /**
     * 获取任务的目录路径
     * @param taskId 任务 ID
     * @return 任务目录的路径对象
     */
    public Path getTaskDir(String taskId) {
        return rootLocation.resolve(taskId);
    }
}