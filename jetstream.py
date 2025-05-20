#! /usr/bin/env python3

# Bluesky jetstream via websocket


import asyncio
import websockets
import json
import re
from datetime import datetime, timezone


#uri = 'wss://jetstream1.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post'
#uri = 'wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post'
uri = 'wss://jetstream1.us-west.bsky.network/subscribe?wantedCollections=app.bsky.feed.post'
#uri = 'wss://jetstream2.us-west.bsky.network/subscribe?wantedCollections=app.bsky.feed.post'


# xterm formatting
def f(code): return '\x1B[' + str(code) + 'm'
def c(code): return f('38;5;' + str(code))
def ln_clear(): return '\r\x1B[K'


# Python-Variable aus einem JSON-String erzeugen (deserialization)
def json_to_py(json_string):
    try:
        return json.loads(json_string)
    except:
        return None


# filter characters
def char_filter(text):
    whitelist_pattern = r'[^' \
        r'\s\n' \
        r'\u0020-\u007E' \
        r'\u00A0-\u00FF' \
        r'\u0100-\u024F' \
        r'\u0370-\u03FF' \
        r'\u0400-\u04FF' \
        r'\u0590-\u05FF' \
        r'\u0600-\u06FF' \
        r'\u0900-\u097F' \
        r'\u3040-\u309F' \
        r'\u30A0-\u30FF' \
        r'\u4E00-\u9FFF' \
        r'\uAC00-\uD7AF' \
        r'\u2000-\u206F' \
        r'\u2070-\u209F' \
        r'\u20A0-\u20CF' \
        r'\u2200-\u22FF' \
        r'\u2300-\u23FF' \
        r']'
    return re.sub(whitelist_pattern, '', text)


async def listen():
    async with websockets.connect(uri) as websocket:
        while 1:
            json = await websocket.recv()
            data = json_to_py(json)
            try:
                text = data['commit']['record']['text']
            except:
                continue
            while ('\n' in text):
                text = text.replace('\n', '\\n')
            filtered = char_filter(text)
            if filtered.strip():
                date = datetime.now(tz=timezone.utc).astimezone().isoformat()
                print(c(39) + date + f(0), filtered)


if __name__ == '__main__':
    try:
        asyncio.run(listen())
    except KeyboardInterrupt:
        print(ln_clear(), end='')
