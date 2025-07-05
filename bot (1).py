# Scammer Buster Bot - Main File (bot.py)

# Developed as per user specs for GitHub deployment

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes, ConversationHandler
)

# --- States ---
(START, CHECK_SCAMMER, SUBMIT_SCAMMER, STEP_PHONE, STEP_UPI, STEP_AMOUNT, STEP_PROOF, STEP_PHOTO, ADMIN_PANEL) = range(9)

# --- In-Memory Database (for prototype) ---
SCAMMERS = []
REPORTS = []
ADMINS = [123456789]  # Replace with real admin Telegram user IDs

# --- Utilities ---
def scammer_grade(amount):
    if amount >= 10000:
        return "ULTRA SCAMMER"
    elif amount >= 1000:
        return "MASTER SCAMMER"
    else:
        return "CHINDI SCAMMER"

def notify_reporter(user_id, msg, app):
    app.bot.send_message(chat_id=user_id, text=msg)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1. Check Scammer", callback_data="check_scammer")],
        [InlineKeyboardButton("2. Submit Scammer Report", callback_data="submit_report")],
        [InlineKeyboardButton("3. Appeal (If you're tagged)", callback_data="appeal")],
        [InlineKeyboardButton("4. Top Scammers List", callback_data="top_scammers")],
    ]
    if update.effective_user.id in ADMINS:
        keyboard.append([InlineKeyboardButton("Admin Panel", callback_data="admin_panel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Scammer Buster Bot!", reply_markup=reply_markup)
    return START

# Add other handlers here (handle_phone, handle_upi, handle_amount, handle_proof, admin_approve, etc.)