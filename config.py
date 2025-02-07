# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "27392387"))
API_HASH = getenv("API_HASH", "37ee47c18c8be62716a27335a771e7da")
BOT_TOKEN = getenv("BOT_TOKEN", "7790663224:AAEP4TdtMohfq-wPrYXJaCC2rfl33OUMf3k")
OWNER_ID = list(map(int, getenv("OWNER_ID", "5787359348").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://Bhardwaj:VHr6zrvpsMsU3@cluster0.p2smf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = getenv("LOG_GROUP", "-1002406770624")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002197825290"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "50"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "1000"))
WEBSITE_URL = getenv("WEBSITE_URL", "Modijiurl.com")
AD_API = getenv("AD_API", "f2bb4074d89772fb1db2ed878a7b417d06c3e121")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
