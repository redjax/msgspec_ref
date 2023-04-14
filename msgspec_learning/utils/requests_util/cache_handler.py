from requests_cache import CachedSession, SQLiteCache
from typing import Tuple

from schemas.request_models import ClientCacheSettings, RequestClient
from lib.constants import (
    allowed_cache_backends,
    allowed_serializers,
    default_cache_settings,
)


def get_sqlite_cache(
    cache_name: str = "example_cache", cache_dir: str = "cache"
) -> SQLiteCache:
    if cache_dir:
        cache_path = f"{cache_dir}/{cache_name}"
    else:
        cache_path = cache_name

    _cache = SQLiteCache(cache_path)

    return _cache


def make_cache_session(cache_settings: ClientCacheSettings = None) -> RequestClient:
    # print(f"Creating cache RequestClient. Cache settings:\n{cache_settings}")
    _session = RequestClient(
        url=cache_settings.url,
        cache_name=cache_settings.cache_name,
        cache_dir=cache_settings.cache_dir,
        backend=cache_settings.backend,
        expire_after=cache_settings.expire_after,
    )

    return _session
