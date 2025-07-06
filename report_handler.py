
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from telegram.ext import (
    CallbackQueryHandler, ConversationHandler, MessageHandler, ContextTypes, filters
)
from utils.db import db
from config import ADMIN_IDS

# States
ASK_TG_ID, ASK_UPI, ASK_PHONE, ASK_IMAGE, ASK_PROOF = range(5)

user_reports = {}  # Temporary storage per user session

async def report_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Enter scammer's Telegram ID:")
    return ASK_TG_ID

async def ask_upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_reports[user_id] = {
        "scammer_tg_id": int(update.message.text.strip()),
        "reported_by": user_id
    }
    skip_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_upi")]])
    await update.message.reply_text("Enter scammer's UPI ID (or skip):", reply_markup=skip_markup)
    return ASK_UPI

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_reports[user_id]["scammer_upi"] = update.message.text.strip()
    skip_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_phone")]])
    await update.message.reply_text("Enter scammer's phone number (or skip):", reply_markup=skip_markup)
    return ASK_PHONE

async def ask_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_reports[user_id]["scammer_number"] = update.message.text.strip()
    skip_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_image")]])
    await update.message.reply_text("Send scammer's image (or skip):", reply_markup=skip_markup)
    return ASK_IMAGE

async def ask_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.photo:
        photo = update.message.photo[-1].file_id
        user_reports[user_id]["scammer_image"] = photo
    else:
        user_reports[user_id]["scammer_image"] = None

    await update.message.reply_text("Send scam proof (screenshot or message):", reply_markup=ReplyKeyboardRemove())
    return ASK_PROOF

async def save_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    proof = update.message.text or (update.message.caption or "")

    user_reports[user_id]["scam_proof"] = proof
    scammer_id = user_reports[user_id]["scammer_tg_id"]
    user_reports[user_id]["scammer_chat_link"] = f"tg://openmessage?user_id={scammer_id}"

    db["pending_reports"].insert_one(user_reports[user_id])

    await update.message.reply_text("✅ Your scammer report has been submitted to admins.")

    # Send to admins
    for admin_id in ADMIN_IDS:
        text = (
            f"🚨 *New Scammer Report Submitted*
"
            f"👤 Scammer TG ID: `{scammer_id}`
"
            f"💳 UPI: {user_reports[user_id].get('scammer_upi', 'N/A')}
"
            f"📞 Phone: {user_reports[user_id].get('scammer_number', 'N/A')}
"
            f"📎 Chat Link: {user_reports[user_id]['scammer_chat_link']}
"
            f"📝 Proof: {proof}"
        )
        await context.bot.send_message(chat_id=admin_id, text=text, parse_mode='Markdown')

    user_reports.pop(user_id, None)
    return ConversationHandler.END

# Skipping handlers
async def skip_upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_reports[update.effective_user.id]["scammer_upi"] = None
    skip_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_phone")]])
    await update.callback_query.edit_message_text("Enter scammer's phone number (or skip):", reply_markup=skip_markup)
    return ASK_PHONE

async def skip_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_reports[update.effective_user.id]["scammer_number"] = None
    skip_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip_image")]])
    await update.callback_query.edit_message_text("Send scammer's image (or skip):", reply_markup=skip_markup)
    return ASK_IMAGE

async def skip_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_reports[update.effective_user.id]["scammer_image"] = None
    await update.callback_query.edit_message_text("Send scam proof (screenshot or message):")
    return ASK_PROOF

report_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(report_start, pattern="^report$")],
    states={
        ASK_TG_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_upi)],
        ASK_UPI: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone),
            CallbackQueryHandler(skip_upi, pattern="^skip_upi$")
        ],
        ASK_PHONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, ask_image),
            CallbackQueryHandler(skip_phone, pattern="^skip_phone$")
        ],
        ASK_IMAGE: [
            MessageHandler(filters.PHOTO, ask_proof),
            CallbackQueryHandler(skip_image, pattern="^skip_image$")
        ],
        ASK_PROOF: [MessageHandler(filters.TEXT | filters.PHOTO, save_report)]
    },
    fallbacks=[],
)
