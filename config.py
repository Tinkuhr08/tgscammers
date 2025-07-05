# config.py

# 🔐 Telegram Bot Token (replace with your actual token)
BOT_TOKEN = "your_telegram_bot_token_here"

# 👑 Admin User IDs (Telegram numeric user IDs)
ADMINS = [123456789, 987654321]  # Replace with actual admin Telegram IDs

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
