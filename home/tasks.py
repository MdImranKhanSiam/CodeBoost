from celery import shared_task
from django.core.mail import EmailMessage


@shared_task(ignore_result=True, bind=True, max_retries=3, default_retry_delay=5, acks_late=True, reject_on_worker_lost=True,)
def send_welcome_email(self,subject,message,sender,receiver):
    try:
        email = EmailMessage(
            subject,
            message,
            sender,
            [receiver]
        )

        email.content_subtype = "html"
        email.send(fail_silently=True)
        pass
    except Exception as exc:
        raise self.retry(exc=exc)
    




# @shared_task(ignore_result=True, bind=True, max_retries=3, default_retry_delay=5, acks_late=True, reject_on_worker_lost=True,)
# def check_rate_limit(self,api,limit):
#     try:
#         import asyncio
#         import aiohttp

#         async def fetch(session, url):
#             async with session.get(url) as response:
#                 return response.status

#         async def main():
#             async with aiohttp.ClientSession() as session:
#                 tasks = [
#                     fetch(session, api)
#                     for _ in range(limit)
#                 ]

#                 results = await asyncio.gather(*tasks)
#                 print(results)

#         asyncio.run(main())
#         pass
#     except Exception as exc:
#         raise self.retry(exc=exc)
    






# # ── Module-level imports (top of your tasks.py) ───────────────────────────────
# import asyncio
# import random
# import ssl
# import sys
# from itertools import cycle

# import aiohttp

# # ── Celery Task ───────────────────────────────────────────────────────────────

# @shared_task(
#     ignore_result=True,
#     bind=True,
#     acks_late=True,
#     reject_on_worker_lost=True,
# )
# def check_rate_limit(self, api: str, limit: int) -> None:
#     """
#     Fire `limit` async HTTP GET requests to `api` as fast as possible.

#     - ProactorEventLoop (IOCP) on Windows — no file-descriptor cap.
#     - Connection pool + keep-alive shared across all requests.
#     - Proxy list cycled per request (leave PROXIES empty to use own IP).
#     - Headers (User-Agent, Accept-Language, X-Forwarded-For …) randomised
#       per request to avoid fingerprinting.
#     - All responses and errors silently discarded.
#     """
#     try:

#         # ── Tunables ──────────────────────────────────────────────────────────
#         # Windows IOCP can handle thousands of sockets, but stay conservative.
#         # 200 simultaneous connections is safe and fast on Windows.
#         CONCURRENCY: int = limit

#         TIMEOUT = aiohttp.ClientTimeout(
#             total     = 15,
#             connect   = 5,
#             sock_read = 10,
#         )

#         # ── Proxy list ────────────────────────────────────────────────────────
#         # HTTP  → "http://host:port"  or  "http://user:pass@host:port"
#         # SOCKS5 → install aiohttp-socks; see _fetch() note below.
#         # Leave empty to send all requests from the worker's own IP.
#         PROXIES: list[str] = [
#             # "http://11.22.33.44:3128",
#             # "http://user:pass@55.66.77.88:8080",
#         ]

#         # ── Browser fingerprints ──────────────────────────────────────────────
#         _UA: list[str] = [
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#             "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 "
#             "(KHTML, like Gecko) Version/17.5 Safari/605.1.15",
#             "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
#             "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 "
#             "(KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
#             "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
#             "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
#         ]

#         _ACCEPT_LANGS: list[str] = [
#             "en-US,en;q=0.9",
#             "en-GB,en;q=0.8",
#             "en-AU,en;q=0.7,en-US;q=0.5",
#             "fr-FR,fr;q=0.9,en;q=0.4",
#             "de-DE,de;q=0.9,en;q=0.5",
#         ]

#         # ── Helpers ───────────────────────────────────────────────────────────

#         def _rand_ip() -> str:
#             """Random-looking public IPv4 (avoids RFC-1918 / reserved blocks)."""
#             first = random.choice([12, 34, 45, 52, 66, 77, 91, 103, 185, 194, 203, 217, 220])
#             return (
#                 f"{first}."
#                 f"{random.randint(1, 254)}."
#                 f"{random.randint(1, 254)}."
#                 f"{random.randint(1, 254)}"
#             )

#         def _headers() -> dict[str, str]:
#             """
#             Randomised browser-like headers per request.

#             X-Forwarded-For / X-Real-IP / Forwarded spoof the origin IP at the
#             HTTP application layer — effective only when the target server or a
#             CDN trusts these headers for rate-limiting.
#             They do NOT change the real TCP source IP (only proxies do that).
#             """
#             return {
#                 "User-Agent":      random.choice(_UA),
#                 "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#                 "Accept-Language": random.choice(_ACCEPT_LANGS),
#                 "Accept-Encoding": "gzip, deflate, br",
#                 "Cache-Control":   "no-cache",
#                 "Pragma":          "no-cache",
#                 "DNT":             "1",
#                 # ── IP spoofing (application layer only) ──────────────────────
#                 "X-Forwarded-For": f"{_rand_ip()}, {_rand_ip()}",
#                 "X-Real-IP":       _rand_ip(),
#                 "Forwarded":       f"for={_rand_ip()};proto=https",
#                 "Via":             f"1.1 {_rand_ip()} (squid/5.9)",
#             }

