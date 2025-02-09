package com.example.demo.utils;

import org.apache.poi.xwpf.usermodel.*;
import org.openxmlformats.schemas.wordprocessingml.x2006.main.CTRPr;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

// 该类用于在Word文档中高亮显示指定的文本
public class Highlighter {
    /**
     * 内部类，用于存储Run的信息
     */
    private static class RunInfo {
        // 对应的Run对象
        XWPFRun run;
        // Run在段落中的起始位置
        int start;
        // Run在段落中的结束位置
        int end;

        /**
         * 构造函数，初始化Run信息
         * @param run 对应的Run对象
         * @param start Run在段落中的起始位置
         * @param end Run在段落中的结束位置
         */
        RunInfo(XWPFRun run, int start, int end) {
            this.run = run;
            this.start = start;
            this.end = end;
        }
    }

    /**
     * 高亮显示文档中所有匹配的目标文本
     * @param doc 要处理的XWPFDocument对象，代表一个Word文档
     * @param targetText 要高亮显示的目标文本
     */
    public static void highlightText(XWPFDocument doc, String targetText) {
        // 遍历文档中的每个段落
        for (XWPFParagraph paragraph : doc.getParagraphs()) {
            // 构建段落文本及Run信息
            List<RunInfo> runInfos = buildRunInfos(paragraph);
            // 从Run信息中构建出整个段落的完整文本
            String fullText = buildFullText(runInfos);
            // 查找完整文本中所有目标文本的出现位置
            List<int[]> occurrences = findOccurrences(fullText, targetText);

            // 逆序处理每个匹配项，这样在插入和删除Run时不会影响后续匹配项的位置
            Collections.reverse(occurrences);
            // 遍历每个匹配项的起始和结束位置
            for (int[] occurrence : occurrences) {
                // 处理当前匹配项，对匹配的文本进行高亮处理
                processOccurrence(paragraph, runInfos, occurrence[0], occurrence[1]);
            }
        }
    }

    /**
     * 构建段落中每个Run的信息
     * @param paragraph 要处理的段落
     * @return 包含每个Run信息的列表
     */
    private static List<RunInfo> buildRunInfos(XWPFParagraph paragraph) {
        List<RunInfo> runInfos = new ArrayList<>();
        // 当前位置，用于记录每个Run在段落中的起始位置
        int currentPosition = 0;
        // 遍历段落中的每个Run
        for (XWPFRun run : paragraph.getRuns()) {
            // 获取Run中的文本，如果为空则设为空字符串
            String text = run.getText(0);
            if (text == null) text = "";
            // 计算该Run的结束位置
            int end = currentPosition + text.length();
            // 创建RunInfo对象并添加到列表中
            runInfos.add(new RunInfo(run, currentPosition, end));
            // 更新当前位置
            currentPosition = end;
        }
        return runInfos;
    }

    /**
     * 从Run信息列表中构建出整个段落的完整文本
     * @param runInfos 包含每个Run信息的列表
     * @return 整个段落的完整文本
     */
    private static String buildFullText(List<RunInfo> runInfos) {
        StringBuilder sb = new StringBuilder();
        // 遍历每个Run信息
        for (RunInfo info : runInfos) {
            // 将Run中的文本添加到StringBuilder中，如果为空则添加空字符串
            sb.append(info.run.getText(0) != null ? info.run.getText(0) : "");
        }
        return sb.toString();
    }

    /**
     * 查找完整文本中所有目标文本的出现位置
     * @param fullText 整个段落的完整文本
     * @param target 要查找的目标文本
     * @return 包含每个匹配项起始和结束位置的列表
     */
    private static List<int[]> findOccurrences(String fullText, String target) {
        List<int[]> occurrences = new ArrayList<>();
        // 起始查找位置
        int index = 0;
        while (index != -1) {
            // 查找目标文本在完整文本中的下一个出现位置
            index = fullText.indexOf(target, index);
            if (index != -1) {
                // 计算匹配项的结束位置
                int end = index + target.length();
                // 将匹配项的起始和结束位置添加到列表中
                occurrences.add(new int[]{index, end});
                // 更新查找位置，从匹配项的结束位置开始继续查找
                index = end;
            }
        }
        return occurrences;
    }

    /**
     * 处理匹配项，对匹配的文本进行高亮处理
     * @param paragraph 包含匹配项的段落
     * @param runInfos 段落中每个Run的信息列表
     * @param start 匹配项的起始位置
     * @param end 匹配项的结束位置
     */
    private static void processOccurrence(XWPFParagraph paragraph, List<RunInfo> runInfos, int start, int end) {
        List<RunInfo> affected = new ArrayList<>();
        // 遍历所有Run信息，找出与匹配项有重叠的Run
        for (RunInfo info : runInfos) {
            if (info.end > start && info.start < end) {
                affected.add(info);
            }
        }

        // 逆序处理Run，这样在插入和删除Run时不会影响后续处理
        Collections.reverse(affected);
        // 遍历受影响的Run
        for (RunInfo info : affected) {
            // 计算重叠部分的起始和结束位置
            int overlapStart = Math.max(info.start, start);
            int overlapEnd = Math.min(info.end, end);
            // 计算在当前Run中的起始和结束位置
            int localStart = overlapStart - info.start;
            int localEnd = overlapEnd - info.start;

            // 分割当前Run并对重叠部分进行高亮处理
            splitAndHighlightRun(info.run, localStart, localEnd, paragraph);
        }
    }

