from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import json

TOKEN = ""
DB_FILE = "links.json"

try:
    with open(DB_FILE, "r", encoding="utf-8") as f:
        links = json.load(f)
        if not isinstance(links, list):
            links = []
except:
    links = []

last_link = None


def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_link

    text = update.message.text

    if not text:
        return

    text = text.strip()

    if "http" in text:
        last_link = text
        await update.message.reply_text("שלח עכשיו הסבר ללינק")
        return

    if last_link is not None:
        links.append({
            "url": last_link,
            "description": text
        })
        save_db()
        last_link = None
        await update.message.reply_text("נשמר ✅")
        return

    query = text.lower()

    results = []
    for item in links:
        if not isinstance(item, dict):
            continue

        description = str(item.get("description", ""))
        url = str(item.get("url", ""))

        if query in description.lower():
            results.append(f"{description}\n{url}")

    if not results:
        await update.message.reply_text("לא מצאתי")
        return

    await update.message.reply_text("\n\n".join(results[:10]))


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()
