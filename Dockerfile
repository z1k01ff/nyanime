# Use the official Python image as base
FROM python:3.12-slim

# Set environment variables
ENV TZ=Europe/Kiev
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and clean up in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    wget \
    poppler-utils \
    libaio1 \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Oracle Instant Client
RUN wget https://download.oracle.com/otn_software/linux/instantclient/1923000/instantclient-basiclite-linux.x64-19.23.0.0.0dbru.zip \
    && unzip instantclient-basiclite-linux.x64-19.23.0.0.0dbru.zip -d /oracle \
    && rm -f instantclient-basiclite-linux.x64-19.23.0.0.0dbru.zip

# Install Google Chrome and ChromeDriver
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && ln -s /usr/bin/google-chrome /usr/bin/chromium-browser \
    && wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && rm -rf /var/lib/apt/lists/*

# Set up timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set working directory
WORKDIR /bot

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /bot

# Copy .env file
COPY .env /bot/.env

# Create log file
RUN touch /var/log/syslog
