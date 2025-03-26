# Use an official Python image with a specific version (Python 3.10)
FROM python:3.10-slim

# Set the working directory inside the container to '/app'
WORKDIR /app

# Copy everything from the current backend folder into the container's '/app' directory
COPY . .

# Install dependencies + FORCE INSTALL python-multipart
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir python-multipart

# Expose port 8000 for FastAPI (the application will run on this port)
EXPOSE 8000

# Command to run the FastAPI server using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
