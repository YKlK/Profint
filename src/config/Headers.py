from fake_useragent import UserAgent
import random


# Generador dinámico de User-Agents
def headers():
    ua = UserAgent(browsers=['chrome', 'firefox', 'edge'])

    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": f"es-ES,es;q=0.{random.randint(5, 9)},en;q=0.{random.randint(5, 9)}",
        "Accept-Encoding": "gzip, deflate, br, identity",
        "DNT": str(random.randint(0, 1)),
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers",
        "Connection": "keep-alive",
        "Referer": "https://www.amazon.com/" if random.random() > 0.5 else "https://www.google.com/"
    }