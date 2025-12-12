import asyncio
from file_work import load_json
from status import check_servers, check_now
from telegram.ext import Application, CommandHandler
from tg_notif import start, exit_user


def main() -> None:
    settings = load_json()
    token = settings["token"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("exit", exit_user))
    app.add_handler(CommandHandler("check", check_now))

    async def on_startup(application: Application) -> None:
        asyncio.create_task(check_servers(application))

    app.post_init = on_startup

    print("Telegram bot is working")
    app.run_polling()


if __name__ == "__main__":
    main()
