# ai_service.py
import os
import random
import logging
from groq import Groq, RateLimitError, APIStatusError

logger = logging.getLogger(__name__)


def get_groq_keys() -> list[str]:
    """Collects every GROQ_API_KEY_N from the environment, in order."""
    keys = []
    i = 1
    while True:
        key = os.getenv(f'GROQ_API_KEY_{i}')
        if not key:
            break
        keys.append(key)
        i += 1
    return keys


def call_groq(prompt: str, model: str = "openai/gpt-oss-120b") -> str:
    keys = get_groq_keys()

    if not keys:
        raise RuntimeError("No Groq API keys configured")

    # shuffle so load spreads across keys instead of always hammering key #1 first
    random.shuffle(keys)

    last_error = None

    for idx, key in enumerate(keys):
        try:
            client = Groq(api_key=key)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        except RateLimitError as e:
            logger.warning(f"[Groq] Key #{idx+1} rate limited, trying next...")
            last_error = e
            continue

        except APIStatusError as e:
            # covers other 4xx/5xx (invalid key, quota exhausted, etc.) — skip and try next key
            logger.warning(f"[Groq] Key #{idx+1} failed ({e.status_code}), trying next...")
            last_error = e
            continue

        except Exception as e:
            logger.warning(f"[Groq] Key #{idx+1} unexpected error: {e}")
            last_error = e
            continue

    # every key failed
    raise RuntimeError(f"All Groq keys exhausted. Last error: {last_error}")