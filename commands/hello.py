from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.web import Response
from linebot.models import MessageEvent, TextSendMessage

if TYPE_CHECKING:
    from bot import Bot

async def hello(bot: Bot, event: MessageEvent) -> Response:
    if event.message.text.lower() == "hello":
        profile = await bot.get_profile(event.source.user_id)
        await bot.reply_message(event.reply_token, TextSendMessage(f"Hello, {profile.display_name}!"))
    return Response(text="OK\n")
