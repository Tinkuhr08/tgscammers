# config.py

# 🔐 Telegram Bot Token (replace with your actual token)
BOT_TOKEN = "7887330354:AAGUAJf_GBYGh3DExWecX8B6kd3R8KTBFQ8"

# 👑 Admin User IDs (Telegram numeric user IDs)
ADMINS = [1948138813]  # Replace with actual admin Telegram IDs

# 📁 File path for storing scammer & report data (if you're using JSON)
SCAMMER_DATA_FILE = "scammers.json"
REPORTS_DATA_FILE = "reports.json"

# 📷 Max image size (in bytes) for optional scammer photo submission
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# 🔧 Other constants
SCAMMER_GRADES = {
    "Chindi": 0,
    "Master": 1000,
    "Ultra": 10000,
}
