import asyncio
import threading
import time


from file_work import load_json
from telegram.ext import Application, CommandHandler
from tg_notif import *


def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(load_json()["token"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("exit", exit_user))
    print("Telegram bot is working")

    try:
        app.run_polling()
    finally:
        loop.close()


bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()
time.sleep(2)


async def send_notifications():
    app = Application.builder().token(load_json()["token"]).build()
    await notify_all_users(app, "update found")


async def async_worker(name: str, delay: float):
    while True:
        print(f"[async] {name}: still alive...")
        await asyncio.sleep(delay)


async def async_demo():
    task1 = asyncio.create_task(async_worker("task 1", 1.0))
    task2 = asyncio.create_task(async_worker("task 2", 1.5))

    await asyncio.sleep(5)
    task1.cancel()
    task2.cancel()


def threaded_worker(name: str, delay: float):
    for i in range(5):
        print(f"[thread] {name}: step {i}")
        time.sleep(delay)


def start_thread_demo():
    t1 = threading.Thread(target=threaded_worker, args=("thread 1", 0.7), daemon=True)
    t2 = threading.Thread(target=threaded_worker, args=("thread 2", 1.0), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def main():
    settings = load_json()

    print("threads")
    start_thread_demo()

    print("asyncio")
    asyncio.run(async_demo())

    print("demo is over. bot is running")


if __name__ == "__main__":
    main()
