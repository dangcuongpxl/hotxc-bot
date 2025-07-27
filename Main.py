import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = 1617976122

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Bạn không có quyền dùng bot này.")
        return
    await update.message.reply_text("🤖 Gửi API Key Bybit theo cú pháp:\n`api_key|api_secret`")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    msg = update.message.text.strip()
    if "|" in msg:
        api_key, api_secret = msg.split("|", 1)
        with open("bybit_api.txt", "w") as f:
            f.write(f"{api_key.strip()}|{api_secret.strip()}")
        await update.message.reply_text("✅ Đã lưu Bybit API. Bot sẽ bắt đầu trade nếu đủ điều kiện.")
    else:
        await update.message.reply_text("❌ Sai định dạng. Gửi theo mẫu: `api_key|api_secret`")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling()
