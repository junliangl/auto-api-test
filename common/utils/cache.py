from cachetools import TTLCache, cached


def cache(maxsize: int, ttl: int, *args, **kwargs):
    ttl_cache = TTLCache(maxsize, ttl, *args, **kwargs)
    return cached(ttl_cache)
