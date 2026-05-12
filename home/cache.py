from django.core.cache import cache

USER_DATA_CACHE_KEY = "user:data:{user_id}"

TTL_USER_DATA = 60 * 60 * 24 * 7

def get_user_data(user_id):
    return cache.get(USER_DATA_CACHE_KEY.format(user_id=user_id))

def set_user_data(user_id, data):
    cache.set(USER_DATA_CACHE_KEY.format(user_id=user_id), data, TTL_USER_DATA)

def invalidate_user_data(user_id):
    cache.delete(USER_DATA_CACHE_KEY.format(user_id=user_id))