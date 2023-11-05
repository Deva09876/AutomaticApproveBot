from os import getenv

from dotenv import load_dotenv

# Fill These Variables

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
CHANNEL = getenv("CHANNEL", "Dadeyebotz")
OWNER_ID = int(getenv("OWNER_ID", 5381777131))
MONGO = getenv("MONGO")
