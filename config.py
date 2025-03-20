# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "23680771"))
API_HASH = getenv("API_HASH", "0c58f3e3fecefc4a9d8e5bcf6968a106")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = list(map(int, getenv("OWNER_ID", "7796913460").split()))
MONGO_DB = getenv("MONGO_DB", "")
LOG_GROUP = getenv("LOG_GROUP", "-1002611183621")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002543707369"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "100"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "5000"))
WEBSITE_URL = getenv("WEBSITE_URL", None)
AD_API = getenv("AD_API", None)
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
