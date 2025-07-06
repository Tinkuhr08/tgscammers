
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from config import ADMIN_IDS
from utils.db import is_scammer

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    scammer_data = is_scammer(user_id)

    if scammer_data:
        # Scammer found in DB
        reported_by = scammer_data.get("reported_by", "Unknown")

        appeal_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Appeal", callback_data="appeal")]
        ])
        await update.message.reply_text(
            f"🚫 Sorry, you can't use this bot because you are registered as scammer "
            f"by {reported_by}.",
            reply_markup=appeal_button
        )
        return

    # If not scammer, show full main menu
    buttons = [
        [InlineKeyboardButton("🔍 Check Scammer", callback_data="check")],
        [InlineKeyboardButton("🚨 Report Scammer", callback_data="report")],
        [InlineKeyboardButton("📊 Top Scammers", callback_data="top")],
        [InlineKeyboardButton("📁 My Reports", callback_data="myreport")],
        [InlineKeyboardButton("📤 Appeal", callback_data="appeal")],
    ]

    if user_id in ADMIN_IDS:
        buttons.append([InlineKeyboardButton("🛠 Admin Panel", callback_data="admin")])

    await update.message.reply_text(
        "Welcome to Scammer Finder Bot! 👇 Choose an option:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

start_handler = CommandHandler("start", start)
