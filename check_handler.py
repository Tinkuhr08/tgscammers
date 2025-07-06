
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from utils.db import scammers  # MongoDB collection
import re

# States
ASK_UPI, ASK_TG_ID, ASK_PHONE = range(3)

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🔍 Check by UPI", callback_data="check_upi")],
        [InlineKeyboardButton("🆔 Check by Telegram ID", callback_data="check_tg_id")],
        [InlineKeyboardButton("📞 Check by Number", callback_data="check_number")]
    ]
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Select how you want to check:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return ConversationHandler.END

async def check_upi_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Send the UPI ID to check:")
    return ASK_UPI

async def check_tg_id_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Send the Telegram user ID to check:")
    return ASK_TG_ID

async def check_phone_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Send the phone number to check:")
    return ASK_PHONE

async def handle_upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    upi = update.message.text.strip()
    scammer = scammers.find_one({"scammer_upi": upi})
    await respond_with_result(update, scammer)
    return ConversationHandler.END

async def handle_tg_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tg_id = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Invalid Telegram ID.")
        return ConversationHandler.END
    scammer = scammers.find_one({"scammer_tg_id": tg_id})
    await respond_with_result(update, scammer)
    return ConversationHandler.END

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = re.sub(r'\D', '', update.message.text)  # remove non-digit characters
    scammer = scammers.find_one({"scammer_number": phone})
    await respond_with_result(update, scammer)
    return ConversationHandler.END

async def respond_with_result(update: Update, scammer):
    if scammer:
        msg = f"⚠️ This person is reported as a scammer.\n"
        if scammer.get("scammer_chat_link"):
            msg += f"🔗 [Chat Link]({scammer['scammer_chat_link']})\n"
        await update.message.reply_text(msg, parse_mode='Markdown')
        if scammer.get("scammer_image"):
            await update.message.reply_photo(photo=scammer["scammer_image"])
    else:
        await update.message.reply_text("✅ No scammer found with this info.")

check_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(check_command, pattern="^check$")],
    states={
        ASK_UPI: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_upi)],
        ASK_TG_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tg_id)],
        ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone)],
    },
    fallbacks=[],
)

check_menu_handler = [
    CallbackQueryHandler(check_upi_prompt, pattern="^check_upi$"),
    CallbackQueryHandler(check_tg_id_prompt, pattern="^check_tg_id$"),
    CallbackQueryHandler(check_phone_prompt, pattern="^check_number$")
]
