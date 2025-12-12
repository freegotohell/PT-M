from tg_data_base import conn, cursor
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


async def send_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Проверить хосты", callback_data="cmd_check")],
        [
            InlineKeyboardButton("Подписаться", callback_data="cmd_start"),
            InlineKeyboardButton("Отписаться", callback_data="cmd_exit"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "cmd_check":
        await context.bot.send_message(chat_id=query.message.chat_id, text="/check")
    elif query.data == "cmd_start":
        await context.bot.send_message(chat_id=query.message.chat_id, text="/start")
    elif query.data == "cmd_exit":
        await context.bot.send_message(chat_id=query.message.chat_id, text="/exit")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    cursor.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("INSERT INTO users VALUES (NULL, ?)", (chat_id,))
        conn.commit()
        await update.message.reply_text("you've just subscribed to notif")
    else:
        await update.message.reply_text("you're already subscribed to notif")

    await send_menu(update, context)


async def exit_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    cursor.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    conn.commit()
    await update.message.reply_text("no more notif from here")
    await send_menu(update, context)


async def notify_all_users(app, message: str) -> None:
    cursor.execute("SELECT chat_id FROM users")
    subscribers = cursor.fetchall()
    for subscriber in subscribers:
        try:
            await app.bot.send_message(chat_id=subscriber[0], text=message)
        except Exception as e:
            print(f"err during sending notif to subscriber {e}")