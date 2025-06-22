import os
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

# API Endpoints
FACT_API = "https://uselessfacts.jsph.pl/random.json?language=en"
CAT_FACT_API = "https://catfact.ninja/fact"
QUOTE_API = "https://api.quotable.io/random"
HISTORY_API = "https://history.muffinlabs.com/date"
ANIME_API = "https://api.jikan.moe/v4/anime"

# Fun responses
LOVE_RESPONSES = [
    "I love you too 💖",
    "Of course I do 😌",
    "I'm just a bot, but let's pretend 💌",
    "Love is in the air 🌸",
    "Always have, always will 💘"
]

FOOD_RESPONSES = [
    "I don't eat, but thanks for asking! 🍽️",
    "I'm a bot, but I imagine pizza would be great right now 🍕",
    "No lunch, just code and queries 🤖",
    "Yes! Data soup with an extra byte 😋",
    "Still waiting for my ramen delivery... 🍜"
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user.first_name or "there"

    if text == 'hi':
        await update.message.reply_text(f"Hi {user}! 👋")

    elif "i love you" in text or "do you love me" in text:
        await update.message.reply_text(random.choice(LOVE_RESPONSES))

    elif "have you lunch" in text or "do you eat" in text:
        await update.message.reply_text(random.choice(FOOD_RESPONSES))

    elif "fact" in text:
        try:
            r = requests.get(FACT_API).json()
            await update.message.reply_text(f"🧠 Fun Fact: {r.get('text')}")
        except:
            await update.message.reply_text("Could not fetch a fact at the moment 😔")

    elif "cat" in text:
        try:
            r = requests.get(CAT_FACT_API).json()
            await update.message.reply_text(f"🐱 Cat Fact: {r.get('fact')}")
        except:
            await update.message.reply_text("No cat facts right now 😿")

    elif "quote" in text:
        try:
            r = requests.get(QUOTE_API).json()
            await update.message.reply_text(f"📜 “{r.get('content')}” — {r.get('author')}")
        except:
            await update.message.reply_text("Couldn't fetch a quote right now.")

    elif "history" in text or "today" in text:
        try:
            r = requests.get(HISTORY_API).json()
            events = r["data"]["Events"]
            e = random.choice(events)
            await update.message.reply_text(f"📅 On this day ({r['date']}): {e['year']} - {e['text']}")
        except:
            await update.message.reply_text("No history available now.")

    elif "anime" in text:
        await update.message.reply_text("Fetching anime updates... 🎌")
        try:
            response = requests.get(ANIME_API, params={"order_by": "start_date", "sort": "desc", "limit": 10})
            data = response.json()
            if "data" in data:
                anime = random.choice(data["data"])
                title = anime["title"]
                url = anime["url"]
                synopsis = anime.get("synopsis", "No synopsis available.")
                image = anime["images"]["jpg"]["image_url"]
                reply = f"""🎬 *{title}*\n{synopsis[:300]}...\n🔗 [More Info]({url})"""
                await update.message.reply_photo(photo=image, caption=reply, parse_mode="Markdown")
            else:
                await update.message.reply_text("Couldn't find any anime updates.")
        except Exception as e:
            print(e)
            await update.message.reply_text("Anime update failed 😔")

    else:
        await update.message.reply_text("""Try typing:
- hi
- fact
- cat
- quote
- anime
- today
- i love you
- have you lunch""")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "there"
    await update.message.reply_text(f"""Hey {user}! 👋
Say 'hi', 'fact', 'anime', 'quote', 'history', or fun stuff like 'I love you'.""")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
