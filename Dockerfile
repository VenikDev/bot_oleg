# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy source code to image
COPY . .

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the application
CMD [ "python", "bot.py" ]