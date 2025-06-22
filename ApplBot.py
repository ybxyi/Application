import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Google Sheets setup ===
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("/home/ec2-user/Application/telegrambotapplications-2e9e38c381bc.json", SCOPE)
GSHEET = gspread.authorize(CREDS)
SPREADSHEET = GSHEET.open("Driver applications")

# === Chat ID → Worksheet mapping ===
CHAT_WORKSHEET_MAP = {
    -1002664379092: "Asia",
}

# === Логирование ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Обработка сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE & filters.TEXT, handle_message))
    message = update.edited_message or update.message
    if not message:
        return
    logger.info(f"Received message from chat_id: {message.chat_id}")
    chat_id = message.chat_id
    text = message.text.strip()
    lines = text.splitlines()
    if not text.lower().startswith("#driver"):
        return  # не водители — не добавляем


 # Логирование полученного сообщения
    print(f"Новое сообщение от {chat_id}: {text}")

     # Получаем имя листа по chat_id
    worksheet_name = CHAT_WORKSHEET_MAP.get(chat_id)
    if not worksheet_name:
        logger.warning(f"Chat_id {chat_id} not in the mapping.")
        return  # если chat_id не найден в маппинге, ничего не делаем

    if len(lines) >= 3:
        name = lines[1].strip()
        company = lines[2].strip()
        phone = lines[3].strip()
        now = datetime.now().strftime("%m/%d/%Y")

        worksheet = SPREADSHEET.worksheet(worksheet_name)
        worksheet.append_row([name, company, phone, now])
        

# === Запуск бота ===
app = ApplicationBuilder().token("7640182483:AAHuTCYyUUP_XQ3s4nXEGBHWVYwLQAVzZOk").build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()
