import asyncio
from file_work import load_json
from status import check_servers, check_now
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from tg_notif import start, exit_user, menu_callback, send_menu


def main() -> None:
    """Initialize Telegram bot, register handlers and start polling."""
    settings = load_json()
    token = settings["token"]
    hosts = settings.get("hosts", [])
    commands = settings.get("commands", {})

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler(commands.get("subscribe", "start"), start))
    app.add_handler(CommandHandler(commands.get("unsubscribe", "exit"),
                                   exit_user))
    app.add_handler(CommandHandler(commands.get("check_hosts", "check"),
                                   lambda u, c: check_now(u, c, hosts)))
    app.add_handler(CommandHandler("menu", send_menu))
    app.add_handler(CallbackQueryHandler(menu_callback))

    async def on_startup(application: Application) -> None:
        asyncio.create_task(check_servers(application, hosts))

    app.post_init = on_startup

    print("Telegram bot is working")
    app.run_polling()


if __name__ == "__main__":
    main()
