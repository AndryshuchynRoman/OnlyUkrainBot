import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler, filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def hello (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'хаю хай {update.effective_user.first_name}')
async def HI(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'віііііііі {update.effective_user.first_name}')
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   messege = update.message.text.lower()

   if 'привіт' in messege:
       reply_text = f'привіт {update.effective_user.first_name}!'
   else:
       reply_text = 'Я тебе не розумію '

   await update.message.reply_text(reply_text)
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("HI", HI))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
