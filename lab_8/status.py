import asyncio
import socket
from telegram import Update
from telegram.ext import ContextTypes
from tg_notif import notify_all_users


class ServerStatus:
    """Represent server availability status (host and is-down flag)."""
    def __init__(self, host: str, down: bool):
        self.host = host
        self.down = down


async def ping_servers(
        hosts: list[str],
        timeout: float = 3.0
) -> list[ServerStatus]:
    """Check availability of multiple hosts in parallel and return their statuses."""
    loop = asyncio.get_running_loop()
    results: list[ServerStatus] = []

    def check_host(host: str, port: int = 80) -> ServerStatus:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return ServerStatus(host, False)
        except OSError:
            return ServerStatus(host, True)

    port = 80
    tasks = [loop.run_in_executor(None, check_host, host, port)
             for host in hosts]

    for task in asyncio.as_completed(tasks):
        status = await task
        results.append(status)

    return results


async def check_servers(app, hosts: list[str], interval: int = 600) -> None:
    """Periodically check hosts and notify users if any servers are down."""
    while True:
        status_list = await ping_servers(hosts)
        down_hosts = [s.host for s in status_list if s.down]
        if not down_hosts:
            await asyncio.sleep(interval)
        else:
            await notify_all_users(app,
                                   f"server {down_hosts} is not available")
            await asyncio.sleep(interval)


async def check_now(
        update: Update, context: ContextTypes.DEFAULT_TYPE,
        hosts: list[str]
) -> None:
    """Check hosts on demand and reply with current availability."""
    status_list = await ping_servers(hosts)
    down_hosts = [s.host for s in status_list if s.down]

    if not down_hosts:
        text = "servers are available"
    else:
        text = "not responding: " + ", ".join(down_hosts)

    await update.message.reply_text(text)
