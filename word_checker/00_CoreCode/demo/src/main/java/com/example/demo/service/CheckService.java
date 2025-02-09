package com.example.demo.service;

import com.example.demo.utils.Highlighter;
import com.example.demo.utils.StringUtils;
import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.common.Term;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

@Service
public class CheckService {
    @Autowired
    private StringUtils stringUtils;

    private final String currPath = System.getProperty("user.dir");

    private String filePath;
    private String fileName;

    private String province = "河北省";
    private String city = "张家口市";
    private String area = "怀来县";

    public List<String> checkReagion(String fileName) throws IOException {
        // 返回结果
        List<String> result = new ArrayList<>();

        // 定义要检查的 DOCX 文件路径
        File dirPath = new File(currPath + "/static");
        if(!dirPath.exists()){
            dirPath.mkdir();
        }
        String filePath = dirPath + File.separator + fileName;
        File file = new File(filePath);

        // 创建文件输入流
        FileInputStream fis = new FileInputStream(file);
        // 创建 XWPFDocument 对象，用于表示 DOCX 文档
        XWPFDocument document = new XWPFDocument(fis);

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
        // 分词
        List<Term> words = HanLP.segment(text);
        // 遍历词元列表并输出每个词及其词性
        for (Term word : words) {
            if(word.nature.toString().equals("ns") && stringUtils.isRegion(word.word)){
                if (!word.word.equals(province) && !word.word.equals(city) && !word.word.equals(area)) {
                    result.add(word.word + " " + word.nature);
                    matches.add(word.word);
                }
            }
        }
        // 高亮
        for (String match : matches) {
            Highlighter.highlightText(document, match);
        }
        // 保存
        FileOutputStream fos = new FileOutputStream("output.docx");
        document.write(fos);
        // 关闭文档和输入流
        document.close();
        fis.close();
        fos.close();
        return result;
    }

    public void checkStandard(String fileName) throws IOException {

    }

}
