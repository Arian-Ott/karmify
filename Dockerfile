FROM python:3.13-rc-slim

ENV PYTHONUNBUFFERED=True 
ENV PYTHONDONTWRITEBYTECODE=True

WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the API port
EXPOSE 4567

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "4567", "--reload", "--workers", "1"]