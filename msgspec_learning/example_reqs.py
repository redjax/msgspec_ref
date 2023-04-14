from __future__ import annotations

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from typing import Union, Any, Set, TYPE_CHECKING

import msgspec
import json
import datetime

from lib.constants import (
    random_user_api_url,
    default_cache_dir,
    default_cache_settings,
    default_req_client_settings,
    allowed_cache_backends,
    allowed_conf_filetypes,
    allowed_serializers,
)

if TYPE_CHECKING:
    ...

from schemas.request_models import (
    RequestClient,
    ClientCacheSettings,
    RequestClientSession,
    ClientResponse,
)
from utils.requests_util.cache_handler import make_cache_session

random_user_cache_conf = ClientCacheSettings(
    url=random_user_api_url, cache_name="random_user_api", backend="sqlite"
)
random_user_backend = make_cache_session(cache_settings=random_user_cache_conf)

_client = make_cache_session(cache_settings=random_user_cache_conf)

res = _client.get()
print(f"[DEBUG] Results ({type(res)}):\n{res}")

_encode_obj = json.dumps(
    {
        "status_code": res.status_code,
        "content": res.content_decoded,
        "created_at": str(res.created_at),
        "elapsed": str(res.elapsed),
        "encoding": res.encoding,
        "expires": str(res.expires),
        "from_cache": res.from_cache,
        "history": res.history,
        "ok": res.ok,
        "reason": res.reason,
    }
)

print(f"[INFO] Encoding response")

_content_encode = msgspec.json.encode(
    msgspec.to_builtins(
        _encode_obj,
        builtin_types=(
            datetime.datetime,
            datetime.date,
            datetime.time,
        ),
        str_keys=True,
    )
)
_content_decode = msgspec.json.decode(
    msgspec.from_builtins(
        _content_encode,
        type=ClientResponse,
        builtin_types=(datetime.datetime, datetime.date, datetime.time),
    ),
)

print(f"[DEBUG] Decoded message ({type(_content_decode)}):\n{_content_decode}")

if TYPE_CHECKING:
    ...
