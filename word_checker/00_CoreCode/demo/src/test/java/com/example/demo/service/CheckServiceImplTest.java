package com.example.demo.service;

import java.io.IOException;

public class CheckServiceImplTest {
    public static void main(String[] args) {
        CheckService checker = new CheckService();
        try {
            checker.checkReagion("demo.docx");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
