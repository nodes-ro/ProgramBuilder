# Use the Python 3.11 Alpine image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY static static
COPY templates templates

COPY app.py app.py
COPY requirements.txt requirements.txt

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8010

# Define environment variable to disable buffering
ENV PYTHONUNBUFFERED=1

# Run the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8010", "--workers", "1", "--reload", "app:app"]
