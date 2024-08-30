FROM python:3.9-slim

# Set environment variables
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0

# Install dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Run Celery
CMD ["celery", "-A", "backend", "worker", "--loglevel=info"]
