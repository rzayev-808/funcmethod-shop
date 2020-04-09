import asyncio

import aiohttp


@asyncio.coroutine
def func():
    response = yield from aiohttp.request("GET", "https://turbo.az")
    text = yield from response.text()
    print(text)


asyncio.get_event_loop().run_until_complete(func())