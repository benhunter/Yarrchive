import discord
import re
import datetime
import yaml
import os  # For environment variables

# Load configuration from YAML file
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config.yaml not found.  Exiting.")
    exit()
except yaml.YAMLError as e:
    print(f"Error parsing config.yaml: {e}.  Exiting.")
    exit()

# Get bot token from environment variable
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not BOT_TOKEN:
    print("Error: DISCORD_BOT_TOKEN environment variable not set.  Exiting.")
    exit()

CHANNEL_IDS = config.get("channel_ids", [])  # Default to empty list if not found
LOG_FILE = config.get("log_file", "url_log.csv")  # Default log file
LOG_FORMAT = config.get("log_format", "csv") # Default log format

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
client = discord.Client(intents=intents)

# URL Regular Expression (improved)
URL_REGEX = re.compile(
    r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
)

# Function to log URLs
def log_url(url, author, timestamp):
    """Logs the URL to a file (CSV or text) based on config."""
    try:
        if LOG_FORMAT == "csv":
            with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
                import csv
                writer = csv.writer(csvfile)
                writer.writerow([timestamp, author.name, author.id, url])
        elif LOG_FORMAT == "text":
            with open(LOG_FILE, 'a', encoding='utf-8') as textfile:
                textfile.write(f"{timestamp} - {author.name} ({author.id}): {url}\n")
        else:
            print(f"Error: Invalid log format '{LOG_FORMAT}' in config.yaml.  Using default CSV.")
            with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
                import csv
                writer = csv.writer(csvfile)
                writer.writerow([timestamp, author.name, author.id, url])

    except Exception as e:
        print(f"Error logging URL: {e}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    if message.channel.id in CHANNEL_IDS:
        urls = URL_REGEX.findall(message.content)
        for url in urls:
            # Clean up the URL (remove extra characters)
            url = url.strip()
            if url:  # Ensure the URL isn't empty after stripping
                timestamp = datetime.datetime.now().isoformat()
                log_url(url, message.author, timestamp)
                print(f"Logged URL: {url} from {message.author.name}")

# Run the bot
client.run(BOT_TOKEN)
