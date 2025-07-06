import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))

# 📷 Max image size (in bytes) for optional scammer photo submission
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# 🔧 Other constants
SCAMMER_GRADES = {
    "Chindi": 0,
    "Master": 1000,
    "Ultra": 10000,
}
