from schemas.request_models import ClientCacheSettings, RequestClient


def get_request_client(cache_settings: ClientCacheSettings = None) -> RequestClient:
    _client = RequestClient(
        url=cache_settings.url,
        use_cache=cache_settings.use_cache,
        backend=cache_settings.backend,
        cache_name=cache_settings.cache_name,
        cache_dir=cache_settings.cache_dir,
        expire_after=cache_settings.expire_after,
    )

    return _client
