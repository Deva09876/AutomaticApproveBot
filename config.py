from os import getenv

from dotenv import load_dotenv

# Fill These Variables

START_IMG = getenv("START_IMG" "https://telegra.ph/file/933eea77aca96ed3460b8.png")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
SESSION = getenv("SESSION")
OWNER_ID = int(getenv("OWNER_ID", 5381777131))
CHANNEL = getenv("CHANNEL", "Dadeyebotz")
