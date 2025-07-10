FROM python:3.11-slim-buster

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot script and config file
COPY bot.py .
COPY config.yaml .

# Command to run the bot
CMD ["python", "bot.py"]
