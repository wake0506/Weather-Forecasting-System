FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ ./src/
COPY config/ ./config/

# 健壮的 data 目录复制 - 使用条件检查
#RUN mkdir -p /app/data
#COPY data/ /app/data/ 2>/dev/null || echo "Warning: data directory copy failed or empty, continuing..."

# 创建非root用户
RUN useradd -m -r appuser && \
    chown -R appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "src/main.py"]