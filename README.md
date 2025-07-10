# Yarrchive

# Getting Started

1. Set environment variable DISCORD_BOT_TOKEN.
2. Run the bot.

```
docker run -d \
  --name yarrchive \
  -e DISCORD_BOT_TOKEN="$DISCORD_BOT_TOKEN" \
  yarrchive:0.0.1
```

3. View logs.
```
docker logs yarrchive
```

# Development

```
docker build -t yarrchive:0.0.1
```
