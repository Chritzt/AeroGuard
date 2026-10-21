# 1. Image
FROM python:3.11-slim

# 2. Env-Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Workfolder
WORKDIR /app

# 4. Optimization for caching
COPY requirements.txt .

# 5. install requirements
RUN pip install --no-cache-dir -r requirements.txt

# 6. Cypo code
COPY . .

# 7. SECURITY HARDENING: Non-Root User 
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 8. Port
EXPOSE 3000

# 9. Start Command
CMD ["python", "src/main.py"]