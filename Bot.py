from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import random

TOKEN = "7902171019:AAHpTe-xepDouirL2jzW2F8YYp-GVrA_D7M"

CATEGORIES = {
    "Новый год": "cards/new_year",
    "День рождения": "cards/birthday",
    "8 марта": "cards/women_day",
    "23 февраля": "cards/defender_day"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(text=key, callback_data=key)] for key in CATEGORIES.keys()]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Выберите праздник для поздравления:", reply_markup=reply_markup)

async def send_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    category = query.data
    folder_path = CATEGORIES.get(category)
    
    if folder_path and os.path.exists(folder_path):
        cards = os.listdir(folder_path)
        if cards:
            chosen_card = random.choice(cards)
            card_path = os.path.join(folder_path, chosen_card)
            with open(card_path, "rb") as card:
                await query.message.reply_photo(photo=InputFile(card), caption=f"Поздравляю с {category}!")
        else:
            await query.message.reply_text("Открытки для этого праздника пока нет.")
    else:
        await query.message.reply_text("Не удалось найти открытки для этого праздника.")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_card(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    app.run_polling()

if __name__ == "__main__":
    main()
