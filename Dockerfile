# Use an official Python runtime as a parent image
FROM python:3.10-alpine AS builder

# Set the working directory in the builder stage
WORKDIR /app

# Copy only the requirements file to install dependencies
COPY requirements.txt .

# Install dependencies in the builder stage
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.10-alpine

# Set the working directory in the final stage
WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY . .

# Expose port 80 to allow external access
EXPOSE 80

# Define the command to run the application
CMD ["python", "/app/main.py"]