    /**
     * 分割Run并对指定部分进行高亮处理
     * @param originalRun 要处理的原始Run
     * @param start 要高亮部分在原始Run中的起始位置
     * @param end 要高亮部分在原始Run中的结束位置
     * @param paragraph 包含原始Run的段落
     */
    private static void splitAndHighlightRun(XWPFRun originalRun, int start, int end, XWPFParagraph paragraph) {
        // 获取原始Run中的文本，如果文本为空则将其设置为空字符串
        String originalText = originalRun.getText(0);
        if (originalText == null) originalText = "";

        // 从原始文本中截取高亮部分之前的文本
        String before = originalText.substring(0, start);
        // 从原始文本中截取需要高亮显示的文本
        String highlight = originalText.substring(start, end);
        // 从原始文本中截取高亮部分之后的文本
        String after = originalText.substring(end);

        // 获取原始Run在段落中的索引位置
        int runPosition = paragraph.getRuns().indexOf(originalRun);
        // 如果未找到原始Run，则直接返回，不进行后续操作
        if (runPosition == -1) return;

        // 声明一个变量用于存储原始Run的样式信息
        CTRPr sourceRPr = null;
        // 检查原始Run是否设置了样式信息
        if (originalRun.getCTR().isSetRPr()) {
            // 如果设置了样式信息，则对其进行深度复制，避免后续原始对象状态变化影响复制的样式
            sourceRPr = (CTRPr) originalRun.getCTR().getRPr().copy();
        }

        // 从段落中移除原始Run
        paragraph.removeRun(runPosition);

        // 处理高亮部分之前的文本，如果该部分文本不为空
        if (!before.isEmpty()) {
            // 在原始Run的位置插入一个新的Run，用于存放高亮部分之前的文本
            XWPFRun newRun = paragraph.insertNewRun(runPosition);
            // 如果存在原始Run的样式信息
            if (sourceRPr != null) {
                // 将复制的样式信息再次复制给新的Run，确保新Run拥有相同的样式
                newRun.getCTR().setRPr((CTRPr) sourceRPr.copy());
            }
            // 将高亮部分之前的文本设置到新的Run中
            newRun.setText(before);
            // 索引位置加1，为后续插入高亮Run做准备
            runPosition++;
        }

        // 在当前位置插入一个新的Run，用于存放需要高亮显示的文本
        XWPFRun highlightRun = paragraph.insertNewRun(runPosition);
        // 如果存在原始Run的样式信息
        if (sourceRPr != null) {
            // 将复制的样式信息再次复制给高亮Run，确保高亮Run拥有相同的样式
            highlightRun.getCTR().setRPr((CTRPr) sourceRPr.copy());
        }
        // 设置高亮Run的文本颜色为红色，实现高亮显示效果
        highlightRun.setColor("FF0000");
        // 将需要高亮显示的文本设置到高亮Run中
        highlightRun.setText(highlight);
        // 索引位置加1，为后续插入高亮部分之后的文本的Run做准备
        runPosition++;

        // 处理高亮部分之后的文本，如果该部分文本不为空
        if (!after.isEmpty()) {
            // 在当前位置插入一个新的Run，用于存放高亮部分之后的文本
            XWPFRun afterRun = paragraph.insertNewRun(runPosition);
            // 如果存在原始Run的样式信息
            if (sourceRPr != null) {
                // 将复制的样式信息再次复制给存放高亮部分之后文本的Run，确保其拥有相同的样式
                afterRun.getCTR().setRPr((CTRPr) sourceRPr.copy());
            }
            // 将高亮部分之后的文本设置到对应的Run中
            afterRun.setText(after);
        }
    }

    /**
     * 复制源Run的样式到目标Run
     * @param source 源Run
     * @param target 目标Run
     */
    private static void copyRunStyle(XWPFRun source, XWPFRun target) {
        // 获取源Run的样式信息
        CTRPr sourceRPr = source.getCTR().isSetRPr() ? source.getCTR().getRPr() : null;
        // 获取目标Run的样式信息
        CTRPr targetRPr = target.getCTR().getRPr();
        if (sourceRPr != null) {
            // 将源Run的样式信息复制到目标Run
            targetRPr.set(sourceRPr.copy());
        }
    }
}