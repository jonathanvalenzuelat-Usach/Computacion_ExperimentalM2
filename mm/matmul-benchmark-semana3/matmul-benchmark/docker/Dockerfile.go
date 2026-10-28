FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends golang-go \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY src/go/ .
RUN go build -o matmul_go .
COPY docker/run_container.sh .
RUN sed -i 's/\r$//' run_container.sh && chmod +x run_container.sh
ENV LANG_ID=go RUN_CMD=/app/matmul_go VERSION_CMD="go version"
ENTRYPOINT ["/app/run_container.sh"]
