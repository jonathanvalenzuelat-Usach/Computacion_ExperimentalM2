FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY src/cpp/matmul.cpp .
RUN g++ -O2 -std=c++17 -ffp-contract=off matmul.cpp -o matmul_cpp
COPY docker/run_container.sh .
RUN sed -i 's/\r$//' run_container.sh && chmod +x run_container.sh
ENV LANG_ID=cpp RUN_CMD=/app/matmul_cpp VERSION_CMD="g++ --version"
ENTRYPOINT ["/app/run_container.sh"]
