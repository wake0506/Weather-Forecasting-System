FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖（开发工具）
RUN apt-get update && apt-get install -y \
    git \
    vim \
    curl \
    wget \
    tree \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir ipython

# 创建必要的目录
RUN mkdir -p data/cache data/logs data/reports

# 设置环境变量
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# 开发模式 - 保持容器运行
CMD ["tail", "-f", "/dev/null"]