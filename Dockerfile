# Use a lightweight Python image
FROM python:3.13.3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your dependencies list
COPY requirements.txt requirements.txt

# Install Flask
RUN pip install -r requirements.txt

# Copy all files into the container
COPY . .

# Tell Docker how to run the app
CMD ["python", "app.py"]
