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
        await update.message.reply_text("Вы подписаны на уведомления.")
    else:
        await update.message.reply_text("Вы уже подписаны на уведомления.")


async def exit_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    cursor.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    conn.commit()
    await update.message.reply_text("Вы больше не будете получать уведомления.")


async def notify_all_users(app, message="Новый тендер"):
    cursor.execute("SELECT chat_id FROM users")
    subscribers = cursor.fetchall()
    for subscriber in subscribers:
        try:
            await app.bot.send_message(chat_id=subscriber[0], text=message)
        except Exception as e:
            print(f"Ошибка отправки уведомления {subscriber}: {e}")
