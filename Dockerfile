# Base image
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy source code to image
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose application port
EXPOSE 5000

# Start the application
CMD [ "python", "bot.py" ]