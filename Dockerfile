# Step 1: Use the official Python image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install -r requirements.txt

# Step 4: Install system dependencies, including the missing libraries for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    make

# Step 5: Copy the rest of the application code into the container
COPY . .

# Step 6: Expose the port that the FastAPI app will run on
EXPOSE 5000

# Step 7: Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
