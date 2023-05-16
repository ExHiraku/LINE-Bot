import asyncio
import logging
from argparse import ArgumentParser

from aiohttp import web

from bot import Bot

stop = asyncio.Event()

async def main(port=8000) -> None:
    bot = await Bot.start()

    app = web.Application()
    app.add_routes([web.post("/callback", bot.on_message)])  # type: ignore

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=port)
    await site.start()
    print(
        f"Running LINE bot on {site.name}"
    )
    await stop.wait()
    # Not setting anywhere because pterodactyl doesn't stop no matter what signal is sent
    # So server has to be killed

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + " [--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", type=int, default=8000, help="port")
    options = arg_parser.parse_args()

    asyncio.run(main(options.port))