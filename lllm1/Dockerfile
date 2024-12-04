# Use an appropriate base image (e.g., Python, Flask)
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy the requirements file first, install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the 'ollama' executable into the container
COPY ./ollama.exe /app/ollama.exe

# Copy the rest of your app code
COPY . /app/

# Expose the Flask app port
EXPOSE 5000

# Command to run the application (update with your app's entry point)
CMD ["python", "app.py"]