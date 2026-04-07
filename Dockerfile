# 1. Sabse stable aur updated base image use karein
FROM python:3.9-slim

# 2. Security: System packages ko upgrade karein (Trivy errors fix karne ke liye)
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Dependencies copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. App code copy karein
COPY . .

# 5. Non-root user (Security best practice)
RUN useradd -m myuser
USER myuser

EXPOSE 5000

CMD ["python", "app.py"]