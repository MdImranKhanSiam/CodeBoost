from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


PROBLEMS_PAGE_CACHE_KEY = "problems:page:{user_id}"
SUBMISSION_API_CACHE_KEY = "submission:api:{user_id}"
SUBMISSION_DETAILS_CACHE_KEY = "submission:details:{user_id}:{submission_id}"


TTL_PROBLEMS_PAGE = 60 * 60 * 12
TTL_SUBMISSION_API = 60 * 60 * 12
TTL_SUBMISSION_DETAILS = 60 * 60 * 12






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


def invalidate_problems_page():
    try:
        cache.delete_pattern("problems:page:*")
    except Exception:
        logger.warning("Cache unavailable: invalidate_problems_page")






# SUBMISSION_API
def get_submission_api(user_id):
    try:
        return cache.get(SUBMISSION_API_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: get_submission_api")
        return None
    

def set_submission_api(user_id, data):
    try:
        cache.set(SUBMISSION_API_CACHE_KEY.format(user_id=user_id), data, TTL_SUBMISSION_API)
    except Exception:
        logger.warning("Cache unavailable: set_submission_api")


def invalidate_submission_api(user_id):
    try:
        cache.delete(SUBMISSION_API_CACHE_KEY.format(user_id=user_id))
    except Exception:
        logger.warning("Cache unavailable: invalidate_submission_api")






# SUBMISSION_DETAILS
def get_submission_details(user_id, submission_id):
    try:
        return cache.get(SUBMISSION_DETAILS_CACHE_KEY.format(user_id=user_id, submission_id=submission_id))
    except Exception:
        logger.warning("Cache unavailable: get_submission_details")
        return None
    

def set_submission_details(user_id, submission_id, data):
    try:
        cache.set(SUBMISSION_DETAILS_CACHE_KEY.format(user_id=user_id, submission_id=submission_id), data, TTL_SUBMISSION_DETAILS)
    except Exception:
        logger.warning("Cache unavailable: set_submission_details")


def invalidate_all_submission_details(user_id):
    try:
        cache.delete_pattern(f"submission:details:{user_id}:*")
    except Exception:
        logger.warning("Cache unavailable: invalidate_submission_details")


def invalidate_current_submission_details(user_id, submission_id):
    try:
        cache.delete(SUBMISSION_DETAILS_CACHE_KEY.format(user_id=user_id, submission_id=submission_id))
    except Exception:
        logger.warning("Cache unavailable: invalidate_submission_details")





