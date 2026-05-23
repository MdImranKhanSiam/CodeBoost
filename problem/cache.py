from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


PROBLEMS_PAGE_CACHE_KEY = "problems:page:{user_id}"


TTL_PROBLEMS_PAGE = 60 * 60 * 12


# PROBLEMS_PAGE
def get_problems_page(user_id):
    try:
        return cache.get(PROBLEMS_PAGE_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: get_problems_page")
        return None
    
def set_problems_page(user_id, data):
    try:
        cache.set(PROBLEMS_PAGE_CACHE_KEY.format(user_id=user_id), data, TTL_PROBLEMS_PAGE)
    except Exception:
        logger.warning("Cache unavailable: set_problems_page")

def invalidate_problems_page(user_id):
    try:
        cache.delete(PROBLEMS_PAGE_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: invalidate_problems_page")