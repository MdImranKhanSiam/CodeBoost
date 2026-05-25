from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

HOMEPAGE_CACHE_KEY = "homepage"

TTL_HOMEPAGE = 60 * 60 * 12


# HOMEPAGE
def get_homepage():
    try:
        return cache.get(HOMEPAGE_CACHE_KEY)
    except Exception:
        logger.warning("Cache unavailable: get_homepage")
        return None

def set_homepage(data):
    try:
        cache.set(HOMEPAGE_CACHE_KEY, data, TTL_HOMEPAGE)
    except Exception:
        logger.warning("Cache unavailable: set_homepage")

def invalidate_homepage():
    try:
        cache.delete(HOMEPAGE_CACHE_KEY)
    except Exception:
        logger.warning("Cache unavailable: invalidate_homepage")
