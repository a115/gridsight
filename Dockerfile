# --- Build Stage ---
FROM python:3.12-slim as builder

WORKDIR /app

# Set dummy env vars required for settings validation during collectstatic
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET_KEY="dummy-key-for-build"
ENV POSTGRES_HOST="db"
ENV POSTGRES_PORT="5432"
ENV POSTGRES_USER="postgres"
ENV POSTGRES_PASSWORD="dummy"
ENV POSTGRES_DB="dummy"
ENV BMRS_API_KEY="dummy"
ENV APP_NAME="gridsight-build"
ENV LOGFIRE_TOKEN="dummy"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install -U pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run collectstatic
RUN python manage.py collectstatic --noinput


# --- Final Stage ---
FROM python:3.12-slim

WORKDIR /app

# Set env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Install only necessary runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy python dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files and static files from builder
COPY --from=builder /app .

# Change ownership to the new user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port
EXPOSE 8000

# The command to run the application
# We use gunicorn for production instead of Django's development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app.wsgi"]
