# Use an official Python runtime as a parent image
FROM python:3.10-alpine


# Set the working directory in the container
WORKDIR /

# Copy only necessary files to reduce context size
COPY requirements.txt .
COPY . .env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY mqtt .

# Expose port 80 to allow external access
EXPOSE 80

# Define the command to run the application
CMD ["python", "main.py"]