#         # ── Core fetch ────────────────────────────────────────────────────────

#         async def _fetch(
#             session : aiohttp.ClientSession,
#             url     : str,
#             proxy   : str | None,
#             retries : int = 2,
#         ) -> None:
#             """
#             Single GET — fully silent.
#             Retries with exponential back-off; swallows all exceptions.

#             SOCKS5 note: aiohttp doesn't support socks5:// in proxy= kwarg.
#             For SOCKS5, install aiohttp-socks and use:
#                 ProxyConnector.from_url("socks5://host:port")
#             """
#             for attempt in range(retries + 1):
#                 try:
#                     async with session.get(
#                         url,
#                         proxy           = proxy,
#                         headers         = _headers(),
#                         timeout         = TIMEOUT,
#                         allow_redirects = True,
#                         ssl             = False,  # skip TLS verify for speed
#                     ) as resp:
#                         await resp.read()         # drain → socket back to pool
#                         return
#                 except Exception:
#                     if attempt == retries:
#                         return
#                     await asyncio.sleep(0.05 * (2 ** attempt))  # 50 ms → 100 ms

#         # ── Async orchestrator ────────────────────────────────────────────────

#         async def main() -> None:
#             proxy_cycle = cycle(PROXIES) if PROXIES else cycle([None])
#             sem         = asyncio.Semaphore(CONCURRENCY)

#             ssl_ctx                = ssl.create_default_context()
#             ssl_ctx.check_hostname = False
#             ssl_ctx.verify_mode    = ssl.CERT_NONE

#             connector = aiohttp.TCPConnector(
#                 limit                 = 0,      # no cap on pooled connections
#                 limit_per_host        = 0,      # no cap per host
#                 keepalive_timeout     = 30,     # hold idle sockets open (s)
#                 force_close           = False,  # keep-alive ON
#                 enable_cleanup_closed = True,   # prune broken connections
#                 ssl                   = ssl_ctx,
#             )

#             async with aiohttp.ClientSession(connector=connector) as session:

#                 async def _shoot() -> None:
#                     async with sem:
#                         await _fetch(session, api, next(proxy_cycle))

#                 await asyncio.gather(
#                     *(_shoot() for _ in range(limit)),
#                     return_exceptions=True,
#                 )

#         # ── Run ───────────────────────────────────────────────────────────────
#         # asyncio.run() picks up WindowsProactorEventLoopPolicy set at module
#         # level, so the loop it creates uses IOCP — no select() FD cap.
#         asyncio.run(main())

#     except Exception:
#         raise










import asyncio
import logging
from collections import Counter
import aiohttp

logger = logging.getLogger(__name__)

ERR_TIMEOUT = -1
ERR_CONNECTION = -2
ERR_CLIENT = -3
ERR_UNKNOWN = -99

MAX_CONCURRENT = 200

async def _fetch(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore) -> int:
    async with sem:
        try:
            async with session.get(url) as response:
                await response.read()
                return response.status
        except asyncio.TimeoutError:
            return ERR_TIMEOUT
        except aiohttp.ClientConnectionError:
            return ERR_CONNECTION
        except aiohttp.ClientError:
            return ERR_CLIENT
        except Exception:
            logger.exception("Unexpected error fetching %s", url)
            return ERR_UNKNOWN


async def _fire_burst(url: str, count: int, max_concurrent: int = MAX_CONCURRENT, timeout: float = 10.0) -> Counter:
    connector = aiohttp.TCPConnector(
        limit=max_concurrent,
        limit_per_host=max_concurrent,
        ttl_dns_cache=300,
    )
    timeout_cfg = aiohttp.ClientTimeout(total=timeout)
    sem = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout_cfg) as session:
        tasks = [asyncio.create_task(_fetch(session, url, sem)) for _ in range(count)]
        results = await asyncio.gather(*tasks)

    return Counter(results)


def fire_burst_sync(url: str, count: int, max_concurrent: int = MAX_CONCURRENT, timeout: float = 10.0) -> Counter:
    return asyncio.run(_fire_burst(url, count, max_concurrent=max_concurrent, timeout=timeout))


@shared_task(
    ignore_result=True,
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
)
def check_rate_limit(self, api: str, limit: int) -> None:
    results = fire_burst_sync(api, limit)

    success = results.get(200, 0)
    failed = limit - success

    logger.info("success=%d", success)
    logger.info("failed=%d", failed)