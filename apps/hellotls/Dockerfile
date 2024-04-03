# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV TARGET="World" \
    COLOR="black"

# Set working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY app.py /app
COPY requirements.txt /app

# Install required dependencies
RUN pip install -r requirements.txt

# Expose port 443 for HTTPS
EXPOSE 443

# Run the Flask application
CMD ["python", "app.py"]
