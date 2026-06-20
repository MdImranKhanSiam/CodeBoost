from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


USER_PROFILE_CACHE_KEY = "user:profile:{user_id}"
USER_PROGRESS_HEATMAP_CACHE_KEY = "user:progress:heatmap:{user_id}"



TTL_USER_PROFILE = 60 * 60 * 24
TTL_USER_PROGRESS_HEATMAP = 60 * 60 * 24



# USER_PROFILE
def get_user_profile(user_id):
    try:
        return cache.get(USER_PROFILE_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: get_user_profile {user_id}")
        return None
    

def set_user_profile(user_id, data):
    try:
        cache.set(USER_PROFILE_CACHE_KEY.format(user_id=user_id), data, TTL_USER_PROFILE)
    except Exception:
        logger.warning("Cache unavailable: set_user_profile {user_id}")


def invalidate_user_profile(user_id):
    try:
        cache.delete(USER_PROFILE_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: invalidate_user_profile {user_id}")




# USER_PROGRESS_HEATMAP
def get_user_progress_heatmap(user_id):
    try:
        return cache.get(USER_PROGRESS_HEATMAP_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: get_user_progress_heatmap {user_id}")
        return None
    

def set_user_progress_heatmap(user_id, data):
    try:
        cache.set(USER_PROGRESS_HEATMAP_CACHE_KEY.format(user_id=user_id), data, TTL_USER_PROGRESS_HEATMAP)
    except Exception:
        logger.warning("Cache unavailable: set_user_progress_heatmap {user_id}")


def invalidate_user_progress_heatmap(user_id):
    try:
        cache.delete(USER_PROGRESS_HEATMAP_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: invalidate_user_progress_heatmap {user_id}")
