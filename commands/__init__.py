from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp.web import Response
from linebot import AsyncHttpResponse
from linebot.models import MessageEvent, TextMessage

from utils import get_events
from .echo import echo
from .hello import hello

if TYPE_CHECKING:
    from bot import Bot

async def run_text_commands(bot: Bot, request: AsyncHttpResponse):
    events = await get_events(bot.parser, request)
    if isinstance(events, Response):
        return events
    
    for event in events:  # type: ignore
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        # List all text-related commands here
        await echo(bot, event)
        await hello(bot, event)
