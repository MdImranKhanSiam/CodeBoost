from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

USER_DATA_CACHE_KEY = "user:data:{user_id}"

TTL_USER_DATA = 60 * 60 * 12


# USER_DATA
def get_user_data(user_id):
    try:
        return cache.get(USER_DATA_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: get_user_data")
        return None

def set_user_data(user_id, data):
    try:
        cache.set(USER_DATA_CACHE_KEY.format(user_id=user_id), data, TTL_USER_DATA)
    except Exception:
        logger.warning("Cache unavailable: set_user_data")

def invalidate_user_data(user_id):
    try:
        cache.delete(USER_DATA_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: invalidate_user_data")

