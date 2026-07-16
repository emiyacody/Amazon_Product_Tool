# 使用 Playwright 官方 Python 基础镜像，它预装了 Python、Chromium 浏览器以及运行所需的所有系统依赖
FROM mcr.microsoft.com/playwright/python:v1.61.0-jammy

# 设置工作目录
WORKDIR /code

# 首先复制依赖文件，便于利用 Docker 缓存层
COPY ./requirements.txt /code/requirements.txt

# 安装项目依赖包
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 复制应用程序文件和前端静态网页文件
COPY ./app /code/app
COPY ./static /code/static

# 创建本地数据缓存目录，并赋予所有用户读写权限（防止容器内以非 root 用户运行时出现权限问题）
RUN mkdir -p /code/cache && chmod 777 /code/cache

# 暴露 Hugging Face Spaces 要求的默认 Web 端口 7860
EXPOSE 7860

# 运行 FastAPI 应用，绑定 0.0.0.0 和端口 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
