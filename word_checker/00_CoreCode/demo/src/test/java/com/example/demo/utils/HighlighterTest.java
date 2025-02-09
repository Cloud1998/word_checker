package com.example.demo.utils;

import org.apache.poi.xwpf.usermodel.XWPFDocument;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class HighlighterTest {
    public static void main(String[] args){
        try {
            String currPath = System.getProperty("user.dir");
            File dirPath = new File(currPath + "/static");
            String filePath = dirPath + "/demo.docx";
            File file = new File(filePath);
            // 创建文件输入流
            FileInputStream fis = new FileInputStream(file);
            // 创建 XWPFDocument 对象，用于表示 DOCX 文档
            XWPFDocument doc = new XWPFDocument(fis);

            Highlighter.highlightText(doc, "云南省");

            FileOutputStream fos = new FileOutputStream("output.docx");
            doc.write(fos);
            // 关闭文档和输入流
            doc.close();
            fis.close();
            fos.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}