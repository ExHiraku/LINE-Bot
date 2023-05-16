from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.web import Response
from linebot.models import MessageEvent, TextSendMessage

if TYPE_CHECKING:
    from bot import Bot

async def echo(bot: Bot, event: MessageEvent) -> Response:
    if event.message.text.startswith("echo "):
        response = event.message.text.split("echo ")[1]
        if response:
            await bot.reply_message(event.reply_token, TextSendMessage(response))
    return Response(text="OK\n")