# 使用轻量级 JDK 镜像
FROM eclipse-temurin:17-jdk-jammy

# 设置工作目录
WORKDIR /app

# 复制构建好的 Jar 包（先执行 mvn package）
COPY target/demo.jar app.jar

# 暴露端口（与 Spring Boot 的 server.port 一致）
EXPOSE 8080

# 启动命令
ENTRYPOINT ["java", "-jar", "app.jar"]