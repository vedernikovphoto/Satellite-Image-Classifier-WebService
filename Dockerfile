FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt
    
RUN apt-get update && \
    apt-get install -y \
    build-essential  \
    libgl1-mesa-glx \
    libglib2.0-0 \
    --no-install-recommends && \
    make
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
