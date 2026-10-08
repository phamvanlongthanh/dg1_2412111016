FROM python:3.10-slim

# Tạo người dùng không phải root (non-root)
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Cài thư viện trước khi sao chép mã nguồn (tối ưu Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn
COPY . .

# Tạo thư mục data và cấp quyền cho appuser
RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python3", "app/app.py"]
