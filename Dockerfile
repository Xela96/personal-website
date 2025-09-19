# personal-website/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy and install Flask app dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY . .

# Expose Flask port
EXPOSE 5000

# Default environment vars
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
