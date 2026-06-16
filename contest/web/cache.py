from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)



CONTESTS_PAGE_CACHE_KEY = "contests:page"
PRIVATE_CONTESTS_CACHE_KEY = "private:contests:{user_id}"



TTL_CONTESTS_PAGE = 60 * 60 * 24
TTL_PRIVATE_CONTESTS = 60 * 60 * 24



# CONTESTS_PAGE
def get_contests_page():
    try:
        return cache.get(CONTESTS_PAGE_CACHE_KEY)
    except Exception:
        logger.warning("Cache unavailable: get_contests_page")
        return None
    

def set_contests_page(data):
    try:
        cache.set(CONTESTS_PAGE_CACHE_KEY, data, TTL_CONTESTS_PAGE)
    except Exception:
        logger.warning("Cache unavailable: set_contests_page")


def invalidate_contests_page():
    try:
        cache.delete(CONTESTS_PAGE_CACHE_KEY)
    except Exception:
        logger.warning("Cache unavailable: invalidate_contests_page")






# PRIVATE_CONTESTS
def get_private_contests(user_id):
    try:
        return cache.get(PRIVATE_CONTESTS_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: get_private_contests")
        return None
    

def set_private_contests(user_id, data):
    try:
        cache.set(PRIVATE_CONTESTS_CACHE_KEY.format(user_id=user_id), data, TTL_PRIVATE_CONTESTS)
    except Exception:
        logger.warning("Cache unavailable: set_private_contests")


def invalidate_private_contests():
    try:
        cache.delete_pattern("private:contests:*")
    except Exception:
        logger.warning("Cache unavailable: invalidate_private_contests")

