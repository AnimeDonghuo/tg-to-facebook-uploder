FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev curl && apt-get clean
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /tmp/tgfb && chmod +x start.sh
EXPOSE 8000
CMD ["./start.sh"]
