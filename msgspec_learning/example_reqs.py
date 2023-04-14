from __future__ import annotations

from typing import Union, Any, Set, TYPE_CHECKING

from lib.constants import (
    random_user_api_url,
    default_cache_dir,
    default_cache_settings,
    default_req_client_settings,
    allowed_cache_backends,
    allowed_conf_filetypes,
    allowed_serializers,
)

from schemas.request_models import (
    RequestClient,
    ClientCacheSettings,
    RequestClientSession,
)
from utils.requests_util.cache_handler import make_cache_session

random_user_cache_conf = ClientCacheSettings(
    url=random_user_api_url, cache_name="random_user_api", backend="sqlite"
)
random_user_backend = make_cache_session(cache_settings=random_user_cache_conf)

_client = make_cache_session(cache_settings=random_user_cache_conf)

res = _client.get()

print(f"[DEBUG] Results:\n{res}")

if TYPE_CHECKING:
    ...
