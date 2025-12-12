from tg_data_base import conn, cursor
from telegram.ext import ContextTypes
from telegram import Update


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    cursor.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO users VALUES (NULL, ?)", (chat_id,))
        conn.commit()
        await update.message.reply_text("you ve just subscribed to notif")
    else:
        await update.message.reply_text("you r already subscribed to notif")


async def exit_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    cursor.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    conn.commit()
    await update.message.reply_text(
        "no more notif from here"
    )


async def notify_all_users(app, message):
    cursor.execute("SELECT chat_id FROM users")
    subscribers = cursor.fetchall()
    for subscriber in subscribers:
        try:
            await app.bot.send_message(chat_id=subscriber[0], text=message)
        except Exception as e:
            print(f"err during sending notif {subscriber}: {e}")
