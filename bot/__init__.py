import os
import sys
from typing import List, Optional, Union

import aiohttp
from aiohttp import web
from dotenv import load_dotenv
from linebot import AsyncLineBotApi, WebhookParser, WebhookPayload, AsyncHttpResponse
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import InvalidSignatureError

from commands import run_text_commands

load_dotenv()

CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
if not CHANNEL_SECRET:
    print("Missing environment variable 'CHANNEL_SECRET'.")
    sys.exit(1)
elif not CHANNEL_ACCESS_TOKEN:
    print("Missing environment variable 'CHANNEL_ACCESS_TOKEN'.")
    sys.exit(1)


class Bot(AsyncLineBotApi):
    client: AiohttpAsyncHttpClient
    parser: WebhookParser
    session: aiohttp.ClientSession

    @classmethod
    async def start(cls) -> "Bot":
        session = aiohttp.ClientSession()
        client = AiohttpAsyncHttpClient(session)
        bot = cls(CHANNEL_ACCESS_TOKEN, client)
        bot.client = client
        bot.parser = WebhookParser(CHANNEL_SECRET)
        bot.session = session
        return bot
    
    async def validate_request(self, request: AsyncHttpResponse) -> Union[WebhookPayload, List, web.Response]:
        sig = request.headers["X-Line-Signature"]
        body = await request.text()
        events: Union[WebhookPayload, List]

        try:
            events = self.parser.parse(body, sig)
            return events
        except InvalidSignatureError:
            return web.Response(status=400, text="Invalid Signature")
        
    async def on_message(self, request: AsyncHttpResponse) -> Optional[web.Response]:
        return await run_text_commands(self, request)
    
