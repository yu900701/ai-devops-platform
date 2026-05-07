# 使用官方 Python image
FROM python:3.11-slim

# 避免 Python 產生 pyc
ENV PYTHONDONTWRITEBYTECODE=1

# 即時輸出 log
ENV PYTHONUNBUFFERED=1

# container 工作目錄
WORKDIR /app

# 複製 requirements
COPY app/requirements.txt .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製 app source code
COPY app/ .

# 開放 port
EXPOSE 8000

# 啟動 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]