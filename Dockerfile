# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to allow external access
EXPOSE 80

# Define the command to run the application
CMD ["python", "BoardEdgeRouter.py"]
