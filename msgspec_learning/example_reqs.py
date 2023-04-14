from __future__ import annotations

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from typing import Union, Any, Set, TYPE_CHECKING, Type

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

import requests
import requests_cache

from schemas.request_models import (
    RequestClient,
    ClientCacheSettings,
    RequestClientSession,
    ClientResponse,
)
from utils.requests_util.cache_handler import make_cache_session
from utils.requests_util.encode_decode import encode_clientresponse

random_user_cache_conf = ClientCacheSettings(
    url=random_user_api_url, cache_name="random_user_api", backend="sqlite"
)
random_user_backend = make_cache_session(cache_settings=random_user_cache_conf)

_client = make_cache_session(cache_settings=random_user_cache_conf)

res = _client.get()
print(f"[DEBUG] Results ({type(res)}):\n{res}")

# res_dict = res.to_dict()
# print(f"[DEBUG] Res dict:\n{res_dict}")

encode_msg = {
    "url": res.url,
    "revalidated": res.revalidated,
    "ok": res.ok,
    "status_code": res.status_code,
    "reason": res.reason,
    "from_cache": res.from_cache,
    "expires": res.expires,
    "headers": res.headers,
    "content": res.content,
    "size": res.size,
}

# msg = msgspec.json.encode(encode_msg)
# _decode = msgspec.json.decode(msg)

msg = encode_clientresponse(res=res)
print(f"[DEBUG] Encoded msg ({type(msg)}):\n{msg}")

# print(f"[DEBUG] Decoded message ({type(_decode)}): {_decode}")

if TYPE_CHECKING:
    ...
