FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jdk-headless \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY src/java/MatMul.java .
RUN javac MatMul.java
COPY docker/run_container.sh .
RUN sed -i 's/\r$//' run_container.sh && chmod +x run_container.sh
ENV LANG_ID=java RUN_CMD="java -cp /app MatMul" VERSION_CMD="java -version"
ENTRYPOINT ["/app/run_container.sh"]