from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import random

BOT_TOKEN = '8050769355:AAGdI99KGP-7UTBXa8HKy9od_Nu0Tl1ZYXU'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text == 'hi':
        await update.message.reply_text("Hi there! 👋")

    elif text == 'i love you':
        await update.message.reply_text("I love you too 💖")

    elif 'anime' in text:
        await update.message.reply_text("Fetching latest anime news... 📰")
        try:
            response = requests.get("https://api.jikan.moe/v4/anime", params={"order_by": "start_date", "sort": "desc", "limit": 10})
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                anime = random.choice(data["data"])
                title = anime["title"]
                url = anime["url"]
                synopsis = anime["synopsis"] or "No synopsis available."

                reply = f"🎬 *{title}*\n{synopsis[:300]}...\n🔗 [More Info]({url})"
                await update.message.reply_markdown(reply)
            else:
                await update.message.reply_text("Couldn't find any anime news.")
        except Exception as e:
            await update.message.reply_text("Error fetching anime news.")
            print(e)

    else:
        await update.message.reply_text("Say 'hi', 'i love you', or 'anime' to get a response!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Type 'hi', 'i love you', or 'anime'.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
