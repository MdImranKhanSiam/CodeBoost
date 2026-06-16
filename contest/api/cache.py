from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)



CONTEST_LEADERBOARD_CACHE_KEY = "contest:leaderboard:{contest_id}"



TTL_CONTEST_LEADERBOARD = 15




# CONTEST_LEADERBOARD
def get_contest_leaderboard(contest_id):
    try:
        return cache.get(CONTEST_LEADERBOARD_CACHE_KEY.format(contest_id=contest_id))
    except Exception:
        logger.warning("Cache unavailable: get_contest_leaderboard")
        return None
    

def set_contest_leaderboard(contest_id, data):
    try:
        cache.set(CONTEST_LEADERBOARD_CACHE_KEY.format(contest_id=contest_id), data, TTL_CONTEST_LEADERBOARD)
    except Exception:
        logger.warning("Cache unavailable: set_contest_leaderboard")


def invalidate_contest_leaderboard(contest_id):
    try:
        cache.delete(CONTEST_LEADERBOARD_CACHE_KEY.format(contest_id=contest_id))
    except Exception:
        logger.warning("Cache unavailable: invalidate_contest_leaderboard")
