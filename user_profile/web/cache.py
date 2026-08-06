from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


AUTHORED_PROBLEMS_PAGE_CACHE_KEY = "authored:problems:page:{user_id}"


TTL_PROBLEMS_PAGE = 60 * 60 * 24



# PROBLEMS_PAGE
def get_authored_problems_page(user_id):
    try:
        return cache.get(AUTHORED_PROBLEMS_PAGE_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: get_authored_problems_page")
        return None
    

def set_authored_problems_page(user_id, data):
    try:
        cache.set(AUTHORED_PROBLEMS_PAGE_CACHE_KEY.format(user_id=user_id), data, TTL_PROBLEMS_PAGE)
    except Exception:
        logger.warning("Cache unavailable: set_authored_problems_page")


def invalidate_authored_problems_page(user_id):
    try:
        cache.delete(AUTHORED_PROBLEMS_PAGE_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: invalidate_authored_problems_page")


# def invalidate_user_authored_problems_page(user_id):
#     try:
#         cache.delete(AUTHORED_PROBLEMS_PAGE_CACHE_KEY.format(user_id=user_id))
#         logger.info(f"Problems Page Cache Invalidated For User {user_id}")
#     except Exception:
#         logger.warning("Cache unavailable: invalidate_user_problems_page")



