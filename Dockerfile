FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Ensure the app directory is in the python path
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libffi-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN useradd -m botuser && chown -R botuser /app
USER botuser

# Install dependencies
COPY --chown=botuser:botuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy project
COPY --chown=botuser:botuser . .

ENV PATH="/home/botuser/.local/bin:${PATH}"
RUN mkdir -p /tmp/tgfb

EXPOSE 8000

# Using a shell script to allow for pre-run tasks if needed
CMD ["python3", "-m", "app.main"]
