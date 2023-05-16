from typing import List, Union

from aiohttp.web import Response
from linebot import AsyncHttpResponse, WebhookParser, WebhookPayload
from linebot.exceptions import InvalidSignatureError

async def get_events(parser: WebhookParser, request: AsyncHttpResponse) -> Union[WebhookPayload, List, Response]:
    sig = request.headers["X-Line-Signature"]
    body = await request.text()
    events: Union[WebhookPayload, List]

    try:
        events = parser.parse(body, sig)
        return events
    except InvalidSignatureError:
        return Response(status=400, text="Invalid Signature")