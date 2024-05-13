# Use the official Python image as a base
FROM python:3.9-slim

# Install tcpdump
RUN apt-get update && \
    apt-get install -y tcpdump && \
    apt-get clean
    
# Set environment variables
ENV TARGET="v1"

# Set working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY app.py /app
COPY requirements.txt /app

# Install required dependencies
RUN pip install -r requirements.txt

# Expose port 
EXPOSE 5000


# Run the Flask application
CMD ["python", "app.py"]
