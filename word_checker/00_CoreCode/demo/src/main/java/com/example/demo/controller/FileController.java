package com.example.demo.controller;

import com.example.demo.dto.ApiResponse;
import com.example.demo.dto.ProcessRequest;
import com.example.demo.dto.TaskProgress;
import com.example.demo.service.FileStorageService;
import com.example.demo.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.nio.file.Path;

@RestController
@RequestMapping("/api")
public class FileController {
    @Autowired
    private TaskService taskService;
    @Autowired
    private FileStorageService storageService;

    @PostMapping("/create-task")
    public ApiResponse<String> createTask(@RequestBody ProcessRequest request) {
        storageService.checkStorage();
        String taskId = taskService.createTask(request);
        return ApiResponse.success(taskId);
    }

    @PostMapping("/upload")
    public ApiResponse<?> uploadFile(
        @RequestParam("file") MultipartFile file,
        @RequestParam("taskId") String taskId
    ) {
        if (file.isEmpty()) {
            return ApiResponse.error(400, "文件不能为空");
        }
        
        taskService.processFile(taskId, file);
        return ApiResponse.success("文件上传成功");
    }

    @GetMapping("/progress/{taskId}")
    public ApiResponse<TaskProgress> getProgress(@PathVariable String taskId) {
        return ApiResponse.success(taskService.getProgress(taskId));
    }

    @GetMapping("/download/{taskId}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String taskId) {
        Path filePath = taskService.getTaskDir(taskId).resolve("output.docx");
        Resource resource = new FileSystemResource(filePath);

        return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_DISPOSITION,
                   "attachment; filename=\"output.docx\"")
            .contentType(MediaType.APPLICATION_OCTET_STREAM)
            .body(resource);
    }
}